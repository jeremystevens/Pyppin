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

def handle_weather():
    """
        Fetches the current weather for a specified city.

        Args:
        city (str): Name of the city for which to get the weather.
        api_key (str): OpenWeatherMap API key.

        Returns:
        str: A string describing the weather in the city, or an error message.
        """
    city = input("Enter the City Name: ")
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
