from flask import render_template, request, url_for, redirect
from cruddy.query import *
from __init__ import app
from flask_login import login_required


from cruddy.app_crud import app_crud
app.register_blueprint(app_crud)


# Default URL for Blueprint
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/quiz')
def quiz():
    return render_template("quiz.html")

@app.route('/attendance')
def attendance():
    return render_template("attendance_security_html/attendance.html")


if __name__ == "__main__" :
    # runs the application on the repl development server
    app.run(debug=True, port="5223")