from flask_login import login_required
from cruddy.login import login, logout, authorize
from __init__ import app
from cruddy.app_crud import app_crud
from flask import redirect, request, url_for

app.register_blueprint(app_crud)
from cruddy.att_crud import app_attend

app.register_blueprint(app_attend)

from cruddy.app_notes import app_notes

app.register_blueprint(app_notes)

from flask import render_template, send_from_directory
from __init__ import app, login_manager

from uploady.app_upload import app_upload
app.register_blueprint(app_upload)

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
def guidelines():
    return render_template("events/guidlines.html")


@app.route('/shooting')
def shootings():
    return render_template("events/shootings.html")


@app.route('/emergencycontacts')
def emergencycontacts():
    return render_template("events/emergencycontacts.html")

# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    app.config['NEXT_PAGE'] = request.endpoint
    return redirect(url_for('main_login'))


# if login url, show phones table only
@app.route('/login/', methods=["GET", "POST"])
def main_login():
    # obtains form inputs and fulfills login requirements
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):
            try:  # try to redirect to next page
                next_page = app.config['NEXT_PAGE']
                app.config['NEXT_PAGE'] = None
                return redirect(url_for(next_page))
            except:  # any failure goes to home page
                return redirect(url_for('index'))

    # if not logged in, show the login page
    return render_template("login.html")


# if login url, show phones table only
@app.route('/logout/', methods=["GET", "POST"])
@login_required
def main_logout():
    logout()
    return redirect(url_for('index'))


# user authorize with password validation
@app.route('/authorize/', methods=["GET", "POST"])
def main_authorize():
    error_msg = ""
    # check form inputs and creates user
    if request.form:
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")  # password should be verified
        if password1 == password2:
            if authorize(user_name, email, password1):
                return redirect(url_for('main_login'))
        else:
            error_msg = "Passwords do not match"
    # show the auth user page if the above fails for some reason
    return render_template("authorize.html", error_msg=error_msg)


# serve uploaded files so they can be downloaded by users.
@app.route('/<name>')
def uploads_endpoint(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# register "uploads_endpoint" endpoint so url_for will find all uploaded files
app.add_url_rule("/" + app.config['UPLOAD_FOLDER'] + "/<name>", endpoint="uploads_endpoint", build_only=True)


if __name__ == "__main__":
    # runs the application on the repl development server
    app.run(debug=True, port="5224")
