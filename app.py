'''
bot interacts with user to provide weather information based on provided location.
makes use of OpenWeatherMap API to fetch weather data and Geopy library to geocode location input from user
'''
import os
import telebot
import requests
import json
import logging, logging.config
import random
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')  # Update this line

POLLING_TIMEOUT = None
bot = telebot.TeleBot(BOT_TOKEN)


config = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'short': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
        'long': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'short',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'plugins': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''
    returns a welcome message when the '/start' command is sent by the user
    '''
    bot.send_message(message.chat.id, 
    '''Ahoy, weather voyager, ready to rhyme?
        Come decode the skies or share a funny line!
        Let's banter about clouds or the oddities of fate,
        In this whimsical chat, laughter awaits!''')


@bot.message_handler(commands=['weather'])
def send_weather(message):
    '''
    returns a prompt asking the user to enter a location when the '/weather' command is sent.
    registers the next step handler to wait for the user's input and calls the 'fetch_weather' function
    '''
    location = 'Enter a Location: '
    sent_message = bot.send_message(message.chat.id, location, parse_mode='Markdown')
    bot.register_next_step_handler(sent_message, fetch_weather)
    return location


def location_handler(message):
    '''
    returns the latitude and longitude coordinated from user's message (location) using the Nominatim geocoder.
    if location is found - returns the rounded latitude and longitude
    else - returns Location not found
    '''
    location = message.text
    # Create a geocoder instance
    geolocator = Nominatim(user_agent="my_app")

    try:
        # Get the latitude and longitude
        location_data = geolocator.geocode(location)
        latitude = round(location_data.latitude,2)
        longitude = round(location_data.longitude,2)
        logger.info("Latitude '%s' and Longitude '%s' found for location '%s'", latitude, longitude, location)
        return latitude, longitude
    except AttributeError:
        logger.exception('Location not found', exc_info=True)


def get_weather(latitude,longitude):
    '''
    arguments - latitude, longitude
    takes in arguments as inputs and constructs URL to make API call to OpenWeatherMap API
    returns a response JSON after fetching weather data for the specified latitude and longitude
    '''
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'.format(latitude, longitude, WEATHER_TOKEN)
    response = requests.get(url)
    # print(response.json())
    return response.json()

def generate_humorous_response(description):
    """
    Generates a humorous response based on the weather description.
    """
    if 'rain' in description:
        responses = [
            "Looks like it's raining cats and dogs out there!",
            "Don't forget your umbrella, unless you want to look like a drowned rat!",
            "Rain, rain, go away! Come again another day when I don't have plans."
        ]
    elif 'sunny' in description:
        responses = [
            "Time to break out the sunscreen and shades!",
            "It's a beautiful day to be outside and work on your tan lines!",
            "Careful, the sun is out and ready to turn you into a human crisp!"
        ]
    elif 'clouds' in description:
        responses = [
            "Looks like the clouds are having a party in the sky today.",
            "Don't let the clouds rain on your parade, there's always a silver lining!",
            "Cloudy with a chance of sarcasm and witty remarks!"
        ]
    else:
        responses = [
            "The weather is as unpredictable as my sense of humor!",
            "I'm not sure what to make of this weather, but at least it's not boring!",
            "Weather forecast: a high chance of puns and dad jokes!"
        ]

    return random.choice(responses)
    
def fetch_weather(message): 
    '''
    called when the user provides location in response to the '/weather' command.
    uses the 'location_handler' function to get latitude & longitude of the provided location and 'get_weather' function to fetch the weather data
    extracts weather description from API response and sends to user as message.
    '''
    latitude, longitude = location_handler(message)
    weather = get_weather(latitude,longitude)
    data = weather['list']
    data_2 = data[0]
    info = data_2['weather']
    data_3 = info[0]
    description = data_3['description']
    weather_message = f'*Weather:* {description}\n'
    humorous_response = generate_humorous_response(description)
    bot.send_message(message.chat.id, 'Here\'s the weather!')
    bot.send_message(message.chat.id, weather_message, parse_mode='Markdown')
    bot.send_message(message.chat.id, humorous_response)
    


# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     '''
#     echoes back any other messages bot receives from user
#     '''
#     bot.reply_to(message, message.text)




def get_llm_response(query):
    '''
    Calls the LLM AI API with the provided query and returns the response.
    '''
    
    response = requests.post(url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {'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'}",
        # "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
        # "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
    },
    data=json.dumps({ 
        "model": "openai/gpt-3.5-turbo", # Optional
        "messages": [
        {"role": "user", "content": "add humor to this: "+query}
        ]
    })
    )
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f'Error fetching response from LLM AI. Status code:{response.status_code}'

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    '''
    Handles messages received by the bot.
    '''
    if message.text.startswith('/ask_llm'):
        # Extract the query from the message
        query = message.text[len('/ask_llm'):].strip()
        # Call the LLM AI API to get a response
        response = get_llm_response(query)
        bot.send_message(message.chat.id, response)
    else:
        # Echo back other messages
        bot.reply_to(message, message.text)


    
bot.infinity_polling()