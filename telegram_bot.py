import json
from datetime import datetime, timedelta

import requests
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_USER_ID")

STATUS_FILE_PATH = "./status.json"

log_file_read = open(STATUS_FILE_PATH, encoding="utf-8")
log_file_data = json.load(log_file_read)
log_file_read.close()

alert_text = """
=======⚠️=======
STATUS: Product found
Store: %store_name%
Orario: %time_found%
Link: %link%
=======⚠️======="""

warning_text = """
=======⚠️=======
STATUS: WARNING
Store: %store_name%
Warning: %warning%
=======⚠️======="""

time_format = "%d/%m/%Y %H:%M:%S"


def send_to_telegram(message):
    api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    try:
        response = requests.post(api_url, json={'chat_id': CHAT_ID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def main():
    for store in log_file_data:

        store_loaded = log_file_data[store]

        store_name = store
        store_found_status = store_loaded["found"]
        store_found_time = store_loaded["time_found"]
        store_found_link = store_loaded["link"]
        store_message_sent = store_loaded["message_sent"]
        store_warning = store_loaded["warning"]

        if store_warning is not None:

            new_warning_text = warning_text.replace("%warning%", store_warning).replace("%store_name%", store_name)
            send_to_telegram(new_warning_text)

            now = datetime.now()
            store_loaded["message_sent"] = now.strftime(time_format)

            log_json_object = json.dumps(log_file_data, indent=4)
            with open(STATUS_FILE_PATH, "w") as outfile:
                outfile.write(log_json_object)

            continue

        if store_found_status:

            if store_message_sent is not None:

                store_message_sent_obj = datetime.strptime(store_message_sent, time_format)
                now = datetime.now()

                # Send message only if the alert hasn't been sent in the previous 24 hours
                # (Used not to create an alert bombing)
                if not (now-timedelta(hours=24) <= store_message_sent_obj <= now) or store_message_sent_obj is None:
                    new_alert_text = alert_text.replace("%store_name%", store_name).replace("%time_found%", store_found_time).replace("%link%", store_found_link)
                    send_to_telegram(new_alert_text)

                    now = datetime.now()
                    store_loaded["message_sent"] = now.strftime(time_format)

                    log_json_object = json.dumps(log_file_data, indent=4)
                    with open(STATUS_FILE_PATH, "w") as outfile:
                        outfile.write(log_json_object)

            elif store_message_sent is None:

                new_alert_text = alert_text.replace("%store_name%", store_name).replace("%time_found%", store_found_time).replace("%link%", store_found_link)
                send_to_telegram(new_alert_text)

                now = datetime.now()
                store_loaded["message_sent"] = now.strftime(time_format)

                log_json_object = json.dumps(log_file_data, indent=4)
                with open(STATUS_FILE_PATH, "w") as outfile:
                    outfile.write(log_json_object)


if __name__ == "__main__":
    main()
