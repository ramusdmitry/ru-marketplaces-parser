from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from app.constants import SUPPORT_BTN, SEARCH_BTN, MENU_PLACEHOLDER

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=SEARCH_BTN, command='url')],
    [KeyboardButton(text=SUPPORT_BTN)],
],
    resize_keyboard=True,
    input_field_placeholder=MENU_PLACEHOLDER)


def buy_btn(url):
    btn = InlineKeyboardButton(text="🛒 Купить", url=url, callback_data="buy_btn_menu")
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])
