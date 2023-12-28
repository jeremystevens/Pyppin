import requests

"""
This module contains a function to fetch a random quote.

The function uses the Quotable API.

Functions:
get_random_quote: Fetches a random quote.
"""

import requests
import os
from requests.exceptions import Timeout, TooManyRedirects, RequestException


def get_random_quote():

    """
    Fetches a random quote from the API and returns it.
    """
    try:
        response = requests.get('https://api.quotable.io/random', timeout=5)
        response.raise_for_status()
    except Timeout:
        return "Sorry, the request for a quote timed out. Please try again."
    except TooManyRedirects:
        return "Sorry, the request for a quote encountered too many redirects."
    except RequestException as e:
        return f"Sorry, there was a problem with the request for a quote: {e}"

    json_response = response.json()
    return f'"{json_response["content"]}" - {json_response["author"]}'
