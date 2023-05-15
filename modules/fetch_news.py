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

import os
import requests
from requests.exceptions import Timeout, TooManyRedirects, RequestException
from tqdm import tqdm

"""
This module contains a function to fetch the latest news articles.

The function uses the News API.

Functions:
fetch_news: Fetches the latest news articles.
"""

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def fetch_news(query):
    """
    Fetches the latest news articles.

    Args:
    query (str): Topic for news search.

    Returns:
    str: A string containing the latest news articles, or an error message.
    """
    try:
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Timeout:
        return "Sorry, the request for news timed out. Please try again."
    except TooManyRedirects:
        return "Sorry, the request for news encountered too many redirects."
    except RequestException as e:
        return f"Sorry, there was a problem with the request for news: {e}"

    data = response.json()
    articles = data['articles']
    if articles:
        results = []
        for article in tqdm(articles[:5], desc="Fetching news", ncols=80):  # Limit to the first 5 articles
            title = article['title']
            url = article['url']
            results.append(f"{title}\n{url}\n")
        return "\n".join(results)
    else:
        return f"No news articles found for '{query}'."
