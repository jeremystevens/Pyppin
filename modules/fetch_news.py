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

__version__ = '0.0.7'

import aiohttp
import asyncio
import os


"""
This module contains a function to fetch the latest news articles.

The function uses the News API.

Functions:
fetch_news: Fetches the latest news articles.
"""

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

async def fetch_news(query):
    """
    Fetches the latest news articles.

    Args:
    query (str): News search query.

    Returns:
    str: A string containing the latest news articles, or an error message.
    """
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    articles = data['articles']
                    if articles:
                        results = []
                        for article in articles[:5]:  # Limit to the first 5 articles
                            title = article['title']
                            url = article['url']
                            results.append(f"{title}\n{url}\n")
                        return "\n".join(results)
                    else:
                        return f"No news articles found for '{query}'."
                else:
                    return f"Failed to fetch news articles. Error code: {resp.status}"
    except aiohttp.ClientError as e:
        return f"Sorry, there was a problem with the request for news: {e}"
    except Exception as e:
        return f"Sorry, an unexpected error occurred: {e}"

# Then, to call this function, you would use asyncio.run in your main program like so:
# asyncio.run(fetch_news('Python'))  -<<--- only use is using python 3.7
