import json
from aiogram import F, types, Router, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import os
from aiogram.enums import ParseMode
from database.engine import save_product
from dotenv import find_dotenv, load_dotenv
from database.engine import get_all_products, get_product_by_id, delete_product
from aiogram.utils.keyboard import InlineKeyboardBuilder

from kbds import reply

load_dotenv(find_dotenv())

ADMIN_ID = os.getenv("ADMIN_ID")
admin_id = int(ADMIN_ID)

admin_ro = Router()

back_to_name = InlineKeyboardButton(text="Back to name", callback_data='back_to_name')
back_to_photo = InlineKeyboardButton(text="Back to photo", callback_data='back_to_photo')
back_to_description = InlineKeyboardButton(text="Back to description", callback_data='back_to_description')

keyboard_name = InlineKeyboardMarkup(inline_keyboard=[[back_to_name]], resize_keyboard=True)
keyboard_photo = InlineKeyboardMarkup(inline_keyboard=[[back_to_photo]], resize_keyboard=True)
keyboard_description = InlineKeyboardMarkup(inline_keyboard=[[back_to_description]], resize_keyboard=True)



def get_confirm_delete_kb(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Yes delete', callback_data=f'confirm_del_{product_id}'),
                InlineKeyboardButton(text='❌ Cancel', callback_data='admin_cancel_delete_product'),
            ],
        ]
    )


admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Add item'),
            KeyboardButton(text='Delete item'),
        ],
    ],
    resize_keyboard=True,
)

del_kb = ReplyKeyboardRemove()

class Item(StatesGroup):
    name = State()
    photo = State()
    description = State()
    price = State()


@admin_ro.message(Command('admin'))
async def admin_search(message: types.Message):
    user_id = message.from_user.id
    if user_id == admin_id:
        await message.answer('Hello admin! What do you want to change', reply_markup=admin_panel)
        
@admin_ro.message(StateFilter('*'), Command("cancel"))
async def cancel_add(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Actions was cancelled", reply_markup=admin_panel)


@admin_ro.message(F.text.lower() == 'add item')
async def admin_add_item(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id == admin_id:
        await message.answer('Send me item\'s name', reply_markup = del_kb)
        await state.set_state(Item.name)



@admin_ro.message(Item.name, F.text)
async def set_item_name(message : types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer('Added! Send me item\'s photo', reply_markup=keyboard_name)
    await state.set_state(Item.photo)

@admin_ro.callback_query(F.data == "back_to_name")
async def back_to_n(callback: CallbackQuery, state: FSMContext):    
    await state.set_state(Item.name)
    await callback.message.edit_text("Enter new name for item")



@admin_ro.message(Item.photo)
async def set_item_photo(message : types.Message, state: FSMContext):
    if message.text:
        await message.answer("You can send me only photo")
        return
    else:
        photo_id = message.photo[-1].file_id
        await state.update_data(photo = photo_id)
        await message.answer('Added! Send me item\'s description', reply_markup=keyboard_photo)
        await state.set_state(Item.description)

@admin_ro.callback_query(F.data == "back_to_photo")
async def back_to_p(callback: CallbackQuery, state: FSMContext):    
    await state.set_state(Item.photo)
    await callback.message.edit_text("Send new photo for item")




@admin_ro.message(Item.description)
async def set_item_description(message : types.Message, state: FSMContext):
    if message.photo or message.text.isdigit(): 
        await message.answer("You can't add photo or numbers as a description")
        return
    else:
        text = message.text
        await state.update_data(description = text)
        await message.answer('Added! Send me item\'s price', reply_markup=keyboard_description)
        await state.set_state(Item.price)

@admin_ro.callback_query(F.data == "back_to_description")
async def back_to_d(callback: CallbackQuery, state: FSMContext):    
    await state.set_state(Item.description)
    await callback.message.edit_text("Send new desciption for item")



@admin_ro.message(Item.price)
async def set_item_price(message : types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
    except ValueError:
        await message.answer("Please enter a valid number for the price.")
    if message.photo:
        await message.answer("You cant add photo or letters as a price")
        return
    else:
        await state.update_data(price=message.text)
        data = await state.get_data()
        await message.answer("New item was added!")
        
        try:
            bold_text_name = (f"<b>{data['name']}</b>")
            response_text = (
                f'📦{bold_text_name}\n\n'
                f"📝Description: {data['description']}\n\n"
                f"💰Price: {data['price']} TMT."
                )
        except KeyError:
            await message.answer("Something went wrong, try again")
        
                
        
        await message.answer_photo(photo=data['photo'], caption=response_text, parse_mode=ParseMode.HTML)

        await save_product(data['name'], data['photo'], data['description'], data['price'])

        await state.clear()




    


@admin_ro.message(F.text.lower() == 'delete item')
async def admin_add_item(message: types.Message):
    user_id = message.from_user.id
    if user_id == admin_id:
        await message.answer('What do you want to delete?', reply_markup=reply.del_kb)
        builder = InlineKeyboardBuilder()
        products = await get_all_products()
        for product in products:
            builder.button(text=product['name'], callback_data=f"del_{product['id']}")
        builder.adjust(2)
        await message.answer("Select product to delete:", reply_markup=builder.as_markup())

@admin_ro.callback_query(F.data.startswith("del_"))
async def show_product_info(callback: types.CallbackQuery):
    
    product_id = int(callback.data.split("_")[-1])
    print(product_id)
    
    product = await get_product_by_id(product_id)
    
    if product:
        bold_text_name = (f"<b>{product['name']}</b>")
        text = (
            f"📦{bold_text_name}\n\n"
            f"📝Description: {product.get('description', 'No description')}\n"
            f"💰Price: {product['price']} TMT."
        )
        
        await callback.message.answer_photo(photo=product['photo'], 
                                            caption=text, 
                                            parse_mode=ParseMode.HTML, 
                                            reply_markup=get_confirm_delete_kb(product_id))
    else:
        await callback.message.answer("Unfortunately product wasnt found")

@admin_ro.callback_query(F.data.startswith("confirm_del_"))
async def delete_confirm_handler(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[-1])
    await delete_product(product_id)
    await callback.message.delete()
    await callback.answer("Successfully deleted!")
    await callback.answer('What do you want to delete?', reply_markup=reply.del_kb)
    builder = InlineKeyboardBuilder()
    products = await get_all_products()
    for product in products:
        builder.button(text=product['name'], callback_data=f"del_{product['id']}")
    builder.adjust(2)
    await callback.message.answer("Select product to delete:", reply_markup=builder.as_markup())
    await callback.answer()
    
@admin_ro.callback_query(F.data == "admin_cancel_delete_product")
async def back_to_step1(callback: CallbackQuery):    
    user_id = callback.from_user.id
    if user_id == admin_id:
        await callback.message.delete()
        await callback.message.answer('What do you want to delete?', reply_markup=reply.del_kb)
        builder = InlineKeyboardBuilder()
        products = await get_all_products()
        for product in products:
            builder.button(text=product['name'], callback_data=f"del_{product['id']}")
        builder.adjust(2)
        await callback.message.answer("Select product to delete:", reply_markup=builder.as_markup())
        await callback.answer()