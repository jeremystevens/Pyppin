import wikipedia
from tqdm import tqdm
import time

"""
This module contains a function to fetch a summary from Wikipedia.

The function uses the Wikipedia API.

Functions:
wikipedia_search: Fetches a summary from Wikipedia.
"""

def handle_wikipedia_search():
    """
        Fetches a summary from Wikipedia.

        Args:
        query (str): Search query.

        Returns:
        str: A string containing the Wikipedia summary, or an error message.
        """
    search_query = input("What would you like to search for: ")
    # Show progress bar
    for _ in tqdm(range(100), desc="Searching Wikipedia"):
        time.sleep(0.01)
    results = wikipedia.summary(search_query)
    return results
