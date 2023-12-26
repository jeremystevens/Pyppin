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

__version__ = "0.0.2"

import requests

"""
This module contains a function to perform a search on stack-overflow

The function uses the requests 

Functions:
handle_stack_overflow(query): Performs a search on stack-overflow.
"""

def search_stackoverflow(query):
    # Set up the API endpoint
    api_url = "https://api.stackexchange.com/2.3/search"

    # Parameters for the API request
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "intitle": query
    }

    # Send the API request
    response = requests.get(api_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Check if there are any results
        if data["items"]:
            # Retrieve the top voted answer
            top_answer = data["items"][0]
            
            # Extract the answer details
            answer_link = top_answer["link"]
            answer_votes = top_answer["score"]
            
            print(f"Top answer (votes: {answer_votes}):")
            return answer_link
        else:
            return "no results found sorry"
    else:
        return "an error occurred"
