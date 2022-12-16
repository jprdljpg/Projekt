import sys
import smbus2
import bme280
import time
import datetime
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
import threading

# connecting sensor
port = 1
address = 0x76
bus = smbus2.SMBus(port)

params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, params)

# collecting sensor data
#humidity = data.humidity
#pressure = data.pressure
#temperature = data.temperature

# scraping data from OpenWeather API
weather_key = 'f447b70e69dff8595b5017f8b474281f'
weather_url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + weather_key + '&q=Warsaw'

response = requests.get(weather_url)

resp = response.json()

if resp['cod'] != '404':
    api_data = resp['main']

    temp_api = float(api_data['temp']) - 273.15
    # temp_api = temp_api.replace('.', ',')
    hum_api = api_data['humidity']
    press_api = api_data['pressure']
else:
    print("ERROR 404")

# connecting to Google Sheets
GDOCS_OAUTH_JSON = '/var/www/app/google-auth.json'

GDOCS_SS = 'rpi'

worksheet = None


def login_open_sheet(key_file, ss):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(ss).sheet1
        print('Logged in-------------------')
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet')
        print('Google sheet login failed with:', ex)
        sys.exit(1)


if worksheet is None:
    worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SS)


# Sending data to Google Sheets
def send_data(worksheet):
    while True:
        try:
            humidity = data.humidity
            pressure = data.pressure
            temperature = data.temperature

            if worksheet.acell('A1').value is None:
                worksheet.insert_row(('DATE', 'TIME', 'SENSOR TEMPERATURE', 'SENSOR HUMIDITY', 'SENSOR PRESSURE',
                                      'LIVE TEMPERATURE', 'LIVE HUMIDITY', 'LIVE PRESSURE'), 1)

            worksheet.append_row((datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%H:%M:%S'),
                                "{0:0.1f}".format(temperature), "{0:0.0f}".format(humidity), "{0:0.0f}".format(pressure),
                                "{0:0.1f}".format(temp_api), hum_api, press_api), value_input_option='USER_ENTERED')

        except Exception as ex:
            print('Append error:', ex)
            worksheet = None

        time.sleep(30)


measure_thread = threading.Thread(target=send_data(worksheet))
measure_thread.start()
