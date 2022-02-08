from photos.cache_updater import LocalCacher
from bot.loader import ya_disk # TODO сделать так чтобы Storage был в лоударе

class Storage():
    cloud = ya_disk()
    local = LocalCacher(local_file='photos/cached_photos.json')

    # и вот здесь как раз подошел бы кэш! 
    
    def get_photo(self, uid):
        '''единый метод'''
        # смотрю локально
        # если нет - иду в облако
        pass

    def local_links_updater(self):
        print('')    
        



    # РАБОТАЕТ ДОБАВЛЕНИЕ НОВЫХ ФОТОГРАФИЙ ИЗ ОБЛАКА В ЛОКАЛ
    # НУЖНО СДЕЛАТЬ ОБНОВЛЕНИЕ ЛОКАЛЬНЫХ ССЫЛОК
    # фор сам ризн фотки кешированы.


