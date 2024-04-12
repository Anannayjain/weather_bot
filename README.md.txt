# Personality-Driven Weather Bot for Discord/Telegram

This is a Telegram bot that delivers real-time weather updates for any given city with a unique twist: personality! The bot has a distinct, humorous personality visible in its text responses, aiming to entertain, enlighten, and engage its audience in a memorable way.

## Features

- Fetches and provides current weather information for a specified city using the OpenWeatherMap API
- Utilizes the Geopy library for geocoding the user's location input
- Integrates the OpenAI GPT-3.5 model through the OpenRouter.ai API for generating humorous and creative responses
- Handles errors and invalid inputs creatively, aligning with the bot's unique personality

## Prerequisites

Before running the bot, make sure you have the following:

- Python 3.x installed
- A Telegram bot token (for Telegram bot) or Discord bot token (for Discord bot)
- An OpenWeatherMap API key
- An OpenRouter.ai API key

## Setup

1. Clone the repository:
https://github.com/Anannayjain/weather_bot.git

2. Navigate to the project directory:
3. Create a `.env` file in the project directory and add the following environment variables:
BOT_TOKEN=your_bot_token
WEATHER_TOKEN=your_openweathermap_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

Replace the placeholders with your actual bot token, OpenWeatherMap API key, and OpenRouter.ai API key.

4. Install the required dependencies:
pip install -r requirements.txt

## Running the Bot

To run the bot, execute the following command:
python main.py

The bot will start running and will be ready to receive commands and interact with users.

## Usage

1. Start a conversation with the bot on your preferred platform (Telegram or Discord).

2. Send the `/start` command to receive a welcome message from the bot.

3. Send the `/weather` command and enter a location when prompted.

4. The bot will fetch and provide the current weather information for the specified location, along with a humorous response based on the weather description.

5. To interact with the LLM AI (GPT-3.5), send the `/ask_llm` command followed by your query. The bot will generate a humorous response using the LLM AI.

## Acknowledgments

- [Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot) for the Telegram bot library
- [OpenWeatherMap](https://openweathermap.org/) for the weather data API
- [Geopy](https://geopy.readthedocs.io/) for the geocoding library
- [OpenRouter.ai](https://openrouter.ai/) for the LLM AI integration
- [OpenAI](https://openai.com/) for the GPT-3.5 model
- [Claude](https://www.anthropic.com/) for development




