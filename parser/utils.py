import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver(url: str = "", app_mode: str = "debug"):
    options = Options()
    if app_mode == "debug":
        options.add_argument("--start-maximized")
    else:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    if url:
        driver.get(url)
    return driver


def is_captcha_displayed(url: str):
    logging.debug(f"Найдена капча у {url}. Закрываю процесс")
    if "captcha" in url:
        return True
    return False
