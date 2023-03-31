import json
import time

from dotenv import load_dotenv
from bs4 import BeautifulSoup

import undetected_chromedriver as uc

load_dotenv()

config_file = open('config.json', encoding='utf-8')
config_data = json.load(config_file)
config_file.close()

messages_sent_file = open('messages_sent.json', encoding='utf-8')
messages_sent_data = json.load(messages_sent_file)
messages_sent_file.close()

stores = config_data["stores"]

driver = uc.Chrome()

for store in stores:

    store_name = store["store_name"]
    store_link = store["link"]
    product_name = store["product_name"]
    not_in_stock_text = store["not_in_stock_text"]
    element_to_search = store["element_to_search"]
    type_to_search = store["type_to_search"]
    class_or_id_to_search = store["class_or_id_to_search"]
    is_list = store["is_list"]

    driver.get(store_link)

    soup = BeautifulSoup(driver.page_source, features="lxml")
    body = soup.body

    print("INFO: Checking store " + store_name)

    product_element = None
    if is_list:

        print("INFO: Mode list check")

        products_list = body.find_all(element_to_search, {type_to_search: class_or_id_to_search})
        while products_list is None:
            print("INFO: Product not found, waiting 5s and restarting the search...")
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, features="lxml")
            body = soup.body
            products_list = body.find_all(element_to_search, {type_to_search: class_or_id_to_search})

        for product in products_list:
            product_text = product.get_text()
            if product_name in product_text:
                product_element = product_text

    else:

        print("INFO: Mode singular check")

        product = body.find(element_to_search, {type_to_search: class_or_id_to_search})
        while product is None:
            print("INFO: Product not found, waiting 5s and restarting the search...")
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, features="lxml")
            body = soup.body
            product = body.find(element_to_search, {type_to_search: class_or_id_to_search})
        product_element = product.get_text()

    if not_in_stock_text not in product_element:
        print("IT'S IN STOCK")
    else:
        print("IS NOT IN STOCK")

    print("====================")
