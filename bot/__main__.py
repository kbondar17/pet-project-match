import asyncio

from bot.loader import bot, dp, get_logger, cache_updater
from aiogram import executor
from bot.paths import dp



logger = get_logger(f'my_log-{__name__}')



if __name__ == '__main__': 


    loop = asyncio.get_event_loop()
    loop.create_task(cache_updater.add_new_from_cloud_to_local())
    loop.create_task(task())

    executor.start_polling(dp)
