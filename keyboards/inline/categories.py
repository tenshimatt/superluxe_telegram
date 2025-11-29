from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

category_cb = CallbackData('category', 'id', 'action')


def categories_markup():
    from loader import db

    global category_cb

    markup = InlineKeyboardMarkup()
    for idx, title in db.fetchall('SELECT * FROM categories'):
        markup.row(InlineKeyboardButton(title, callback_data=category_cb.new(id=idx, action='view'), pay=False))

    return markup
