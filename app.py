from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import app_measure
import threading

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


class Measurements(db.Model):
    DATE = db.Column(db.String, nullable=False, primary_key=True)
    TIME = db.Column(db.String, nullable=False)
    SENSOR_TEMP = db.Column(db.Float)
    SENSOR_HUM = db.Column(db.Integer)
    LIVE_TEMP = db.Column(db.Float)
    LIVE_HUM = db.Column(db.Integer)


measure_thread = threading.Thread(target=app_measure.collect_data())
measure_thread.start()

@app.route("/todo", methods=['GET'])
def todo():
    #if request.method == 'POST':
        #task = Task(name=request.form["task"])
        #db.session.add(task)
        #db.session.commit()
        #return redirect(url_for('todo'))

    measurements = Measurements.query.all()
    return render_template("todo.html", tasks=measurements)