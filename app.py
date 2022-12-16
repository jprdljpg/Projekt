from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


@app.route("/todo", methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        task = Task(name=request.form["task"])
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('todo'))

    tasks = Task.query.all()
    return render_template("todo.html", tasks=tasks)

