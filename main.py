from flask import render_template
from __init__ import app
from cruddy.app_crud import app_crud

app.register_blueprint(app_crud)
from cruddy.att_crud import app_attend

app.register_blueprint(app_attend)

from notey.app_notes import app_notes

app.register_blueprint(app_notes)

# Default URL for Blueprint
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about_us')
def about_us():
    return render_template("about_us.html")


@app.route('/quiz')
def quiz():
    return render_template("quiz.html")


@app.route('/maps')
def maps():
    return render_template("maps.html")


@app.route('/speech')
def speech():
    return render_template("speech.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/bomb')
def bomb():
    return render_template("events/bomb.html")


@app.route('/earthquake')
def Earthquakes():
    return render_template("events/earthquake.html")


@app.route('/fire')
def fire():
    return render_template("events/fire.html")


@app.route('/flood')
def flood():
    return render_template("events/flood.html")


@app.route('/guidelines')
def guidlines():
    return render_template("events/guidlines.html")


@app.route('/shooting')
def shootings():
    return render_template("events/shootings.html")


@app.route('/emergencycontacts')
def emergencycontacts():
    return render_template("events/emergencycontacts.html")


if __name__ == "__main__":
    # runs the application on the repl development server
    app.run(debug=True, port="5224")