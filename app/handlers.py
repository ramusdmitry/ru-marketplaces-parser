from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.constants import *
from worker.worker import parse_url
from aiogram.enums import ParseMode
import app.keyboards as kb


class GetUrl(StatesGroup):
    support = State()
    url = State()
    answer = State()
    urls = State()
    answers = State()


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_sticker(WELCOME_STICKER)
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=kb.main,
        parse_mode=ParseMode.HTML
    )


@router.message(F.text == SUPPORT_BTN)
async def get_help(message: Message, state: FSMContext):
    await state.set_state(GetUrl.support)
    await message.answer(SUPPORT_MESSAGE)
    await state.clear()


@router.message(F.text == SEARCH_BTN)
async def url_one(message: Message, state: FSMContext):
    await state.set_state(GetUrl.url)
    await message.answer('Вставь ссылку на товар, который необходимо найти')


def pretty_msg(data: dict) -> str:
    messages = {
        "🏷️ <b>Название</b>": data.get('title', '-'),
        # "🛒 <b>Товар</b>": f"<a href='{data.get('url', '')}'>ссылка</a>",
        "💰 <b>Оригинальная цена</b>": f"{data.get('original_price', 0)}₽",
        "🔥 <b>Цена со скидкой</b>": f"{data.get('discount_price', 0)}₽",
        "😱 <b>Специальная цена</b>": f"{data.get('special_price', 0)}₽",
        "🎯 <b>Скидка</b>": f"{data.get('discount_percent', 0)}%"
    }
    return '\n'.join(f'{k}: {v}' for k, v in messages.items())


def validate_url(url: str) -> bool:
    if 'wildberries.ru' in url or 'market.yandex.ru' in url:
        return True
    return False


@router.message(GetUrl.url)
async def url_two(message: Message, state: FSMContext):
    if not validate_url(message.text):
        await message.answer(UNKNOWN_URL, ParseMode.HTML)
        return
    await state.update_data(url=message.text)
    await state.set_state(GetUrl.answer)
    state_data = await state.get_data()
    await message.answer(WAITING_MESSAGE)

    try:
        result = await parse_url(state_data["url"])
        if isinstance(result, dict):
            if all(value == -1 for value in
                   [result.get("discount_price"), result.get("special_price"), result.get("discount_percent")]):
                await message.answer(FAILED_MESSAGE)
            else:
                result_str = pretty_msg(result)
                image_url = result.get('image_url')
                if image_url:
                    await message.answer_photo(photo=image_url, caption=result_str, parse_mode=ParseMode.HTML,
                                               reply_markup=kb.buy_btn(state_data['url']))
                else:
                    await message.answer(result_str, parse_mode=ParseMode.HTML,
                                         reply_markup=kb.buy_btn(state_data['url']))
        else:
            await message.answer(result)

        await message.answer('Я готов искать следующий товар для тебя!\n')
        await state.set_state(GetUrl.url)
    except Exception as e:
        await message.answer(f"Произошла ошибка при парсинге URL: {e}")
        await state.set_state(GetUrl.url)


@router.message(F.text)
async def no_mode_selected(message: Message):
    await message.answer(UNKNOWN_CMD)
