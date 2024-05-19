from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.keyboards as kb


class GetUrl(StatesGroup):
    url = State()
    answer = State()


router = Router()


async def google_search(query):
    # Функция имитация работы парсера
    base_url = "https://www.google.com/search?q="
    search_url = base_url + query.replace(' ', '+')
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
async def get_help(message: Message):
    await message.answer(
        'Данный бот создан для того, чтобы парсить маркетплейсы '
        'и находить товар по наилучшей цене. Если возникли '
        'какие-либо ошибки или что-то сломалось, напишите '
        'в наш чат поддержки:'
        ' https://t.me/bot_support_ru_marketplaces.\n'
    )


@router.message(F.text == 'Поиск')
async def url_one(message: Message, state: FSMContext):
    await state.set_state(GetUrl.url)
    await message.answer('Вставь ссылку на интересующий тебя товар')


@router.message(GetUrl.url)
async def url_two(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(GetUrl.answer)
    url_data = await state.get_data()

    await message.answer(f'Я приступил к поиску товара:\n{url_data["url"]}, ожидайте')
    search_url = await google_search(url_data["url"])
    await message.answer(search_url)

    await message.answer(
        'Я готов искать следующий товар для тебя, '
        'просто введи что необходимо найти!'
    )
    await state.set_state(GetUrl.url)
