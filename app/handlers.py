from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import parser
from worker.worker import parse_url



class GetUrl(StatesGroup):
    support = State()
    url = State()
    answer = State()
    urls = State()
    answers = State()


router = Router()


# Функция имитация работы парсера
async def google_search(query):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + query.replace(' ', '+')
    print(search_url)
    return search_url

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAU0w0mYWtHnC-TwVZCJ4qpIb780YyrlVAAIpAQACFkJrCqxwmND03X3YNAQ')
    await message.answer(
        'Привет! Я бот, который поможет тебе найти товар на '
        'маркетплейсе по лучшей цене!\nДля поиска нажми на кнопку поиск',
        reply_markup=kb.main
    )


@router.message(F.text == 'Поддержка')
async def get_help(message: Message, state: FSMContext):
    await state.set_state(GetUrl.support)
    await message.answer(
        'Данный бот создан для того, чтобы парсить маркетплейсы '
        'и находить товар по наилучшей цене. Если возникли '
        'какие-либо ошибки или что-то сломалось, напишите '
        'в наш чат поддержки:'
        ' https://t.me/bot_support_ru_marketplaces.\n'
    )
    await state.clear()


@router.message(F.text == 'Поиск')
async def url_one(message: Message, state: FSMContext):
    await state.set_state(GetUrl.url)
    await message.answer('Вставь ссылку на интересующий тебя товар')


@router.message(GetUrl.url)
async def url_two(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(GetUrl.answer)
    url_data = await state.get_data()
    await message.answer(f'Я приступил к поиску товара:\n{url_data["url"]},\nЭто займет какое-то время')

    #search_url = await google_search(url_data["url"])
    #await message.answer(search_url)

    search_url = await parse_url(url_data["url"])
    await message.answer(parser.get_product_info())

    await message.answer(
        'Я готов искать следующий товар для тебя!\n'
    )
    await state.set_state(GetUrl.url)

@router.message(F.text)
async def no_mode_selected(message: Message):
    await message.answer('Нажми кнопку Поиск')