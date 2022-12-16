import smbus2
import bme280
import time
import datetime
import requests

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

    humidity = data.humidity
    # pressure = data.pressure
    temperature = data.temperature

    time.sleep(30)

