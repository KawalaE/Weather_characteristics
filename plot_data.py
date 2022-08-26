import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime


db_name = "weatherdb"
table_name = "report"

with open('db_pass.txt') as f:
    DB_PASS = f.readline()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=DB_PASS,
    database=db_name
)
dbcursor = mydb.cursor()


def get_city_names():
    dbcursor.execute(f"SELECT DISTINCT city FROM {table_name}")
    return dbcursor.fetchall()


city_names = get_city_names()

cities_data = dict()


def get_data_for_each_city(cities: list):
    for city in cities:
        dbcursor.execute(f"SELECT * FROM {table_name} WHERE city='{city[0]}'")
        db_data = dbcursor.fetchall()
        times = []
        temperatures = []
        pressures = []
        humidities = []

        for instance in db_data:
            times.append(datetime.fromtimestamp(instance[1]))
            temperatures.append(instance[3] / 100)
            pressures.append(instance[4])
            humidities.append(instance[5])

        cities_data[city[0]] = times, temperatures, pressures, humidities


def draw_plot():

    for i in range(1, 4):

        plt.figure(figsize=(10, 6), tight_layout=True)
        plt.plot(cities_data["Cracow"][0], cities_data["Cracow"][i], 'o', cities_data['Warsaw'][0], cities_data['Warsaw'][i], 'o', cities_data['Poznan'][0], cities_data['Poznan'][i], 'o', cities_data['Wroclaw'][0], cities_data['Wroclaw'][i], 'o', linewidth=2, linestyle='dashed')

        if i == 1:
            plt.xlabel('Time')
            plt.ylabel('Temperature [°C]')
            plt.title('Time vs Temperature')

        if i == 2:
            plt.xlabel('Time')
            plt.ylabel('Pressure [hPa]')
            plt.title('Time vs Pressure')

        if i == 3:
            plt.xlabel('Time')
            plt.ylabel('Humidity [%]')
            plt.title('Time vs Humidity')

        plt.legend(title='cities', title_fontsize=13,
                   labels=cities_data.keys())
        plt.gcf().autofmt_xdate()
    plt.show()


get_data_for_each_city(city_names)
draw_plot()
