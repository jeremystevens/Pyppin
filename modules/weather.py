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


import requests
import os
from requests.exceptions import Timeout, TooManyRedirects, RequestException

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

"""
This module contains a function to fetch the current weather for a specified city.

The function uses the OpenWeatherMap API.

Functions:
fetch_weather: Fetches the current weather for a specified city.
"""

def handle_weather(city):
    """Get the weather for a given city."""
    try:
        response = requests.get(f"http://api.weatherstack.com/current?access_key={WEATHER_API_KEY}&query={city}", timeout=5)
        response.raise_for_status()
    except Timeout:
        return "Sorry, the request to get the weather information timed out. Please try again later."
    except TooManyRedirects:
        return "Sorry, your request for weather information was redirected too many times. Please try again later."
    except RequestException as e:
        return f"Sorry, there was an error with your request. Here's the error message: {str(e)}"
    except Exception as e:
        return f"Sorry, an unexpected error occurred: {str(e)}"

    data = response.json()

    if 'error' in data:
        return data['error']['info']

    return f"Weather in {data['location']['name']}: {data['current']['temperature']}°C, {data['current']['weather_descriptions'][0]}"
