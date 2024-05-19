from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поиск', command='url')],
    [KeyboardButton(text='Поддержка')]
],
                            resize_keyboard=True,
                            input_field_placeholder='Выберите пункт меню.')
