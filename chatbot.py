import logging
import os
import datetime
import requests
import aiohttp
import asyncio
import random
from nltk.tokenize import word_tokenize
import nltk
import modules
from modules import weather, fetch_news, wikipedia_search
from modules.random_cat_fact import get_random_cat_fact
from modules.random_quote import get_random_quote
from modules.weather import handle_weather as get_weather, handle_weather
from modules.google_search import handle_google_search

# Set up logging
from modules.wikipedia_search import handle_wikipedia_search

logging.basicConfig(filename='chatbot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
__version__ = '0.0.8'
CHAT_BOT = "Pyppin"
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
weather.WEATHER_API_KEY = WEATHER_API_KEY
fetch_news.NEWS_API_KEY = NEWS_API_KEY
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


# Function Definitions
def get_greeting():
    """
        Returns a greeting based on the current time.

        Returns:
            str: The greeting message.
    """

    logging.info('Chatbot initiated')
    current_hour = datetime.datetime.now().hour

    if current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def handle_date_search(query):
    """
       Handles a date search query.

       Args:
           query (str): The date query.

       Returns:
           str: The search result.
    """
    print("Date Search Started")
    pass

def handle_general_query(query):
    """
       Handles a general query.

       Args:
           query (str): The general query.

       Returns:
           str: The query response.
    """
    print("General Query")
    pass

def respond(user_input):
    """
        Generates a response to a given user input.

        Args:
            user_input (str): The user's input.

        Returns:
            str: The chatbot's response.
    """
    # Tokenize the user input
    tokens = word_tokenize(user_input.lower())
    tagged_tokens = nltk.pos_tag(tokens)
    named_entities = nltk.ne_chunk(tagged_tokens)
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
        (["weather in"], []),
        (["cat fact"], []),
        (["time"], [datetime.datetime.now().strftime("%I:%M %p")]),
        (["date"], [datetime.datetime.now().strftime("%B %d, %Y")]),
        (["are", "you"], ["doing great! thanks", "doing ok thanks for asking"]),
        (["feel"], ["As an artificial intelligence language model I have no Feeling", "I feel fantastic",
                    "I need more sleep to be honest"]),
        (["", "", "feeling"], ["As an artificial intelligence language model I have no Feeling", "I feel fantastic",
                               "I need more sleep to be honest"]),
    ]

    # Define a list of individual keywords to check for
    individual_keywords = [
        "weather in",
        "wikipedia",
        "google"
    ]

    def extract_named_entities(tree):
        named_entities = []
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NE'):
            entity = ' '.join(word for word, tag in subtree.leaves())
            entity_type = subtree.label()
            named_entities.append((entity, entity_type))
        return named_entities

    def handle_named_entities(named_entities, user_input):
        response = ""  # Initialize response with default value
        for entity, entity_type in named_entities:
            if entity_type == 'PERSON':
                # Handle person name
                # Example: "My name is John"
                response = f"Nice to meet you, {entity}!"
            elif entity_type == 'LOCATION':
                # Handle location
                # Example: "Tell me the weather in Paris"
                city = entity
                response = handle_weather(city)
            elif entity_type == 'ORGANIZATION':
                # Handle organization
                # Example: "Search for information about OpenAI"
                query = entity
                response = handle_wikipedia_search(query)
            elif entity_type == 'DATE':
                # Handle date
                # Example: "What happened on January 1st, 2022?"
                response = handle_date_search(entity)

        # If no named entity is found, fallback to regular response
        if not response:
            response = handle_general_query(user_input)

        return response

    # Check for individual keywords
    for token in tokens:
        if token in individual_keywords:
            if token == "weather in":
                city = user_input.lower().split("weather in")[1].strip()
                return modules.weather(city)

            elif token == "wikipedia":
                query = user_input.split('wikipedia', 1)[
                    1].strip()  # Extract the part of the user_input after 'wikipedia'
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
                if phrase == "weather in":
                    city = user_input.lower().split("weather in")[1].strip()
                    response = weather.handle_weather(city)
                    return response
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


# Main Code Block
def chatbot():
    print(f"chatbot: {get_greeting()}, How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit()":
            print("Chatbot: Goodbye! See you Next time")
            logging.info('Chatbot: Goodbye! See you Next time')
            break
        if user_input.lower() == "error":
            logging.error('User input caused an error')
        response = respond(user_input)
        logging.info(f'Chatbot: {response}')
        print("Chatbot:", response)


if __name__ == "__main__":
    chatbot()
