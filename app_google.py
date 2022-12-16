from flask import Flask, render_template
from measure import login_open_sheet, GDOCS_OAUTH_JSON, GDOCS_SS

app = Flask(__name__)
app.debug = True


worksheet = None
if worksheet is None:
    worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SS)


@app.route("/")
def hello():
    return "Hello World"


@app.route("/app")
def measure():
    ws_data = worksheet.get_all_records()


    if ws_data.pop()['SENSOR HUMIDITY'] is not None and ws_data.pop()['SENSOR TEMPERATURE'] is not None and ['SENSOR PRESSURE'] is not None:
        return render_template("lab_temp.html", temp=ws_data.pop()['SENSOR TEMPERATURE'], hum=ws_data.pop()['SENSOR HUMIDITY'], api_temp=ws_data.pop()['LIVE TEMPERATURE'], api_hum=ws_data.pop()['LIVE HUMIDITY'])
    else:
        return render_template("no_sensor.html")

