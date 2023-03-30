import os

from twilio.rest import Client
from dotenv import load_dotenv
from bs4 import BeautifulSoup

import undetected_chromedriver as uc

load_dotenv()

# Constants | Variables
AMD_RYZEN_NAME = "AMD Ryzen™ 9 7950X3D Processor"
AMD_STORE_URL = "https://www.amd.com/en/direct-buy/it"
ALERT_TEXT = "AMD STORE - RYZEN 9 7950x3D E' TORNATO DISPONIBILE - " + AMD_STORE_URL

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
SENDER_NUMBER = os.environ['TWILIO_SENDER_NUMBER']
RECIVER_NUMBER = os.environ['RECIVER_NUMBER']

# Init
client = Client(ACCOUNT_SID, AUTH_TOKEN)
driver = uc.Chrome()
driver.get(AMD_STORE_URL)

# Getting source code
soup = BeautifulSoup(driver.page_source, features="lxml")
body = soup.body

# Getting our specific element
ryzen_element = ""
products_list = body.find_all("div", {"class": "direct-buy"})
for product in products_list:
    product_text = product.get_text()
    if AMD_RYZEN_NAME in product_text:
        ryzen_element = product_text

not_in_stock_text = "Out of Stock"
if not_in_stock_text not in ryzen_element:
    message = client.messages.create(body=ALERT_TEXT, from_=SENDER_NUMBER, to=RECIVER_NUMBER)
    print(message.sid)
