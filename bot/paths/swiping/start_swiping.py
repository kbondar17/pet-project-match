from aiogram import types
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

from db.db_funs import repo
from bot.loader import dp, ya_disk
from photos import local_storage
import time


@dp.callback_query_handler(text_contains='swiping')
async def let_swipe(call: types.CallbackQuery, state: FSMContext):

    # async with state.proxy() as data:
    #     print('айди первого сообщения', data['prev_msg_id'])

    user_card = repo.generate_card_for_user(call.from_user.id)

    if not user_card:
        await call.message.answer('Новых профилей нет. Приходи попозже!')

    else:
        text = user_card.self_description
        photo = user_card.profile_pic
        name = user_card.name
        
        
        languages = ','.join([f'#{e}' for e in user_card.prog_lang.replace('{','').replace('}','').split(',')]
)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [KeyboardButton(text='Интересно 🔥', callback_data=f'like#{user_card.uid}')],
            [KeyboardButton(text='Дальше ➡️', callback_data='swiping')]
            ])


        text = f'{name}\n\n{text}\n\nЯзыки: {languages}'


        if not photo:
            await call.message.answer(text=text, reply_markup=kb)

        else:
            # photo = ya_disk.get_user_photo_link(user_id=user_card.uid)
            photo = local_storage.get_user_photo(user_card.uid)
            media = types.InputMediaPhoto(photo)
            media.caption = text
            await call.message.edit_media(media=media, reply_markup=kb)
           # await call.message.answer(text = f'Time: {time.time()- start}')



@dp.message_handler(text_contains='Искать!')
async def lets_swipe_2(message: types.Message,  state: FSMContext):

    existing_desr = repo.get_self_description(message.from_user.id)
    
    if not existing_desr:
        kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Добавить инфу в профиль', callback_data='change_info')]]
            )

        await message.answer('Сначала расскажи о себе и своем проекте!', reply_markup=kb)
    
    else:
        user_card = repo.generate_card_for_user(message.from_user.id)
        if not user_card:
            await message.answer('Новых профилей нет. Приходи попозже!')

        else:
            text = user_card.self_description
            photo = user_card.profile_pic
            name = user_card.name
            
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [KeyboardButton(text='Интересно 🔥', callback_data=f'like#{user_card.uid}')],
                [KeyboardButton(text='Дальше ➡️', callback_data='swiping')]
                ])


            text = f'{name}\n\n{text}'

            if not photo:
                await message.answer(text=text, reply_markup=kb)
            
            else:
    #            photo = ya_disk.get_user_photo_link(user_id=user_card.uid)
                photo = local_storage.get_user_photo(user_card.uid)

                media = {
                    "type": "photo",
                    "media":photo,
                    "caption":text,

                }
                await message.answer_photo(photo=photo, caption=text, reply_markup=kb)

            # next_id = msg.message_id

            # async with state.proxy() as data:
            #     data['prev_msg_id'] = next_id  
                
    #            await message.a(media=media, reply_markup=kb)
                # await message.edit_media(media=photo, caption=text, reply_markup=kb)
