from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import app.keyboards as kb
from app.constants import *
from worker.worker import parse_url, send_message, pretty_msg
from storage import crud, db

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

from aiogram import Bot
@router.message(GetUrl.url)
async def url_two(message: Message, state: FSMContext, bot: Bot):
    url = message.text
    user_id = message.from_user.id
    await state.update_data(url=url)
    await state.set_state(GetUrl.answer)
    await message.answer(WAITING_MESSAGE)

    try:
        result = parse_url(url, user_id, bot)
        if isinstance(result, dict):
            if all(value == -1 for value in
                   [result.get("discount_price"), result.get("special_price"), result.get("discount_percent")]):
                await message.answer(FAILED_MESSAGE)
            else:
                result_str = pretty_msg(result)
                image_url = result.get('image_url')
                # Сохранение данных в базу данных
                notify_user = crud.add_or_update_product(session=db.session,
                                                         user_id=user_id,
                                                         title=result.get('title', ''),
                                                         description=result.get('description', ''),
                                                         image_url=image_url,
                                                         url=url,
                                                         original_price=result.get('original_price', 0),
                                                         discount_price=result.get('discount_price', 0),
                                                         special_price=result.get('special_price', 0),
                                                         discount_percent=result.get('discount_percent', 0.0))
                if notify_user:
                    await send_message(result, user_id, bot)
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
