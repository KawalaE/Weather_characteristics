import requests
import json
from time import time

latitude = 50.055375
longitude = 19.92981

with open('api_key.txt') as f:
    API_KEY = f.readline()


def get_data_from_server(lat: float, lon: float, api_key: str) -> json:
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
    data = response.json()
    return data


#print(json.dumps(request.json(), indent=4))

def extract_data_from_response(response_data: json):
    temp = response_data["main"]["temp"] - 273.15 # convert from Kelvin to Celsius
    pressure = response_data["main"]["pressure"]
    humidity = response_data["main"]["humidity"]
    current_time = time()
    return current_time, temp, pressure, humidity


print(extract_data_from_response(get_data_from_server(latitude, longitude, API_KEY)))
