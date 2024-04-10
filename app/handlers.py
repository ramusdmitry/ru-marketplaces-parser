from aiogram import F, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message

router = Router()

product_name = None  # переменная для сохранения названия товара
processing = False  # переменная для отслеживания состояния обработки


async def google_search(query): #Функция иммитация работы парсера
    base_url = "https://www.google.com/search?q="
    search_url = base_url + query.replace(' ', '+')  # заменяем пробелы на '+'
    return search_url


@router.message(CommandStart())
async def cmd_start(message: Message):
    global processing
    if processing:
        await message.answer('Я все еще обрабатываю твой предыдущий запрос. Пожалуйста, подожди.')
    else:
        await message.answer_sticker('CAACAgIAAxkBAU0w0mYWtHnC-TwVZCJ4qpIb780YyrlVAAIpAQACFkJrCqxwmND03X3YNAQ')
        await message.answer('Привет! Я бот, который поможет тебе найти товар на '
                             'маркетплейсе по лучшей цене! Если что-то не понятно '
                             'или хочешь обратиться в службу поддержики'
                             ' отправь мне команду /help. \nДля поиска просто'
                             ' введи название товара который тебя интересует!')


@router.message(Command('help'))
async def get_help(message: Message):
    global processing
    if processing:
        await message.answer('Я все еще обрабатываю твой предыдущий запрос. Пожалуйста, подожди.')
    else:
        await message.answer('Данный бот создан для того, чтобы парсить маркетплейсы'
                             ' и находить товар по наилучшей цене. Если возникли'
                             ' какие-либо ошибки или что-то сломалась напишите'
                             ' в наш чат поддержки : @support_test. \nДля поиска просто'
                             ' введи название товара который тебя интересует!')


@router.message(F.text != '/help')
async def name_of_product(message: Message):
    global product_name
    global processing
    if processing:
        await message.answer('Я все еще обрабатываю твой предыдущий запрос. Пожалуйста, подожди.')
    else:
        processing = True
        product_name = message.text  # сохраняем название товара в переменную
        print(product_name)  # Выводим в консоль название товара для поиска(нужно для тестов)
        await message.answer('Я приступил к поиску и сравнению товаров, скоро я'
                             ' пришлю тебе ссылку на лучшее предложение!')

        search_url = await google_search(product_name)
        await message.answer(search_url)

        await message.answer('Я готов искать следующий товар для тебя,'
                             ' просто введи что необходимо найти!')

        processing = False
