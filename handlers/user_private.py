from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from kbds import reply
from database.engine import get_all_products, get_product_by_id
from aiogram.enums import ParseMode
ro = Router()


    
@ro.message(CommandStart())
async def start_cmd(message:types.Message):
    name = message.from_user.first_name
    await message.answer(f"Hello {name}!")


@ro.message(Command('check_catalog'))
async def catalog(message:types.Message):
    builder = InlineKeyboardBuilder()
    products = await get_all_products()
    for product in products:
        builder.button(text=product['name'], callback_data=f"product_{product['id']}")
    builder.adjust(2)
    await message.answer("Our catalog:", reply_markup=builder.as_markup())
    

@ro.callback_query(F.data.startswith("product_"))
async def show_product_info(callback: types.CallbackQuery):
    
    product_id = int(callback.data.split("_")[1])
    print(product_id)
    product = await get_product_by_id(product_id)
    
    if product:
        bold_text_name = (f"<b>{product['name']}</b>")
        text = (
            f"📦{bold_text_name}\n\n"
            f"📝Description: {product.get('description', 'No description')}\n"
            f"💰Price: {product['price']} TMT."
        )
        
        await callback.message.answer_photo(photo=product['photo'], caption=text, parse_mode=ParseMode.HTML, reply_markup=reply.choice_product)
        await callback.answer()
    else:
        await callback.message.answer("Unfortunately, the product was not found.")


@ro.callback_query(F.data == "user_cancel_buy_product")
async def back_to_step1(callback: CallbackQuery):    
    await callback.message.delete()
