import asyncio
import aiohttp
import os
import requests
import json
from pathlib import Path
import yadisk
#from bot.loader import get_logger
from db.db_funs import db_funs
import logging
logger = logging.getLogger(__name__) 
#get_logger(f'my_log-{__name__}')
import functools
from aiocache import cached
from aiocache.serializers import PickleSerializer



# @cached(serializer=PickleSerializer())
# async def async_main():
#     print("First ASYNC non cached call...")
#     await asyncio.sleep(1)


'''
API КЛЮЧ:

Идентификатор ключа:
ajeh000lmu25p0huc76k
Ваш секретный ключ:
AQVN0QABW3hFyCPmHNT2rFE2Adk2y3TQVH4op27k

СТАТИЧЕСКИЙ КЛЮЧ:
Идентификатор ключа:
_ZZuWh6iOtN9YZ-4YrOW
Ваш секретный ключ:
OAzUOqLaS-M21QlBf0Pvx0zJ8fWEruAzdvUTi0z6
Сохраните идентификатор и ключ. После закрытия диалога значение ключа будет недоступно.1


'''

class YaDisk():

    path = Path()

    BOT_TOKEN = '1700335109:AAFCfOWa3-9kvQHkK6AaZeLJlZNLqiCmZrQ'
    token = 'AQAAAABL994CAADLWzJds-SfVk9qnMMrTwmv9f4'
    down_load_url = 'https://cloud-api.yandex.net/v1/disk/resources/download'
    base_url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    headers = {'Accept': 'application/json', 
            'Authorization': f'OAuth {token}' }

    def _make_request(self, method, method_name, *args, **kwargs):
        response = getattr(requests, method)(
            'https://api.telegram.org/bot%s/%s' % (self.BOT_TOKEN, method_name),
            *args, **kwargs
        )
        return response.json()

    def _get_json(self, method_name, *args, **kwargs):
        return self._make_request('get', method_name, *args, **kwargs)


    def upload_via_link(self, user_id, file_link, file_name=''):
        headers = {'Accept': 'application/json', 
        'Authorization': f'OAuth {self.token}' }

        if not file_name:
            file_name='user_photo.jpg'

        params = {'path':f'users_pics/{user_id}/{file_name}',
                  'url':file_link}

        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        try:
            req = requests.post(url, headers=headers, params=params)
            req.raise_for_status()
            print()
        except requests.HTTPError as err:
            print(f'юзера {user_id} не получилось загрузить')


    def upload_via_tg(self, file_id, chat_id):
        
        # название фотографии в апи телеграма
        photo = self._get_json('getFile', params={"chat_id": chat_id, "file_id": file_id})
        file_path = photo['result']['file_path']
        file_format = file_path.split('.')[-1]
        print('file_format---',file_format)
        # скачали
        response = requests.get('https://api.telegram.org/file/bot%s/%s' % (self.BOT_TOKEN, file_path))

        
        # папка для сохранения локально
        local_folder = self.path / 'photos'
        # имя файла
        file_name = f'user_photo.{file_format}'
        # сохранили локально
        with open(local_folder/file_name, 'wb') as f:
            f.write(response.content)

        y = yadisk.YaDisk(token=self.token)
        logger.debug('token check --',y.check_token())

        destination_folder = f'users_pics/{chat_id}'        
        try:
            y.mkdir(destination_folder)
            logger.debug('создали папку %s ', destination_folder)
        except yadisk.exceptions.PathExistsError:
            logger.debug('папка юзера уже была')
        
        y.upload(str(local_folder/file_name), f'{destination_folder}/{file_name}', overwrite=True) 
        
        # стерли локальную
        os.remove(local_folder/file_name)

    def get_user_photo_link(self, user_id):
        # получить ссылку на фотку которую можно потом отправлять в сообщениии.
        # должен быть словарик
        # юзер зашел - надо сразу захешировать 17 карточек 
        # и получить список всех возможных карточек, чтобы хешировать их по ходу движения
          
        
        headers = {'Accept': 'application/json', 
        'Authorization': f'OAuth {self.token}' }
        params = {'path':f'users_pics/{user_id}/user_photo.jpg'}
        
        url = 'https://cloud-api.yandex.net/v1/disk/resources/download'
        try:
            req = requests.get(url, headers=headers, params=params)
            req.raise_for_status()
            return req.json()['href']
        except requests.HTTPError as ex:
            logger.warning('видимо у юзера нет фотки!')
            print(ex)

    def get_all_user_ids(self):
        url = self.base_url #+ 'files'
        params = {'path':'/users_pics', 'limit':'300'}
    
        res = requests.get(url, headers=self.headers, params=params)
        #print('URL--------',requests.get(url, headers=self.headers, params=params).url)
        res.raise_for_status()
        return res.json()



    def download_user_photo(user_id, download_path=''):
        
        y_disk = yadisk.YaDisk(token='AQAAAABL994CAADLWzJds-SfVk9qnMMrTwmv9f4')
        y_disk.download(src_path='users_pics/{user_id}/user_photo.jpg', path_or_file='downloaded.jpg')
        return 'ДОПИСАТЬ КУДА СОХРАНЯТЬ ФОТКУ'

    def print_path(self):
        print([x for x in self.path.iterdir() if x.is_dir()])


# CHAT_ID = 106441967

# y = yadisk.YaDisk(token='AQAAAABL994CAADLWzJds-SfVk9qnMMrTwmv9f4')
# y.download(src_path='users_pics/106441967/user_photo.jpg', path_or_file='downloaded.jpg')
# disk = YaDisk()
# import time
# users = (e for e in range(1,51))
# s = time.time()
# res = disk.get_all_users_photos_async(users)

# print(res)
# import json
# with open('photos/cached_photos.json', 'w', encoding='utf-8') as f:
#     json.dump(res, f, ensure_ascii=False, indent=4)
# print('TIME---', time.time() - s)
#y = yadisk.YaDisk(token='AQAAAABL994CAADLWzJds-SfVk9qnMMrTwmv9f4')
#print(disk.print_path())
# for e in range(1,51):
#     disk.upload_via_link(user_id=e, file_link='https://thispersondoesnotexist.com/image')
    # try:
    #     y.mkdir(f'/users_pics/{e}')
    # except:
    #     pass
# import yadisk
# y = yadisk.YaDisk(token='AQAAAABL994CAADLWzJds-SfVk9qnMMrTwmv9f4')
# y.mkdir('/users_pics')
# y.mkdir('another_test/more_test')