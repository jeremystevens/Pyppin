import requests
from tqdm import tqdm
import os

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
      api_key (str): News API key.

      Returns:
      str: A string containing the latest news articles, or an error message.
      """

    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
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
    else:
        return f"Failed to fetch news articles. Error code: {response.status_code}"
