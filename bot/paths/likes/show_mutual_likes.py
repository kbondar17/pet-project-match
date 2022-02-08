from aiogram import types
from aiogram.types import KeyboardButton, InlineKeyboardMarkup

from db.db_funs import repo
from bot.loader import dp, ya_disk, bot
from bot.utils.generators import generate_kb_with_users_likes
from photos import local_storage


@dp.message_handler(text_contains='Взаимные лайки')
async def show_mutual_likes(message: types.Message):
   
    current_user, kb = generate_kb_with_users_likes(message.from_user.id)
    if not current_user:
        await message.answer('Взаимных лайков пока нет')
    else:
        text = f'Взаимный лайк с {current_user.name}!\n\nНапиши: {current_user.user_name}\n\n{current_user.self_description}\n\n{current_user.prog_lang}'
        if not current_user.profile_pic:
            await message.answer(text, reply_markup=kb)
        else:
            photo = local_storage.get_user_photo(current_user.uid)
            print('photo---', photo)
            await message.answer_photo(caption=text, photo=photo, reply_markup=kb)

    

@dp.callback_query_handler(text_contains='mutual')
async def paginate_mutual_likes(call: types.CallbackQuery):

    page = call.data.split('#')[-1]

    current_user, kb = generate_kb_with_users_likes(call.from_user.id, page=int(page))

    text = f'Взаимный лайк с {current_user.name}!\n\nНапиши: {current_user.user_name}\n\n{current_user.self_description}\n\n{current_user.prog_lang}'

    if not current_user.profile_pic:
        await call.message.edit_text(text, reply_markup=kb)
    else:
        photo = local_storage.get_user_photo(current_user.uid)
        media = types.InputMediaPhoto(photo)
        media.caption = text
        await call.message.edit_media(media=media, reply_markup=kb)

#        await call.message.answer_photo(caption=text, photo=photo, reply_markup=kb)
