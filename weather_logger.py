import requests
import json
import mysql.connector
from time import time, sleep, gmtime

starttime = time()
db_name = "weatherdb"
table_name = "report"

with open('api_key.txt') as f:
    API_KEY = f.readline()

with open('db_pass.txt') as f:
    DB_PASS = f.readline()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=DB_PASS,
  database=db_name
)
dbcursor = mydb.cursor()


def create_database_and_table():
    """
    Use only once to create database and table.
    :return:
    """
    dbcursor.execute(f"CREATE DATABASE {db_name}")
    dbcursor.execute(f"CREATE TABLE {table_name}("
                     f"id INT NOT NULL AUTO_INCREMENT,"
                     f"time INT,"
                     f"city VARCHAR(32),"
                     f"temperature INT,"
                     f"pressure INT,"
                     f"humidity INT,"
                     f"PRIMARY KEY (id))")


# Key: City, Value: (latitude, longitude)
cities = {
    "Cracow": (50.055375, 19.92981),
    "Warsaw": (52.233687, 21.009258),
    "Poznan": (52.409985, 16.897515),
    "Wroclaw": (51.107187, 17.031505)
}


def save_to_db(c, ct, t, p, h):
    sql_data_insert = f"INSERT INTO {table_name} (time, city, temperature, pressure, humidity) VALUES(%s,%s,%s,%s,%s)"
    values = (ct, c, t, p, h)
    dbcursor.execute(sql_data_insert, values)
    mydb.commit()
    show_time_stamp(ct)


def start_collecting_data():
    while True:
        for city in cities:
            receive_data = get_data_from_server(cities[city][0], cities[city][1], API_KEY)
            ct, t, p, h = extract_data_from_response(receive_data)
            save_to_db(str(city), ct, t, p, h)

        # Wait 900s (15min). A bit more accurate than just sleep(900)
        sleep(900.0 - ((time() - starttime) % 900.0))


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


def show_time_stamp(currenttime: int):
    t = gmtime(currenttime)
    print(f"{t.tm_mday}.{t.tm_mon}.{t.tm_year} / {t.tm_hour}:{t.tm_min} Database commit success!")


start_collecting_data()
