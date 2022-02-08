from aiogram import types

from bot.loader import dp, ya_disk



text = '''ФИО: Атнашев Тимофей Алексеевич
Возраст: 20
Факультет: Факультет компьютерных наук
Образовательная программа: Прикладная математика и информатика
Уровень образования: Бакалавриат, 4 курс
Научные направления: гуманитарные науки (ФГН), компьютерные науки (ФКН)
Исследовательские интересы / тема работы: Исследовательские интересы: Digital Humanities, NLP 

В прошлом году писал курсовую на тему "Анализ дневников о Революции 1917 года с помощью методов NLP", сейчас работаю над исследованием применения различных NER архитектур для корпуса дневников Прожито'''

@dp.message_handler()
async def start(message: types.Message):
    print(message.text)
    await message.answer('это эхо')
    await message.answer_photo(ya_disk.get_user_photo_link(message.from_user.id))
    print(ya_disk.get_user_photo_link(message.from_user.id))

    # await message.answer(f'{message.text} -- не понимаю. Воспользуйтесь командами из меню')
    # await message.answer_photo('https://downloader.disk.yandex.ru/disk/9c6e76fc523033a8e847f76b286f0254b3c46b9e2ff58e7a13a5e4b7d5139191/61f97f4c/BewswV3GeF-3uji9HuH-EcaldF5hPkL-fbFQ6pzwic4y4NZh2PlJrE1BbDPWpIOiXHmCLfYnSzqlaK5Jaif37w%3D%3D?uid=1274535426&filename=user_photo.jpg&disposition=attachment&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=1274535426&fsize=33362&hid=7c22551ff4bbddb1ece4698d713fbe9e&media_type=image&tknv=v2&etag=d4a5bacd1896e3ebc5e19d16f29bad1d',
    # caption=text)
