from flask import render_template

from __init__ import app

from cruddy.app_crud import app_crud
app.register_blueprint(app_crud)

from cruddy.att_crud import app_attend
app.register_blueprint(app_attend)

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


@app.route('/BombThreat')
def BombThreat():
    return render_template("BombThreat.html")

@app.route('/Earthquakes')
def Earthquakes():
    return render_template("EarthquakesFires.html")

@app.route('/Floods')
def Floods():
    return render_template("Floods.html")

@app.route('/GeneralGuidelines')
def GeneralGuidelines():
    return render_template("GeneralGuidelines.html")

@app.route('/SchoolShootings')
def SchoolShootings():
    return render_template("SchoolShootings.html")

@app.route('/emergencycontacts')
def emergencycontacts():
    return render_template("emergencycontacts.html")

if __name__ == "__main__" :
    # runs the application on the repl development server
    app.run(debug=True, port="5224")

