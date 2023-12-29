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

import time
import datetime
import re  # Import the re module for regular expressions

# Importing modules
import modules
from modules.random_cat_fact import get_random_cat_fact
from modules.random_quote import get_random_quote
from modules.weather import handle_weather as get_weather
from modules.g_search import handle_google_search
from modules.stackoverflow import search_stackoverflow

CHAT_BOT = "pypin"
__version__ = "0.0.7"

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

# Define functions for dynamic responses
def get_current_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_current_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

# Define functions for regular expressions and pattern matching
def handle_weather_request(user_input):
    match = re.match(r'weather in (.+)', user_input)
    if match:
        city_name = match.group(1)
        weather_data = fetch_weather_data(city_name)
        if weather_data:
            return f"The weather in {city_name} is {weather_data['description']} with a temperature of {weather_data['temperature']}°C."
    return "I couldn't fetch the weather data. Please provide a valid city name."

def extract_city_name(user_input):
    match = re.match(r'weather in (.+)', user_input)
    if match:
        return match.group(1)
    return None

def fetch_weather_data(city_name):
    # Implement logic to fetch weather data for the specified city
    # Return weather information as a dictionary or None if not found
    pass

# Define other functions for external API integrations, categorizing keywords, etc.
# ...

# Define keyword-response pairs
keywords = [
    # Greetings and Responses
    (["hello", "hi", "hey", "greetings", "good day"], ["Hi there!", "Hello!", "Hey there!", "Greetings!", "Good day to you!"]),

    # User Emotions and Responses
    (["how are you?", "how are you", "how is your day", "how is your night"], ["Good", "Fine", "Now I’m in a good mood", "If you had my life, you’d be happy too"]),

    # Gratitude and Responses
    (["thank you", "thanks"], ["you are welcome"]),

    # Bot's Name and Responses
    (["name"], [f"My name is {CHAT_BOT}.", f"I'm {CHAT_BOT}."]),

    # Expressions of Laughter and Responses
    (["lol"], ["hahah!!", "hilarious"]),

    # Positive Expressions and Responses
    (["cool", "awesome", "awsome"], ["yeah it is cool!", "I know right!?"]),

    # Queries for Word Meaning and Responses
    (["meaning"], ["I'm sorry, I don't know the meaning of that word."]),

    # Farewell and Responses
    (["bye", "goodbye", "good bye"], ["Goodbye!", "Bye!", "soo long", "see you later"]),

    # Inappropriate Language and Responses
    (["asshole", "fucker", "cunt", "bitch", "slut", "ass", "arse", "bastard"],
     ["that's not nice", "that's rude", "please don't swear at me"]),

    # Profanity and Responses
    (["fuck", "shit"], ["please use appropriate language"]),

    # Age Inquiry and Responses
    (["how old"], ["As an artificial intelligence language model, I don't have an age in the traditional sense."]),

    # Version Inquiry and Response
    (["version"], [f"{CHAT_BOT} version --> {__version__}"]),

    # List of Available Commands
    (["commands"], [", ".join(command_descriptions)]),

    # Jokes (Placeholder, you can expand this with actual jokes)
    (["joke"], []),

    # News (Placeholder, you can integrate an API for news)
    (["news"], []),

    # Random Quote
    (["quote"], [get_random_quote()]),

    # Random Cat Fact (Placeholder, you can integrate an API for cat facts)
    (["cat fact"], []),

    # Current Time
    (["time"], [get_current_time()]),

    # Current Date
    (["date"], [get_current_date()]),

    # Stack Overflow Search (Placeholder, you can implement Stack Overflow search)
    (["stackoverflow"], [search_stackoverflow]),
]

