from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from worker.worker import parse_url
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
    await message.answer_sticker('CAACAgIAAxkBAU0w0mYWtHnC-TwVZCJ4qpIb780YyrlVAAIpAQACFkJrCqxwmND03X3YNAQ')
    await message.answer(
        'Привет! Я бот, который поможет тебе найти товар на '
        'маркетплейсе по лучшей цене!\nДля парсинга нажми на кнопку поиск',
        reply_markup=kb.main
    )


@router.message(F.text == 'Поддержка')
async def get_help(message: Message, state: FSMContext):
    await state.set_state(GetUrl.support)
    await message.answer(
        'Данный бот создан для того, чтобы парсить маркетплейсы ЯМаркет, WB '
        'и находить товар по наилучшей цене. Если возникли '
        'какие-либо ошибки или что-то сломалось, напишите '
        'в наш чат поддержки:'
        ' https://t.me/bot_support_ru_marketplaces.\n'
    )
    await state.clear()


@router.message(F.text == 'Поиск')
async def url_one(message: Message, state: FSMContext):
    await state.set_state(GetUrl.url)
    await message.answer('Вставь ссылку на товар, который необходимо найти')



@router.message(GetUrl.url)
async def url_two(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(GetUrl.answer)
    url_data = await state.get_data()
    await message.answer(f'Я приступил к поиску товара!\nЭто займет какое-то время')

    result = await parse_url(url_data["url"])
    if isinstance(result, dict):
        # Создаем словарь для перевода
        translation_dict = {
            "title": "Название",
            "description": "Описание",
            "url": "Ссылка на товар",
            "original_price": "Оригинальная цена",
            "discount_price": "Цена со скидкой",
            "special_price": "Специальная цена",
            "discount_percent": "Скидка"
        }
        # Проверяем наличие -1 в значениях
        if all(value == -1 for value in
               [result.get("discount_price"), result.get("special_price"), result.get("discount_percent")]):
            await message.answer('Ошибка парсинга из-за капчи.')
        else:
            # Удаляем ключи со значением -1
            result = {k: v for k, v in result.items() if v != -1}

            # Переводим ключи на русский и обновляем форматирование ссылок
            result_translated = {}
            for k, v in result.items():
                if k in translation_dict:
                    if k == "url":
                        result_translated[translation_dict[k]] = f"<a href='{v}'>тык</a>"
                    elif k == "description" and v.strip() != "":
                        result_translated[translation_dict[k]] = v
                    elif k != "description":
                        result_translated[translation_dict[k]] = v
                else:
                    result_translated[k] = v

            for key in ["Оригинальная цена", "Цена со скидкой", "Специальная цена"]:
                if key in result_translated:
                    result_translated[key] = f"{result_translated[key]} ₽"
            if "Скидка" in result_translated:
                result_translated["Скидка"] = f"{result_translated['Скидка']}%"
            result_str = '\n'.join(f'{k}: {v}' for k, v in result_translated.items())
            await message.answer(result_str, parse_mode='HTML')
    else:
        await message.answer(result)

    await message.answer(
        'Я готов искать следующий товар для тебя!\n'
    )
    await state.set_state(GetUrl.url)



@router.message(F.text)
async def no_mode_selected(message: Message):
    await message.answer('Нажми кнопку Поиск')
