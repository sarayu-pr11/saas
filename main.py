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

@app.route('/saumyaaboutme')
def saumyaaboutme():
    return render_template("aboutus/saumyaaboutme.html")



if __name__ == "__main__" :
    # runs the application on the repl development server
    app.run(debug=True, port="5223")

