from dotenv import load_dotenv
import requests
import os
from pprint import pprint

load_dotenv()

def get_current_weather(city="San Marcos", unit="imperial", state='TX', country='US'):
    """
    Get current weather data from OpenWeatherMap API.
    
    :param city: City name for weather data.
    :param unit: Unit for temperature ('imperial' for Fahrenheit, 'metric' for Celsius).
    :return: Weather data in JSON format.
    """
    if state == 'NA':
        

        request_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('API_KEY')}&units={unit}"
    else:
        request_url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={os.getenv('API_KEY')}&units={unit}"

    weather_data = requests.get(request_url).json()
    
    return weather_data


if __name__ == "__main__":
    print('\n*** Get Current Weather Conditions ***\n')

    city = input("\nPlease enter a city name: \n")
    state = input("\nPlease enter a state name: \n")
    unit = input("Choose temperature unit (C for Celsius, F for Fahrenheit): ").strip().lower()
    country = input("Country name: ").strip().lower()

    if not bool(city.strip()):
        city = "Lynnwood"
    
    if unit not in ['c', 'f']:
        unit = 'f'  # Default to Fahrenheit if invalid input

    weather_data = get_current_weather(city, 'metric' if unit == 'c' else 'imperial', state, country)

    print("\nWeather Data:")
    pprint(weather_data)
