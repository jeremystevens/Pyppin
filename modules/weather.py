import requests
import math
import os
"""
This module contains a function to fetch the current weather for a specified city.

The function uses the OpenWeatherMap API.

Functions:
fetch_weather: Fetches the current weather for a specified city.
"""


# Replace Your OpenWeathermap.org API Key
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
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

def handle_weather(city):
    """
        Fetches the current weather for a specified city.

        Args:
        city (str): Name of the city for which to get the weather.
        api_key (str): OpenWeatherMap API key.

        Returns:
        str: A string describing the weather in the city, or an error message.
        """
    #print(f"Debug: In get_weather, city = '{city}'")
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature_k = data['main']['temp']
        temperature_f = math.ceil((9 / 5) * (temperature_k - 273) + 32)
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        return f'The weather in {city} is {description} with a temperature of {temperature_f} °F and a humidity of {humidity}%.'

    return f'Request failed with error code {response.status_code}.'
