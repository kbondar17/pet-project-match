# постоянно спрашивает о новых фотках 
# если новая -> хешировать
# раз в час обновляет ссылку 
import json
import time
import asyncio

from bot.loader import ya_disk
from bot.my_logger import get_logger

logger = get_logger(f'my_log-{__name__}')


class LocalCacher:

    # 2 обновлятор

    def __init__(self, local_file):
        self.local_file = local_file


    local_data = []
    cloud_data = []

    def load_local_data(self):
        with open(self.local_file, 'r') as f:
            self.local_data = json.load(f)
            
    def get_cloud_data(self):
        self.cloud_data = ya_disk.get_all_user_ids()["_embedded"]['items']
         

    def add_new_to_local(self):
        existig_ids = [e['user_id'] for e in self.local_data]
        ids_on_cloud = [int(e['name']) for e in self.cloud_data]
        ids_on_cloud_only = list(set(ids_on_cloud).difference(existig_ids))

        if not ids_on_cloud_only:
            logger.debug('новых фоток на облаке нет!')
            return

        logger.debug('Нашли на облаке новые фотки: %s', ids_on_cloud_only)

        for ids_ in ids_on_cloud_only:
            href = ya_disk.get_user_photo_link(ids_)
            if href:
                new_row = {
                    "user_id":ids_,
                    "photo":{"href":href,
                    "method":"GET"
                    }
                }
                self.local_data.append(new_row)
        
        with open(self.local_file, 'w') as outfile:
            json.dump(self.local_data, outfile)

            logger.debug('Добавили в локальный файл фоток')


    async def add_new_from_cloud_to_local(self):
        # добавляет новые фотки из облака в локальных json 
        while True:
            print('зашли в add_new_from_cloud_to_local')
            self.load_local_data()
            self.get_cloud_data()
            self.add_new_to_local()
            await asyncio.sleep(60)

    # def start_add_new_from_cloud_to_local(self):
    #     while True:
    #         asyncio.run(self.add_new_from_cloud_to_local())
            
# должен работать постоянно. 
# cache = LocalCacher('photos/cached_photos.json')
# cache.add_new_from_cloud_to_local()


# cache.load_local_data()
# print(cache.local_data)
# print(type(cache.local_data))
# cache.get_cloud_data()

