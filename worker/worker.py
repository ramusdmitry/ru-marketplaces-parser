import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

from app.keyboards import buy_btn
from parser.yandex import YandexParser
from parser.wb import WBParser
from storage import crud, db
from aiogram import Bot

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Функция для многопоточного парсинга
async def multi_threaded_parsing(urls, user_ids, bot, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, parse_url, url, user_id, bot) for url, user_id in zip(urls, user_ids)]
        for response in await asyncio.gather(*futures):
            results.append(response)
    return results

# Функция для парсинга одного URL
def parse_url(url, user_id, bot):
    if not url.strip():
        logging.error(f"Empty URL provided: {url}")
        return {"error": "Empty URL provided"}

    parser = None
    if 'yandex' in url:
        parser = YandexParser(url)
    elif 'wildberries' in url:
        parser = WBParser(url)
    else:
        logging.error(f"Unsupported URL provided: {url}")
        return {"error": "Unsupported URL provided"}

    try:
        result = parser.get_product_info()
        notify_user = save_and_check_changes(result, user_id, bot)
        if notify_user:
            send_result_to_user(result, user_id, bot)
        return result
    except Exception as e:
        logging.error(f"Error occurred while parsing URL {url}: {e}")
        return {"error": str(e)}

def save_and_check_changes(result, user_id, bot):
    session = db.session
    try:
        return crud.add_or_update_product(session=session, user_id=user_id,
                                          title=result['title'], description=result['description'],
                                          url=result['url'],
                                          original_price=result['original_price'], discount_price=result['discount_price'], special_price=result['special_price'],
                                          discount_percent=result['discount_percent'])
    except Exception as e:
        logging.error(f"Error occurred while saving parsed data: {e}")
        return False

def send_result_to_user(result, user_id, bot):
    loop = asyncio.get_event_loop()
    loop.create_task(send_message(result, user_id, bot))

async def send_message(result, user_id, bot):
    result_str = pretty_msg(result)
    image_url = result.get('image_url')
    if image_url:
        await bot.send_photo(chat_id=user_id, photo=image_url, caption=result_str, parse_mode='HTML', reply_markup=buy_btn(result.get('url')))
    else:
        await bot.send_message(chat_id=user_id, text=result_str, parse_mode='HTML', reply_markup=buy_btn(result.get('url')))

def pretty_msg(data: dict) -> str:
    messages = {
        "🏷️ <b>Название</b>": data.get('title', '-'),
        "💰 <b>Оригинальная цена</b>": f"{data.get('original_price', 0)}₽",
        "🔥 <b>Цена со скидкой</b>": f"{data.get('discount_price', 0)}₽",
        "😱 <b>Специальная цена</b>": f"{data.get('special_price', 0)}₽",
        "🎯 <b>Скидка</b>": f"{data.get('discount_percent', 0)}%"
    }
    return '\n'.join(f'{k}: {v}' for k, v in messages.items())

async def periodic_parsing(bot, interval=3600):
    while True:
        current_session = db.session
        products = crud.get_products(current_session)
        urls = [p.url for p in products]
        user_ids = [p.user_id for p in products]
        await multi_threaded_parsing(urls, user_ids, bot, max_workers=5)
        await asyncio.sleep(interval)

async def periodic_advertising(bot, interval=300):
    while True:
        current_session = db.session
        users = crud.get_users(current_session)
        for user in users:
            await bot.send_message(chat_id=user.user_id, text="📢 Здесь могла быть ваша реклама")
        await asyncio.sleep(interval)