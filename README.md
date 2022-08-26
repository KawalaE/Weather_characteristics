# Weather_characteristics
Simple project using Matplotlib and MySQL to generate weather report.

Simple mini project in python created for future developement. 

weather_logger.py script reads current weather report data from following site: https://openweathermap.org, via
API, also is responsible for creating relational database in MySQL. Data from the site is formated and appended to the database every 15 minutes.

https://www.findlatitudeandlongitude.com - is used to get the longitude and latitude of particular cities: Poznan, Cracow, Warsaw and Wroclaw. 

plot_data.py script uses database created in weather_logger.py to plot characteristics via matplotlib module.

![time_vs_temp](https://user-images.githubusercontent.com/112077671/186935636-85c9d087-aa58-44c8-84ed-6b3651574202.JPG)
![time_vs_pressure](https://user-images.githubusercontent.com/112077671/186935646-b3e78bf5-7b0c-49c1-b9b9-f7d1ea7c49e1.JPG)
![time_vs_humidity](https://user-images.githubusercontent.com/112077671/186935654-f03a2f6a-7f27-4585-8861-d3c23090dffc.JPG)

