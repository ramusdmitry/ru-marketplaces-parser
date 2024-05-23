import logging
import random
import time

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


def random_delay(min_ms=500, max_ms=2500):
    """
    This function generates a random delay between the given minimum and maximum milliseconds.

    Args:
        min_ms (int, optional): The minimum delay in milliseconds (default is 500ms).
        max_ms (int, optional): The maximum delay in milliseconds (default is 2500ms).

    Returns:
        None: This function does not return a value; it simply pauses the program execution.
    """
    delay_seconds = random.uniform(min_ms / 1000.0, max_ms / 1000.0)
    time.sleep(delay_seconds)