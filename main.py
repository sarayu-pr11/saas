from flask_login import login_required
from flask import render_template, request, url_for, redirect
from query import *
from __init__ import app, login_manager


# Default URL for Blueprint
@app.route('/')
@login_required
def main():
    """obtains all Users from table and loads Admin Form"""
    return render_template("main.html")


# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized() :
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('main_login'))

# if login url, show phones table only
@app.route('/login/', methods=["GET", "POST"])
def main_login() :
    # obtains form inputs and fulfills login requirements
    if request.form :
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password) :  # zero index [0] used as email is a tuple
            return redirect(url_for('main'))
    # if not logged in, show the login page
    return render_template("login.html")


@app.route('/authorize/', methods=["GET", "POST"])
def main_authorize() :
    # check form inputs and creates user
    if request.form :
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password1")  # password should be verified
        if authorize(user_name, email, password1) :  # zero index [0] used as user_name and email are type tuple
            return redirect(url_for('main'))
    # show the auth user page if the above fails for some reason
    return render_template("authorize.html")


if __name__ == "__main__" :
    # runs the application on the repl development server
    app.run(debug=True, port="5223")
