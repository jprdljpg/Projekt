import smbus2
import bme280
import time
import datetime
import requests
from app import Measurements, db

# connecting sensor
port = 1
address = 0x76
bus = smbus2.SMBus(port)

params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, params)


# connecting to weather API
weather_key = 'f447b70e69dff8595b5017f8b474281f'
weather_url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + weather_key + '&q=Warsaw'


def collect_data():
    response = requests.get(weather_url).json()

    if response['cod'] != '404':
        api_data = response['main']

        temp_api = float(api_data['temp']) - 273.15
        # temp_api = temp_api.replace('.', ',')
        hum_api = api_data['humidity']
        # press_api = api_data['pressure']
    else:
        print("ERROR 404")

    # humidity = data.humidity
    # pressure = data.pressure
    # temperature = data.temperature

    measurement = Measurements(DATE=datetime.datetime.now().strftime('%Y-%m-%d'),
                               TIME=datetime.datetime.now().strftime('%H:%M:%S'),
                               SENSOR_TEMP="{0:0.1f}".format(data.temperature),
                               SENSOR_HUM="{0:0.0f}".format(data.humidity),
                               LIVE_TEMP="{0:0.1f}".format(temp_api),
                               LIVE_HUM="{0:0.0f}".format(hum_api),
                               )
    db.session.add(measurement)
    db.session.commit()

    time.sleep(30)

