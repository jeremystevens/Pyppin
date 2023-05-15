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
This module contains a function to fetch a random quote.

The function uses the Quotable API.

Functions:
get_random_quote: Fetches a random quote.
"""

def get_random_quote():
    """
       Fetches a random quote.

       Args:
       api_key (str): Quotable API key.

       Returns:
       str: A string containing the random quote, or an error message.
       """
    try:
        url = "https://quote-garden.onrender.com/api/v3/quotes/random"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            quote_text = data['data'][0]['quoteText']
            quote_author = data['data'][0]['quoteAuthor']
            return f'"{quote_text}" - {quote_author}'
        else:
            return "Sorry, I couldn't fetch a quote right now."
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"Error occurred: {e}")
        return "Sorry, I couldn't fetch a quote right now."
