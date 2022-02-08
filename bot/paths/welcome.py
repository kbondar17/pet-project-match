import logging
# from loguru import logger
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.loader import get_logger, dp
from db.db_funs import repo

logger = get_logger(f'my_log-{__name__}')


main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🔍 Искать!'),
                                           KeyboardButton(text='📝 Мой профиль')],
                                          [KeyboardButton(text='❤️ Взаимные лайки'),
                                          KeyboardButton(text='❓ О проекте')],
                                          ], row_width=2
                                )

welcome_text = 'Это Pet Project Match! Найди себе напарника для пет-проекта. Коротко расскажи о себе и своем проекте. И выбирай!'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """первое сообщение"""
    user_id = message.from_user.id
    user_name = message.from_user.username
    repo.add_user(user_id)
    repo.set_username(uid=user_id, name=user_name)

    logger.debug('юзер %s нажал на старт', message.from_user.id)
    await message.answer(text=welcome_text, reply_markup=main_menu)
    

@dp.callback_query_handler(text_contains='back_to_start')
async def start_2(call: types.CallbackQuery):

    await call.message.answer(text=welcome_text, reply_markup=main_menu)


# @dp.message_handler(text_contains='О боте')
# async def start(message: types.Message):
#     await message.answer(text=welcome_text, reply_markup=main_menu, parse_mode='Markdown')
