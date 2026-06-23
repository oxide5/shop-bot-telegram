import aiosqlite as sq
async def start():
    async with sq.connect('catalog.db') as con:

            await con.execute("""
    CREATE TABLE IF NOT EXISTS catalog(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        photo TEXT,
                        description TEXT,
                        price FLOAT
                        )
                        """)
            

async def save_product(name, photo, description, price):
    async with sq.connect('catalog.db') as con:
        await con.execute("INSERT INTO catalog(name, photo, description, price) VALUES (?, ?, ?, ?)", (name, photo, description, price))
        await con.commit()


async def get_all_products():
    async with sq.connect('catalog.db') as con:
        con.row_factory = sq.Row
        cursor = await con.execute("SELECT * FROM catalog")
        rows = await cursor.fetchall()
        products = [dict(row) for row in rows]
        return products
    
async def get_product_by_id(product_id):
    async with sq.connect('catalog.db') as con:
        con.row_factory = sq.Row # Теперь можно обращаться как к словарю
        cursor = await con.execute("SELECT * FROM catalog WHERE id = ?", (product_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None
    
async def delete_product(product_id):
    async with sq.connect('catalog.db') as con:
        cursor = await con.execute("DELETE FROM catalog WHERE id = ?", (product_id,))
        await con.commit()
        return cursor
        