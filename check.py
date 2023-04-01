import json
import time

from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup

import undetected_chromedriver as uc

load_dotenv()

config_file = open('config.json', encoding='utf-8')
config_data = json.load(config_file)
config_file.close()

log_file_read = open("status.json", encoding="utf-8")
log_file_data = json.load(log_file_read)
log_file_read.close()

waiting_time = config_data["waiting_time_s"]
stores = config_data["stores"]

driver = uc.Chrome()

time_format = "%d/%m/%Y %H:%M:%S"

for store in stores:

    store_name = store["store_name"]
    store_link = store["link"]
    product_name = store["product_name"]
    not_in_stock_text = store["not_in_stock_text"]
    element_to_search = store["element_to_search"]
    type_to_search = store["type_to_search"]
    class_or_id_to_search = store["class_or_id_to_search"]
    is_list = store["is_list"]

    store_log_data = log_file_data[store_name]

    driver.get(store_link)

    soup = BeautifulSoup(driver.page_source, features="lxml")
    body = soup.body

    print("INFO: Checking store " + store_name)

    product_element = None
    if is_list:

        print("INFO: Mode list check")

        products_list = body.find_all(element_to_search, {type_to_search: class_or_id_to_search})
        while products_list is None:
            print("INFO: Product not found, waiting " + waiting_time + "s and restarting the search...")
            time.sleep(waiting_time)
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
            print("INFO: Product not found, waiting " + waiting_time + "s and restarting the search...")
            time.sleep(waiting_time)
            soup = BeautifulSoup(driver.page_source, features="lxml")
            body = soup.body
            product = body.find(element_to_search, {type_to_search: class_or_id_to_search})
        product_element = product.get_text()

    print(product_element)
    if not_in_stock_text not in product_element:
        print("INFO: STOCK AVAILABLE ✅")
        now = datetime.now()
        store_log_data["time_found"] = now.strftime(time_format)
        store_log_data["found"] = True
    else:
        print("INFO: Stock not available ❌")
        store_log_data["found"] = False

    now = datetime.now()
    store_log_data["last_check"] = now.strftime(time_format)

    log_json_object = json.dumps(log_file_data, indent=4)
    with open("status.json", "w") as outfile:
        outfile.write(log_json_object)

    print("=========================")
