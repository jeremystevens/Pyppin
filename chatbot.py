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
nltk.download('punkt') # Download the Punkt tokenizer for NLTK if not already downloaded
from nltk.tokenize import word_tokenize
import random
import os
import datetime
import requests
import asyncio
import time

# Importing modules
import modules
from modules import weather, fetch_news, wikipedia_search
from modules.random_cat_fact import get_random_cat_fact
from keywords import keywords
from modules.random_quote import get_random_quote
from modules.weather import handle_weather as get_weather
from modules.g_search import handle_google_search
from modules.stackoverflow import search_stackoverflow

# Current Chatbot Version and Name
__version__ = '0.0.8'
CHAT_BOT = "Pyppin"
# ChatBot Class
class ChatBot:
    def __init__(self, name=CHAT_BOT):
        self.name = name
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')

    def get_greeting(self):
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            return "Good morning"
        elif 12 <= current_hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def respond(self, user_input):
        # Tokenize the user input
        tokens = word_tokenize(user_input.lower())

        # Define a list of individual keywords to check for
        individual_keywords = ["weather in", "wikipedia", "google", "stackoverflow"]

        # Check for individual keywords
        for token in tokens:
            if token in individual_keywords:
                if token == "weather in":
                    city = user_input.lower().split("weather in")[1].strip()
                    return get_weather(city, self.weather_api_key)

                elif token == "wikipedia":
                    query = user_input.split('wikipedia', 1)[1].strip()
                    return wikipedia_search.wikipedia_search(query)

                elif token == "google":
                    query = user_input.split('google', 1)[1].strip()
                    return handle_google_search(query)

                elif token == "stackoverflow":
                    query = user_input.split('stackoverflow', 1)[1].strip()
                    return search_stackoverflow(query)

        # Other Phrases
        for phrase in [" ".join(tokens[i:i + 2]) for i in range(len(tokens) - 1)] + tokens:
            for keyword, responses in keywords:
                if phrase in keyword:
                    if phrase == "commands":
                        return "\n".join(command_descriptions)
                    if phrase == "cat fact":
                        return get_random_cat_fact()
                    if phrase == "news":
                        async def run_fetch_news():
                            return await fetch_news.fetch_news(query, self.news_api_key)
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
                        except requests.exceptions.RequestException:
                            return "Sorry, I couldn't retrieve a joke right now. Please try again later."
                    else:
                        return random.choice(responses)

        # If no keyword is found, return a generic response
        return "I'm sorry, I didn't understand what you said."

# Main CLI interface
if __name__ == '__main__':
    bot = ChatBot()
    print(f"{bot.get_greeting()}! I'm {bot.name}, your chatbot. How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit()":
            print("Goodbye!")
            break
        response = bot.respond(user_input)
        print(f"{bot.name}: {response}")
