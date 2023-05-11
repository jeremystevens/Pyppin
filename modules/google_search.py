from googlesearch import search
from tqdm import tqdm
import time

"""
This module contains a function to perform a Google search.

The function uses the Google Search API.

Functions:
google_search: Performs a Google search.
"""

def handle_google_search():
    """
        Performs a Google search.

        Args:
        query (str): Search query.
        api_key (str): Google Search API key.

        Returns:
        str: A string containing the Google search results, or an error message.
        """
    query = input("What would you like to search for: ")
    search_results = []
    # Show progress bar
    for _ in tqdm(range(100), desc="Searching Google"):
        time.sleep(0.01)
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        search_results.append(j)

    return "\n".join(search_results)
