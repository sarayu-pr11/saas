"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response

from flask_login import login_required

from cruddy.query import *

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_student = Blueprint('student', __name__,
                     url_prefix='/crud',
                     template_folder='templates/cruddy/',
                     static_folder='static',
                     static_url_path='static')

@app_student.route('/main')
@login_required
def main():
    """obtains all Users from table and loads Admin Form"""
    return render_template("student_security_html/main_student.html")


# if login url, show phones table only
@app_student.route('/login_test/', methods=["GET", "POST"])
def main_login() :
    # obtains form inputs and fulfills login requirements
    if request.form :
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password) :  # zero index [0] used as email is a tuple
            return redirect(url_for('student.main'))
    # if not logged in, show the login page
    return render_template("student_security_html/login_student.html")

"""
# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized2() :
    #Redirect unauthorized users to Login page.
    return redirect(url_for('student.main_login'))
    
    """

@app_student.route('/authorize/', methods=["GET", "POST"])
def main_authorize() :
    # check form inputs and creates user
    if request.form :
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password1")  # password should be verified
        if authorize(user_name, email, password1) :  # zero index [0] used as user_name and email are type tuple
            return redirect(url_for('student.main'))
    # show the auth user page if the above fails for some reason
    return render_template("student_security_html/authorize_student.html")