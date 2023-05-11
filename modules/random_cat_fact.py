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
