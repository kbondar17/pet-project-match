from aiogram import types

from bot.loader import dp, ya_disk
from db.db_funs import db_funs


@dp.message_handler(text_contains='Показать мой профиль')
async def show_profile(message: types.Message):
    uid = message.from_user.id
    text = db_funs.get_self_description(uid=uid)
    photo = ya_disk.get_user_photo_link(uid)
    await message.answer_photo(caption=text, photo=photo)