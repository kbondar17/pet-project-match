from aiogram import types
from aiogram.types import KeyboardButton, InlineKeyboardMarkup

from db.db_funs import repo
from bot.loader import dp, ya_disk, bot

@dp.callback_query_handler(text_contains='like')
async def like(call: types.CallbackQuery):
    '''
    v. добавить в лайки
    v. проверка на взаимность
 
    '''
    user_id = call.from_user.id
    who_was_liked = int(call.data.split('#')[-1])
    repo.add_to_liked(user_id, who_was_liked)
    mutual = repo.if_mutual_like(user_id, who_was_liked)

    if mutual:
        await call.message.answer('О Вау! Это взаимно!')
        await call.message.answer(f'Напиши {repo.get_username(who_was_liked)}!')

        # отправляем уведомление другому лайкнутому
        user_who_liked_info = repo.generate_card_for_user(uid=user_id)

        text = user_who_liked_info.self_description
        photo = user_who_liked_info.profile_pic
        name = user_who_liked_info.name

        if not photo:
            await bot.send_message(f'*Тебя лакнули!*', chat_id=who_was_liked)
        
            await bot.send_message(f'\n\n{name}\n\n{text}', chat_id=who_was_liked)
        
        else:
            photo = ya_disk.get_user_photo_link(user_id=user_who_liked_info.uid)
            
            await bot.send_photo(caption=f'Тебя лайкнули!\n\n{name}\n\n{text}', 
            chat_id=who_was_liked, photo=photo)


    user_card = repo.generate_card_for_user(call.from_user.id)
    
    if not user_card:
        await call.message.answer('Новых профилей нет. Приходи попозже!')

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
            await call.message.edit_text(text=text, reply_markup=kb)
        
        else:
            photo = ya_disk.get_user_photo_link(user_id=user_card.uid)
            await call.message.answer_photo(photo=photo, caption=text, reply_markup=kb)



