from dotenv import load_dotenv
import os
import logging
import logging.config
from yarl import URL

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


from photos.yandex_disk import YaDisk 
ya_disk = YaDisk()

from photos.cache_updater import LocalCacher
cache_updater = LocalCacher('photos/cached_photos.json')

from config import TOKEN

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def get_logger(name):
    logger = logging.getLogger(name)
    format = '%(filename)+13s %(name)s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(format))
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    return logger
    # logger.debug(f'logger {name} initialized!')


# get_logger('bot_log')
# logger = logging.getLogger('bot_log.main')
# logger.debug('logger works!')
logger = get_logger('ТЕЛЕГРАМ ЛОГЕР:')
dp.middleware.setup(LoggingMiddleware(logger))
print(logger.level)
print(logger.debug('сделали логер'))

# вот так инициализировать в других файлах
'''

from bot.loader import get_logger
logger = get_logger(f'my_log-{__name__}')

'''