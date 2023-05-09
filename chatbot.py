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
from tqdm import tqdm
import time

# Current Chatbot Version
__version__ = '0.0.4-R1'

'''
 Version 0.0.4-Rev 1 Changelog
 ------------------------------- 
 Added fetch quotes from Quotes Garden
 Added Fetch random Cat Facts 
 Added Commands List for all available API's and other userful commands 
 Fixed the exit command to exit the program. 
---------------------------------
'''

# ChatBot Name
CHAT_BOT = "Pyppin"

# Replace Your OpenWeathermap.org API Key
api_key = 'API_key_here'
# Replace this with your actual NewsAPI key
NEWS_API_KEY = 'API_key_here'


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

# Fetch a Random Quote from Quote Garden.
def get_random_quote():
    try:
        url = "https://quote-garden.onrender.com/api/v3/quotes/random"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            quote_text = data['data'][0]['quoteText']
            quote_author = data['data'][0]['quoteAuthor']
            return f'"{quote_text}" - {quote_author}'
        else:
            return "Sorry, I couldn't fetch a quote right now."
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"Error occurred: {e}")
        return "Sorry, I couldn't fetch a quote right now."

# Grab a Random Cat Fact
def get_random_cat_fact():
    try:
        response = requests.get('https://catfact.ninja/fact')
        if response.status_code == 200:
            data = response.json()
            return data['fact']
        else:
            return f"Failed to retrieve cat fact. Error code: {response.status_code}"
    except requests.exceptions.RequestException:
        return "Sorry, I couldn't retrieve a cat fact right now. Please try again later."


# fetch News articles
def fetch_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        if articles:
            results = []
            for article in tqdm(articles[:5], desc="Fetching news", ncols=80):  # Limit to the first 5 articles
                title = article['title']
                url = article['url']
                results.append(f"{title}\n{url}\n")
            return "\n".join(results)
        else:
            return f"No news articles found for '{query}'."
    else:
        return f"Failed to fetch news articles. Error code: {response.status_code}"


# Fetch the weather
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
    # Show progress bar
    for _ in tqdm(range(100), desc="Searching Wikipedia"):
        time.sleep(0.01)
    results = wikipedia.summary(search_query)
    return results


def handle_google_search():
    query = input("what would you like to search for: ")
    search_results = []
    # Show progress bar
    for _ in tqdm(range(100), desc="Searching Google"):
        time.sleep(0.01)
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
        (["time"], [datetime.datetime.now().strftime("%I:%M %p")]),  # Add this line for time
        (["date"], [datetime.datetime.now().strftime("%B %d, %Y")]),  # Add this line for date
        (["how", "are", "you"],
         ["I'm doinhg well, thank you for asking!", "I'm just a computer program, but thanks for asking!"])
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
                # show commands and brief desc.
                if phrase == "commands":
                    return "\n".join(command_descriptions)
                # if cat fact return cat fact obviously
                if phrase == "cat fact":
                    return get_random_cat_fact()
                # If a keyword is found, return a random response from its corresponding list
                if phrase == "news":
                    search = input("What topic would you like news about? ")
                    return fetch_news(search)
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
