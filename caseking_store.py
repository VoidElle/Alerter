import os

from twilio.rest import Client
from dotenv import load_dotenv
from bs4 import BeautifulSoup

import undetected_chromedriver as uc

load_dotenv()

# Constants | Variables
RYZEN_NAME = "Ryzen 9 7950X3D 5,7 GHz (Raphael) AM5 - boxed"
STORE_URL = "https://www.caseking.de/amd-ryzen-9-7950x3d-5-7-ghz-raphael-am5-boxed-hpam-259.html?__shop=2"
STORE_NAME = "CASEKING"
NOT_IN_STOCK_TEXT = "not in stock"
BACK_IN_STOCK_MESSAGE = os.environ['BACK_IN_STOCK_NAME']
ALERT_TEXT = STORE_NAME + " - " + BACK_IN_STOCK_MESSAGE + " - " + STORE_URL

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
SENDER_NUMBER = os.environ['TWILIO_SENDER_NUMBER']
RECIVER_NUMBER = os.environ['RECIVER_NUMBER']

# Init
client = Client(ACCOUNT_SID, AUTH_TOKEN)
driver = uc.Chrome()
driver.get(STORE_URL)

# Getting source code
soup = BeautifulSoup(driver.page_source, features="lxml")
body = soup.body

# Getting our specific element
ryzen_element = ""
products_list = body.find_all("div", {"class": "right grid_14 first last"})
for product in products_list:
    product_text = product.get_text()
    if RYZEN_NAME in product_text:
        ryzen_element = product_text

if NOT_IN_STOCK_TEXT in ryzen_element:
    message = client.messages.create(body=ALERT_TEXT, from_=SENDER_NUMBER, to=RECIVER_NUMBER)
    print(message.sid)