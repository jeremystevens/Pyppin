from flask import Flask, render_template, request, jsonify
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

# Current Chatbot Version
__version__ = '0.0.7'

from modules.random_cat_fact import get_random_cat_fact
from keywords import keywords
from modules.random_quote import get_random_quote
from modules.weather import handle_weather as get_weather
from modules.google_search import handle_google_search
from modules.stackoverflow import search_stackoverflow
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

# search stack overflow




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
##    keywords = [
##        (["hello"], ["Hi There", "Hello"]),
##        (["hi"], ["Hello!", "Hi there!"]),
##        (["thank you", "thanks"], ["you are welcome"]),
##        (["name"], [f"My name is {CHAT_BOT}.", f"I'm {CHAT_BOT}."]),
##        (["lol"], ["hahah!!", "hilarious"]),
##        (["cool"], ["yeah it is cool!", "I know right!?"]),
##        (["awesome", "awsome"], ["yes it is!", "I know right!?"]),
##        (["meaning"], ["I'm sorry, I don't know the meaning of that word."]),
##        (["bye", "goodbye", "good bye"], ["Goodbye!", "Bye!", "soo long", "see you later"]),
##        (["asshole", "fucker", "cunt", "bitch", "slut", "ass", "arse", "bastard"],
##         ["that's not nice", "that's rude", "please don't swear at me"]),
##        (["fuck"], ["please use appropriate language"]),
##        (["shit"], ["please use appropriate language"]),
##        (["how old"], ["As an artificial intelligence language model, I don't have an age in the traditional sense."]),
##        (["version"], [f"{CHAT_BOT} version --> {__version__}"]),
##        (["commands"], [", ".join(command_descriptions)]),  # Add this line for commands
##        (["joke"], []),
##        (["news"], []),
##        (["quote"], [get_random_quote()]),
##        (["cat fact"], []),
##        (["time"], [datetime.datetime.now().strftime("%I:%M %p")]),
##        (["date"], [datetime.datetime.now().strftime("%B %d, %Y")]),
##    ]

    # Define a list of individual keywords to check for
    individual_keywords = [
        "weather in",
        "wikipedia",
        "google",
        "stackoverflow"
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
        
            elif token =="stackoverflow":
                query = user_input.split('stackoverflow', 1)[1].strip()  # Extract the part of the message after 'stackoverflow'
                response = search_stackoverflow(query)
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


 ### ============== FLASK =========================== #

app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for handling user requests
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = respond(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()
