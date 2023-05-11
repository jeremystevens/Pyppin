import requests
import math
import os
# Replace Your OpenWeathermap.org API Key
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def handle_weather():
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
