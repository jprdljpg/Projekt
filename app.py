from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import app_measure


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


class Task(db.Model):
    DATE = db.Column(db.String, nullable=False)
    TIME = db.Column(db.String, nullable=False)
    SENSOR_TEMP = db.Column(db.Float)
    SENSOR_HUM = db.Column(db.Integer)
    LIVE_TEMP = db.Column(db.Float)
    LIVE_HUM = db.Column(db.Integer)


@app.route("/todo", methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        task = Task(name=request.form["task"])
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('todo'))

    tasks = Task.query.all()
    return render_template("todo.html", tasks=tasks)