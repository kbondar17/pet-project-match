from aiogram import types
from aiogram.types import KeyboardButton, InlineKeyboardMarkup

from db.db_funs import repo
from bot.loader import dp, ya_disk, bot
from bot.utils.generators import generate_kb_with_users_likes
from photos import local_storage

@dp.callback_query_handler(text_contains='delete_profile')
async def delete(call: types.CallbackQuery):
    

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Да', callback_data='confirm_delete')],
                [InlineKeyboardButton(
                text='Описание проекта', callback_data='cancel_delete')],
        ]

    )



    await call.message.answer('Точно удалить?', reply_markup=kb)

@dp.callback_query_handler(text_contains='confirm_delete')
async def confirm(call: types.CallbackQuery):
    pass
    