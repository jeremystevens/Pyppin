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

import nltk
from nltk.tokenize import word_tokenize
import random
import requests
import math
import os
import json
import datetime
import wikipedia
from googlesearch import search

# Current Chatbot Version
__version__ = '0.0.2-R1'

# ChatBot Name
CHAT_BOT = "Pyppin"

# Replace YOUR_API_KEY with your actual API key
api_key = 'API_key_here'


def handle_weather():
    city = input("Enter the City Name: ")
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature_k = data['main']['temp']
        temperature_f = math.ceil((9 / 5) * (temperature_k - 273) + 32)
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        return f'The weather in {city} is {description} with a temperature of {temperature_f} °F and a humidity of {humidity}%.'

    return f'Request failed with error code {response.status_code}.'


def handle_clear_screen():
    os.system('cls')
    return f'clearing screen'


def handle_wikipedia_search():
    search_query = input("What would you like to search for: ")
    results = wikipedia.summary(search_query)
    return results


def handle_google_search():
    query = input("what would you like to search for: ")
    search_results = []

    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        search_results.append(j)

    return "\n".join(search_results)


def respond(user_input):
    # Tokenize the user input
    tokens = word_tokenize(user_input.lower())

    # Define a list of keywords and their corresponding responses
    keywords = [
        (["hello"], ["Hi There", "Hello"]),
        (["hi"], ["Hello!", "Hi there!"]),
        (["thank you", "thanks"], ["you are welcome"]),
        (["name"], [f"My name is {CHAT_BOT}.", f"I'm {CHAT_BOT}."]),
        (["lol"], ["hahah!!", "hilarious"]),
        (["meaning"], ["I'm sorry, I don't know the meaning of that word."]),
        (["bye", "goodbye", "good bye"], ["Goodbye!", "Bye!", "soo long", "see you later"]),
        (["asshole", "fucker", "cunt", "bitch", "slut", "ass", "arse", "bastard"],
         ["that's not nice", "that's rude", "please don't swear at me"]),
        (["fuck"], ["please use appropriate language"]),
        (["shit"], ["please use appropriate language"]),
        (["how old"], ["As an artificial intelligence language model, I don't have an age in the traditional sense."]),
        (["version"], [f"{CHAT_BOT} version --> {__version__}"]),
        (["joke"], []),
        (["time"], [datetime.datetime.now().strftime("%I:%M %p")]),  # Add this line for time
        (["date"], [datetime.datetime.now().strftime("%B %d, %Y")]),  # Add this line for date
        (["how", "are", "you"],
         ["I'm doing well, thank you for asking!", "I'm just a computer program, but thanks for asking!"])
    ]

    # Define a list of individual keywords to check for
    individual_keywords = [
        "weather",
        "clear screen",
        "wikipedia",
        "google"
    ]

    # Check for individual keywords
    for token in tokens:
        if token in individual_keywords:
            if token == "weather":
                return handle_weather()
            elif token == "clear screen":
                return handle_clear_screen()
            elif token == "wikipedia":
                return handle_wikipedia_search()
            elif token == "google":
                return handle_google_search()

    # The rest of your respond() function
    for phrase in [" ".join(tokens[i:i + 2]) for i in range(len(tokens) - 1)] + tokens:
        for keyword, responses in keywords:
            if phrase in keyword:
                # If a keyword is found, return a random response from its corresponding list
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

                # Get Date
                if phrase == "date":
                    now = datetime.now()
                    return now.strftime("%B %d, %Y")

                # Get the Time
                if phrase == "time":
                    now = datetime.now()
                    return now.strftime("%I:%M %p")

    # If no keyword is found, return a generic response
    return "I'm sorry, I didn't understand what you said."

# Prompt the user for input and get a response from the chatbot
city = None
while True:
    user_input = input("You: ")
    response = respond(user_input)
    print("Chatbot:", response)
