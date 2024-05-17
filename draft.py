try:
    price_block: WebElement = driver.find_element(By.XPATH, '//*[@data-walter-collection="price"]')
    price_block.get_attribute("inner")
except:
    price_block = None