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

"""
This module contains a function to fetch a random cat fact.

The function uses the Cat Facts API.

Functions:
get_random_cat_fact: Fetches a random cat fact.
"""

import requests
import os
from requests.exceptions import Timeout, TooManyRedirects, RequestException


def get_random_cat_fact():
    """
    Fetches a random cat fact from the API and returns it.
    """
    try:
        response = requests.get('https://catfact.ninja/fact', timeout=5)
        response.raise_for_status()
    except Timeout:
        return "Sorry, the request for a cat fact timed out. Please try again."
    except TooManyRedirects:
        return "Sorry, the request for a cat fact encountered too many redirects."
    except RequestException as e:
        return f"Sorry, there was a problem with the request for a cat fact: {e}"

    json_response = response.json()
    return json_response['fact']
