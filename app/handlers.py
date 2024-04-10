from aiogram import F, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я бот, который поможет тебе найти товар на '
                         'маркетплейсе по лучшей цене! Если что-то не понятно'
                         ' отправь мне команду /help. Введи название товара'
                         ' который тебя интересует')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Данный бот создан для того, чтобы парсить маркетплейсы'
                         ' и находить товар по наилучшей цене. Если возникли'
                         ' какие-либо ошибки или что-то сломалась напишите'
                         ' в наш чат поддержки : +_______+. Для поиска просто введи название товара который тебя интересует!')


@router.message(F.text != '/help')
async def name_of_product(message: Message):
    await message.answer('Я приступил к поиску и сравнению товаров, скоро я'
                         ' пришлю тебе ссылку на лучшее предложение!')

