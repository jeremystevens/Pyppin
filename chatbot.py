#!/usr/bin/env python
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
__version__ = '0.0.9-rc1'

# Changes Made: in 0.0.9-rc1
# =============================================================
# Removed the incorrect transformer_conversation initialization.
# Added the correct initialization of the model and tokenizer for DialoGPT.
# Updated the generate_response method to use the correct model and tokenizer for generating responses.
# Ensured the conversational pipeline is correctly created and used.
# Added memory and context feature to maintain conversation history.
# =============================================================

import spacy
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
# -*- coding: utf-8 -*-

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

# Load SpaCy's English model
nlp = spacy.load('en_core_web_sm')

# Load the model and tokenizer
model_name = "microsoft/DialoGPT-large"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create the conversational pipeline
conversation_pipeline = pipeline('text-generation', model=model, tokenizer=tokenizer)

# Bot Name
CHAT_BOT = "Pyppin"
# ChatBot Class
class ChatBot:
    def __init__(self, name=CHAT_BOT):
        self.name = name
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.conversation_history = []

    def get_greeting(self):
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            return "Good morning"
        elif 12 <= current_hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def process_input(self, user_input):
        """ Analyze user input using SpaCy and determine the response """
        # Analyze the input with SpaCy
        doc = nlp(user_input)

        # Check for entities 
        for entity in doc.ents:
            if entity.label_ == 'WEATHER':
                return self.get_weather_info(entity.text)
            # Additional conditions here

        # If no specific action is determined, use the transformer for response
        return self.generate_response(user_input)

    def generate_response(self, user_input):
        """ Generate a response using the transformer model """
        self.conversation_history.append(user_input)
        context = " ".join(self.conversation_history[-5:])  # Use last 5 interactions as context
        inputs = tokenizer.encode(context + tokenizer.eos_token, return_tensors="pt")
        response = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        output_text = tokenizer.decode(response[:, inputs.shape[-1]:][0], skip_special_tokens=True)
        self.conversation_history.append(output_text)
        return output_text

    # Example method for fetching weather (to be implemented based on existing logic)
    def get_weather_info(self, location):
        return f'Fetching weather information for {location}...'

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
                        command_descriptions = ["Command 1 description", "Command 2 description", "Command 3 description"]
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
        return self.generate_response(user_input)

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
