import time
import datetime
# Importing  modules
import modules
from modules import weather, fetch_news, wikipedia_search
from modules.random_cat_fact import get_random_cat_fact
from modules.random_quote import get_random_quote
from modules.weather import handle_weather as get_weather
from modules.google_search import handle_google_search
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
