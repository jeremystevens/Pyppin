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
