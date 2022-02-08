from aiogram.types import InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator

from db.db_funs import repo


def generate_kb_with_users_likes(uid, page=1):

    mutual_likes_ids = repo.show_users_mutual_likes(uid)
    if not mutual_likes_ids:
        return False, False

    liked_users_cards = [repo.get_user_info(uid=uid) for uid in mutual_likes_ids]
    current_user = liked_users_cards[page-1]
    


    paginator = InlineKeyboardPaginator( 
        page_count=len(liked_users_cards),
        current_page=page,
        data_pattern='mutual#{page}'
    )
    paginator.add_after(
        InlineKeyboardButton('< Назад', callback_data='back_to_start'),
    )   
    
    return current_user, paginator.markup
