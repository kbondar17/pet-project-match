import random

from sqlalchemy import text
from db.session import db_session
from sqlalchemy.exc import IntegrityError
from db.models import User, WhoSeenWho, WhoLikedWho

from bot.my_logger import get_logger 
logger = get_logger(f'my_log-{__name__}')

import logging
logger = logging.getLogger(__name__)

class db_funs:

    def add_user(self, u_id):
        user = db_session.query(User).filter_by(uid=u_id).count()
        logger.info(f'юзер {u_id} уже есть!')
    
        if not user:
            user = User(uid=u_id)
            db_session.add(user)
            db_session.commit()
            logger.info(f'добавили юзера {u_id} в БД!')
    
    def delete_user(self, uid):
        user = db_session.query(User).filter_by(uid=uid)
        if not user:
            raise ValueError('Нет такого юзера!')
        user.delete()


    def update_photo(self, u_id):
        user = db_session.query(User).filter_by(uid=u_id).first()
        user.profile_pic = True
        db_session.commit()
    


    def self_describe(self, u_id, descr):
        user = db_session.query(User).filter_by(uid=u_id).first()
        if not user:
            raise ValueError('Нет такого юзера!')

        user.self_description = descr
        db_session.commit()
        logger.debug('поменяли описание себя на')
        print(user.self_description)
        return True

    def get_self_description(self, uid):
        user = db_session.query(User).filter_by(uid=uid).first()
        if not user:
            raise ValueError('Нет такого юзера!')
        return user.self_description


    def project_describe(self, u_id, descr):
        user = db_session.query(User).filter_by(uid=u_id).first()
        if not user:
            raise ValueError('Нет такого юзера!')

        user.project_description = descr
        db_session.commit()
        logger.debug('поменяли описание проекта на')
        print(user.project_description)
        return True

    def generate_card_for_user(self, uid) -> User:
        '''
        генерирует для пользователя карточку юзеру, которого он еще не видел
        1. айди юзера (для колбека)
        2. описание
        3. фотка 
         
        '''
        user = db_session.query(User).filter_by(uid=uid).first()
        
        if not user:
            raise ValueError('Нет такого юзера!')
            
        has_seen = [e[0] for e in db_session.query(WhoSeenWho.seen_who).filter_by(who=uid).all()]

        for user_info in db_session.query(User).all():
            
            if user_info.uid not in has_seen and user_info.self_description:                
                
                new_who_seen_who = WhoSeenWho(who=user.uid, seen_who=user_info.uid)
                db_session.add(new_who_seen_who)
                db_session.commit()
                return user_info
        
        logger.debug(f'Юзер {uid} видел всех!')
        return False

    def get_user_info(self, uid) -> User:
        'отдает карточку с инфой про юзера'
        user = db_session.query(User).filter_by(uid=uid).first()
        
        if not user:
            raise ValueError('Нет такого юзера!')
        
        return user



    def add_to_liked(self, user_id, liked_user_id):
        user = db_session.query(User).filter_by(uid=user_id).first()
        
        if not user:
            raise ValueError('Нет такого юзера!')

        try:
            new_liked = WhoLikedWho(who=user_id, liked_who=liked_user_id)
            db_session.add(new_liked)
            db_session.commit()
            logger.debug(f'добавили {liked_user_id} в лайки юзеру {user_id}')
            return True
        except IntegrityError as ex:
            db_session.rollback()
            logger.warning('ЮЗЕР УЖЕ В ЛАЙКАХ---')
            print(ex)
            print('----')

    def if_mutual_like(self, user_id, liked_user) -> bool:
        '''проверяет лайки лайкнутого человека. если юзер в них есть - True'''
        user = db_session.query(User).filter_by(uid=user_id).first()
        
        if not user:
            raise ValueError('Нет такого юзера!')

        likes_of_liked_user = db_session.query(WhoLikedWho).filter_by(who=liked_user).all()
        
        likes_of_liked_user = [e.liked_who for e in likes_of_liked_user]

        if user_id in likes_of_liked_user:
            return True

    def get_not_notificated_likes(self, user_id):
        likes = WhoLikedWho(liked_who=user_id, liked_person_notificated)



    def set_username(self, uid, name):
        user = db_session.query(User).filter_by(uid=uid).first()
        
        if not user:
            raise ValueError('Нет такого юзера!')        
        
        user.user_name=name
        db_session.commit()

    def get_username(self, uid):
        user = db_session.query(User).filter_by(uid=uid).first()
        
        if not user:
            raise ValueError('Нет такого юзера!')

        return user.user_name

    def show_users_mutual_likes(self, uid) -> list[int]:
        user = db_session.query(User).filter_by(uid=uid).first()
        
        if not user:
            raise ValueError('Нет такого юзера!')
        
        mutual = db_session.execute(text(f'''SELECT DISTINCT t1.who, t1.liked_who
                FROM who_liked_who t1
                INNER JOIN who_liked_who t2 
                    ON t1.who = t2.liked_who 
                    AND t1.liked_who = t2.who where t1.who = {uid};'''))
        
        return [e[1] for e in mutual]  

    



from sqlalchemy.engine.cursor import CursorResult

repo = db_funs()
# print(repo.show_users_mutual_likes(106441967))
# import random
# import requests

# word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

# response = requests.get(word_site).content.decode()
# WORDS = response.splitlines()


# for id_ in range(1, 51):

#     repo.set_username(id_, f'@{random.choice(WORDS)}' )
#     #user = db_session.query(User).filter_by(uid=uid).first()
    
#     try:
#         new = WhoLikedWho(who=id_, liked_who=106441967)
#         print('new---',new)
#         db_session.add(new)
#         db_session.commit()

#     except Exception as ex:
#         db_session.rollback()
#         print(ex)
        



# repo.if_mutual_like(1, 106441967)
# user = db_session.query(User).filter_by(uid=106441967).first()
# who_seen_who = WhoSeenWho(who=user.uid, seen_who=2)
# db_session.add(who_seen_who)
# db_session.commit()
#try:

#for id_ in range(1, 51):
# user = db_session.query(User).filter_by(uid=106441967).first()
# user.name = 'Кирилл'
# db_session.commit()
