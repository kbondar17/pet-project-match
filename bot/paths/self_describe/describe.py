from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

from db.db_funs import repo
from bot.loader import dp, ya_disk
from aiogram.dispatcher import FSMContext
from bot.paths.my_states import My_states

cancel_kb = InlineKeyboardMarkup(
inline_keyboard=[
    [InlineKeyboardButton(
        text='Отменить', callback_data='back_to_start')],

    ]
    )   

kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Данные о себе', callback_data='edit_self')],
            [InlineKeyboardButton(
            text='Описание проекта', callback_data='edit_project')],
        [InlineKeyboardButton(
            text='< Назад', callback_data='back_to_start')],

    ]

)

change_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Изменить текст или фотографию', callback_data='change_info')],
        [InlineKeyboardButton(
            text='❌ Удалить профиль ❌', callback_data='delete_profile')],

        ]
    )   



@dp.message_handler(text_contains='Мой профиль')
async def change_bio(message: types.Message):



    chat_id = message.from_user.id

    text = repo.get_self_description(uid=chat_id)
    photo = ya_disk.get_user_photo_link(chat_id)



    if not text:
        await message.answer('👇🏻 Отправь описание в сообщении! 👇🏻', reply_markup=cancel_kb)

    else:        
        await message.answer('Вот как другие видят тебя при поиске')
        
        if not photo:
            await message.answer(text=text, reply_markup=change_kb)

            # await message.answer('👇🏻 Классное описание! Можешь прислать фотографию - добавим 👇🏻',
            #     reply_markup=kb)

        else:
            await message.answer_photo(caption=text, photo=photo, reply_markup=change_kb)

            # await message.answer(text='👇🏻 Отправь новое описание или фотографию 👇🏻', reply_markup=kb)
        


@dp.callback_query_handler(text='change_info')
async def change_info(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text='👇🏻 Отправь новое описание или фотографию 👇🏻', reply_markup=cancel_kb)
    await My_states.sending_photo_or_text.set()


@dp.message_handler(state=My_states.sending_photo_or_text, content_types=["photo"])
async def get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    chat_id = message.from_user.id
    
    ya_disk.upload_via_tg(chat_id=chat_id, file_id=photo_id)
    await message.answer('Отлично! Фотку поменяли, теперь вот так')
    await state.reset_state()

    repo.update_photo(chat_id)
    
    text = repo.get_self_description(uid=chat_id)
    photo = ya_disk.get_user_photo_link(chat_id)

    if photo: 
        await message.answer_photo(caption=text, photo=photo)
    else:
        await message.answer(text=text)



@dp.message_handler(state=My_states.sending_photo_or_text)
async def get_text(message: types.Message, state: FSMContext):
    text = message.text
    u_id = message.from_user.id
    if text in ['🔍 Искать!', '📝 Мой профиль']:
        await message.answer('Нажми еще раз, плз')
        await state.reset_state()
    else:
        repo.self_describe(message.from_user.id, message.text)
        await message.answer('Поменяли описание! Теперь вот так:')
        await state.reset_state()

        text = repo.get_self_description(uid=u_id)
        photo = ya_disk.get_user_photo_link(u_id)

        if photo: 
            await message.answer_photo(caption=text, photo=photo, reply_markup=change_kb)
        else:
            await message.answer(text=text, reply_markup=change_kb)
            

@dp.callback_query_handler(state=My_states.sending_photo_or_text)
async def get_back(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    kb = InlineKeyboardMarkup(inline_keyboard=[[KeyboardButton(text='Да!', callback_data='swiping')]])

    await call.message.answer('Идем искать напарника?', reply_markup=kb)
    # user_id = message.from_user.id
    # user_name = message.from_user.username
    # #api_client.users.add_user(uid=user_id, name=user_name)
    # await message.answer(text=welcome_text, reply_markup=main_menu)
    # repo.add_user(user_id)
    




