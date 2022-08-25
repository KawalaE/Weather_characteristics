import requests
import json
import mysql.connector
from time import time, sleep

with open('api_key.txt') as f:
    API_KEY = f.readline()

with open('db_pass.txt') as f:
    DB_PASS = f.readline()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=DB_PASS
)

print(mydb)

# Key: City, Value: (latitude, longitude)
cities = {
    "Cracow": (50.055375, 19.92981),
    "Warsaw": (52.233687, 21.009258),
    "Poznan": (52.409985, 16.897515),
    "Wroclaw": (51.107187, 17.031505)
}


def start_collecting_data():
    while 1:
        for city in cities:
            receive_data = get_data_from_server(cities[city][0], cities[city][1], API_KEY)
            ct, t, p, h = extract_data_from_response(receive_data)
            save_to_db(city, ct, t, p, h)
        sleep(5)


def save_to_db(c, ct, t, p, h):
    pass


def get_data_from_server(lat: float, lon: float, api_key: str) -> json:
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
    data = response.json()
    return data


def extract_data_from_response(response_data: json):
    temp = response_data["main"]["temp"] - 273.15 # convert from Kelvin to Celsius
    pressure = response_data["main"]["pressure"]
    humidity = response_data["main"]["humidity"]
    current_time = time()
    return int(current_time), int(temp*100), pressure, humidity

