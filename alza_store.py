import os

from twilio.rest import Client
from dotenv import load_dotenv
from bs4 import BeautifulSoup

import undetected_chromedriver as uc

load_dotenv()

# Constants | Variables
RYZEN_NAME = "AMD Ryzen 9 7950X3D"
STORE_URL = "https://www.alza.cz/EN/amd-ryzen-9-7950x3d-d7665222.htm"
STORE_NAME = "ALZASTORE"
NOT_IN_STOCK_TEXT = "We accept pre-orders"
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
product = None
while product is None:
    product = body.find("span", {"class": "stcStock avlVal avl4 none"})

product_text = product.get_text()

if NOT_IN_STOCK_TEXT not in product_text:
    message = client.messages.create(body=ALERT_TEXT, from_=SENDER_NUMBER, to=RECIVER_NUMBER)
    print(message.sid)