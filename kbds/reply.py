from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import Message, InlineKeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Check services'),
            KeyboardButton(text='Support'),
        ],
        [KeyboardButton(text='Check our website')]
    ],
    resize_keyboard=True,
)

choice_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Buy product', callback_data='user_buy_product'),
            InlineKeyboardButton(text='Cancel', callback_data='user_cancel_buy_product'),
        ],
    ]
)

del_kb = ReplyKeyboardRemove()