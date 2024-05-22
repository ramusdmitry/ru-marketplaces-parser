import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from parser.yandex import YandexParser
from parser.wb import WBParser
from storage import crud, db


# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Функция для многопоточного парсинга
async def multi_threaded_parsing(urls, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(parse_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                if data:
                    results.append(data)
            except Exception as e:
                logging.error(f"Error occurred for URL {url}: {e}")
    return results

# Функция для парсинга одного URL
async def parse_url(url):
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
        return {"error": "Ссылка не поддерживается"}

    try:
        return parser.get_product_info()
    except Exception as e:
        logging.error(f"Error occurred while parsing URL {url}: {e}")
        return {"error": str(e)}

# Пример использования
if __name__ == "__main__":
    current_session = db.session
    urls = crud.get_urls(current_session)

    parsed_data = multi_threaded_parsing(urls, max_workers=5)
    for data in parsed_data:
        print(data)

#result = parse_url('https://ozon.ru/t/AZBbw8w')
#print(result)