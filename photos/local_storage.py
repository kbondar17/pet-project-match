import asyncio
from functools import lru_cache
import json

from aiocache import cached
from aiocache.serializers import PickleSerializer


    
@lru_cache
def get_user_photo(uid):
    with open('photos/cached_photos.json', 'r') as f:
        data = json.load(f)
        print('enterted function, no cache')
        return [e for e in data if e['user_id'] == uid][0]['photo']['href']


