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

# Importing  modules
import modules
from modules import weather, random_quote, random_cat_fact, fetch_news, wikipedia_search, google_search

# Current Chatbot Version
__version__ = '0.0.6'

from modules.random_cat_fact import get_random_cat_fact

from modules.random_quote import get_random_quote
from modules.weather import handle_weather as get_weather
from modules.google_search import handle_google_search

"""
This module contains the main logic for the Pyppin chatbot.

The chatbot responds to a variety of user inputs with information fetched from different APIs. The responses include current weather, random quotes, random cat facts, news articles, Wikipedia summaries, and Google search results.

API keys are managed through environment variables for security.

Functions:
respond: Generates a response to a given user input.
"""

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
    print(f"Debug: In handle_weather, city = '{city}'")  # Debug print
    weather_info = weather.get_weather(city)
    print(f"Debug: In handle_weather, weather_info = '{weather_info}'")  # Debug print
    if weather_info:
        return weather_info
    else:
        return "I'm sorry, I couldn't fetch the weather information."


def handle_wikipedia_search(query):
    return wikipedia_search.wikipedia_search(query)


# Respond to users input
def respond(user_input):
    """
        Generates a response to a given user input.

        The function tokenizes the user input, checks it against a list of keywords, and calls the appropriate function to generate a response. If no matching keywords are found, it returns a generic response.

        Args:
        user_input (str): The user's input.

        Returns:
        str: The chatbot's response.
        """
    # Tokenize the user input
    tokens = word_tokenize(user_input.lower())
    # Define a list of keywords and their corresponding responses
    keywords = [
        (["hello"], ["Hi There", "Hello"]),
        (["hi"], ["Hello!", "Hi there!"]),
        (["thank you", "thanks"], ["you are welcome"]),
        (["name"], [f"My name is {CHAT_BOT}.", f"I'm {CHAT_BOT}."]),
        (["lol"], ["hahah!!", "hilarious"]),
        (["cool"], ["yeah it is cool!", "I know right!?"]),
        (["awesome", "awsome"], ["yes it is!", "I know right!?"]),
        (["meaning"], ["I'm sorry, I don't know the meaning of that word."]),
        (["bye", "goodbye", "good bye"], ["Goodbye!", "Bye!", "soo long", "see you later"]),
        (["asshole", "fucker", "cunt", "bitch", "slut", "ass", "arse", "bastard"],
         ["that's not nice", "that's rude", "please don't swear at me"]),
        (["fuck"], ["please use appropriate language"]),
        (["shit"], ["please use appropriate language"]),
        (["how old"], ["As an artificial intelligence language model, I don't have an age in the traditional sense."]),
        (["version"], [f"{CHAT_BOT} version --> {__version__}"]),
        (["commands"], [", ".join(command_descriptions)]),  # Add this line for commands
        (["joke"], []),
        (["news"], []),
        (["quote"], [get_random_quote()]),
        (["cat fact"], []),
        (["time"], [datetime.datetime.now().strftime("%I:%M %p")]),
        (["date"], [datetime.datetime.now().strftime("%B %d, %Y")]),
    ]

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
                print(f"Debug: city = '{city}'")  # Debug print
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
                print("Google Was Requested")
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
                    query = user_input.split('news', 1)[1].strip()
                    return modules.fetch_news.fetch_news(query)
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
