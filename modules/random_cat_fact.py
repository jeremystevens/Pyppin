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

import requests

"""
This module contains a function to fetch a random cat fact.

The function uses the Cat Facts API.

Functions:
get_random_cat_fact: Fetches a random cat fact.
"""

def get_random_cat_fact():
    """
       Fetches a random cat fact.

       Args:
       api_key (str): Cat Facts API key.

       Returns:
       str: A string containing the random cat fact, or an error message.
       """
    try:
        response = requests.get('https://catfact.ninja/fact')
        if response.status_code == 200:
            data = response.json()
            return data['fact']
        else:
            return f"Failed to retrieve cat fact. Error code: {response.status_code}"
    except requests.exceptions.RequestException:
        return "Sorry, I couldn't retrieve a cat fact right now. Please try again later."
