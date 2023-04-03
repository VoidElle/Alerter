# Alerter
Alerter is a python based stock monitoring bot.
It's a customizable and automated solution for tracking product availability across multiple websites. 
By utilizing web scraping technology, the bot can continuously check selected websites to determine whether the desired product is back in stock.

The bot is highly configurable, allowing users to select the specific product and websites they wish to monitor. 
Additionally, the bot is integrated with Telegram, enabling users to receive real-time notifications whenever the product becomes available again.

The bot is easy to use and can be customized without requiring any programming knowledge.

<!-- GETTING STARTED -->
## Getting Started

Before executing Alerter, you have to follow the instructions below to make it works 

### Prerequisites
- Python 3
- Pip 3
- Chrome (Not Chromium)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/VoidElle/Alerter.git
   ```
2. Install the required packages
   ```sh
   pip3 install -r requirements.txt
   ```
3. Create a .env file (In the project directory) with the following keys
   ```sh
   BACK_IN_STOCK_NAME=The product is back in stock! # Text that will be sent by Telegram
   TELEGRAM_BOT_TOKEN=TOKEN # Your Telegram bot token
   TELEGRAM_USER_ID=USER_ID # The id of the user that will get a notification
   ```
4. Populate the `config.json` file adding the stores (Use the `config_example.json` for a described example)
5. Populate the `status.json` file adding the template status for the stores (Use the `status_example.json` for a described example)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Execution

### Normal execution
To execute the bot using a normal procedure you have to start the script `normal_checker.py` using the following command:
   ```sh
   python3 normal_checker.py
   ```

### Automatic execution
To execute the bot using an automatic execution (Like crontab for linux) you have to execute a different script, `scheduled_checker.py` using the following command:
   ```sh
   python3 scheduled_checker.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
