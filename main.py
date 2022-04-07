from flask import render_template
from __init__ import app

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/attendance')
def attendance():
    return render_template("attendance/attendance.html")




if __name__ == "__main__":
    # runs the application on the repl development server
    app.run(debug=True, port="5222")
