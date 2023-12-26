# MIT License

# Copyright (c) 2023 - Jeremy Stevens

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Import required modules
from nltk.tokenize import word_tokenize
import random
import os
import datetime
import requests
import aiohttp
import asyncio
import time

# Importing  modules
import modules
from modules import weather, fetch_news, wikipedia_search
from modules.random_cat_fact import get_random_cat_fact
from modules.random_quote import get_random_quote
from modules.weather import handle_weather as get_weather
from modules.google_search import handle_google_search

# import keywords
from keywords import keywords

# Current Chatbot Version
__version__ = '0.0.7'

# ChatBot Name
CHAT_BOT = "Pyppin"
user_name = ""  # username

'''
don't forget to set the environment variables 
setx WEATHER_API_KEY = ""
setx NEWS_API_KEY = ""
'''

# Get API keys from environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Pass API keys to functions that need them
weather.WEATHER_API_KEY = WEATHER_API_KEY
fetch_news.NEWS_API_KEY = NEWS_API_KEY

# Define a list of command keywords to help the user.
command_descriptions = [
    "Commands List \n",
    "weather: Fetches the current weather for a specified city.",
    "wikipedia: Searches Wikipedia for a specified topic.",
    "google: Performs a Google search for a specified query.",
    "joke: Tells a random joke.",
    "quote: Provides a random quote.",
    "news: Fetches the latest news articles based on a user-specified topic.",
    "cat_fact: Provides a random cat fact.",
    "date: Get the current date mm/dd/yyyy format",
    "time: Get the current time in hh/mm/ss format",
    "version: Get the Version of pyppin you are running",
    "exit(): Exits the chatbot."
]


def get_greeting():
    current_hour = datetime.datetime.now().hour

    if current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


# get the weather
def handle_weather(city):
    #print(f"Debug: In handle_weather, city = '{city}'")  # Debug print
    weather_info = weather.get_weather(city)
    print(f"Debug: In handle_weather, weather_info = '{weather_info}'")  # Debug print
    if weather_info:
        return weather_info
    else:
        return "I'm sorry, I couldn't fetch the weather information."


def handle_wikipedia_search(query):
    return wikipedia_search.wikipedia_search(query)


# make_api_request function with rate limit handling
def make_api_request(url, params=None):
    max_retries = 5
    backoff_time = 1

    for attempt in range(max_retries):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            print(f"Rate limit exceeded. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            backoff_time *= 2
            continue

        # Handle other error codes...

        response.raise_for_status()

    # Handle max retries exceeded
    print("Max retries exceeded. Unable to make API request.")
    return None

# Respond to users input
def respond(user_input):
    # Tokenize the user input
    tokens = word_tokenize(user_input.lower())
    # list of keywords
    ''' moved keywords to keywords.py '''
    # Define a list of individual keywords to check for
    individual_keywords = [
        "weather in",
        "wikipedia",
        "google"
    ]
    # Check for individual keywords
    for keyword in individual_keywords:
        if keyword in user_input.lower():
            if keyword == "weather in":
                city = user_input.lower().split("weather in")[1].strip()
                #print(f"Debug: city = '{city}'")  # Debug print
                return get_weather(city)

    # Check for individual keywords
    for token in tokens:
        if token in individual_keywords:
            if token == "weather in":
                city = user_input.lower().split("weather in")[1].strip()
                return modules.weather(city)

            elif token == "wikipedia":
                query = user_input.split('wikipedia', 1)[1].strip()  # Extract the part of the user_input after 'wikipedia'
                response = modules.wikipedia_search.handle_wikipedia_search(query)
                return response

            elif token == "google":
                query = user_input.split('google', 1)[1].strip()  # Extract the part of the message after 'google'
                response = handle_google_search(query)
                return response

    # Other Phrases
    for phrase in [" ".join(tokens[i:i + 2]) for i in range(len(tokens) - 1)] + tokens:
        for keyword, responses in keywords:
            if phrase in keyword:
                # show commands and brief desc.
                if phrase == "commands":
                    return "\n".join(command_descriptions)
                # if cat fact return cat fact obviously
                if phrase == "cat fact":
                    return get_random_cat_fact()
                # If a keyword is found, return a random response from its corresponding list
                if phrase == "news":
                    # changed to use Aio in 0.7
                    query = user_input.split('news', 1)[1].strip()

                    async def run_fetch_news():
                        return await modules.fetch_news.fetch_news(query)
                    loop = asyncio.get_event_loop()
                    news_result = loop.run_until_complete(run_fetch_news())
                    return news_result
                if phrase == "joke":
                    try:
                        url = "https://official-joke-api.appspot.com/random_joke"
                        response = requests.get(url)
                        if response.status_code == 200:
                            data = response.json()
                            setup = data['setup']
                            punchline = data['punchline']
                            return f"{setup}\n{punchline}"
                        else:
                            return f"Failed to retrieve joke. Error code: {response.status_code}"
                    # catch request exception ex. no internet connection
                    except requests.exceptions.RequestException:
                        return "Sorry, I couldn't retrieve a joke right now. Please try again later."
                else:
                    return random.choice(responses)

    # If no keyword is found, return a generic response
    return "I'm sorry, I didn't understand what you said."


# Greet User
print(f"chatbot: {get_greeting()}, How can I assist you today?")

# Prompt the user for input and get a response from the chatbot
city = None
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit()":
        answer = input("Chatbot: are you sure you want to quit ? y / n? ")
        if answer.lower() == "y":
            print("Chatbot: Goodbye! See you Next time")
            break
        else:
            print("Chatbot: I will not quit yet")
            continue
    response = respond(user_input)
    print("Chatbot:", response)
