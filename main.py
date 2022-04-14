from flask import render_template, request, url_for, redirect
from cruddy.query import *
from __init__ import app, login_manager
from flask_login import login_required, logout_user


# Default URL for Blueprint
@app.route('/')
def index():
    return render_template("index.html")



@app.route('/main')
@login_required
def main():
    """obtains all Users from table and loads Admin Form"""
    return render_template("student_security_html/main_student.html")


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
    return render_template("student_security_html/login_student.html")


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
    return render_template("student_security_html/authorize_student.html")




# Default URL for Blueprint
@app.route('/crud')
@login_required  # Flask-Login uses this decorator to restrict acess to logged in users
def crud():
    """obtains all Users from table and loads Admin Form"""
    return render_template("attendance_security_html/crud.html", table=users_all())


# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('crud_login'))


# if login url, show phones table only
@app.route('/login_aadya/', methods=["GET", "POST"])
def crud_login():
    # obtains form inputs and fulfills login requirements
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):       # zero index [0] used as email is a tuple
            return redirect(url_for('crud'))

    # if not logged in, show the login page
    return render_template("attendance_security_html/login.html")


@app.route('/authorize_aadya/', methods=["GET", "POST"])
def crud_authorize():
    # check form inputs and creates user
    if request.form:
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        phone = request.form.get("phone")
        password2 = request.form.get("password1")           # password should be verified
        if authorize(user_name, email, password1, phone):    # zero index [0] used as user_name and email are type tuple
            return redirect(url_for('crud_login'))
    # show the auth user page if the above fails for some reason
    return render_template("attendance_security_html/authorize.html")



@app.route('/logout_aadya/')
@login_required
def crud_logout():
    logout_user()
    return redirect(url_for('crud'))

# CRUD create/add
@app.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = Users(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("phone")
        )
        po.create()
    return redirect(url_for('crud.crud'))


# CRUD read
@app.route('/read_aadya/', methods=["POST"])
def read():
    """gets userid from form and obtains corresponding data from Users table"""
    table = []
    if request.form:
        userid = request.form.get("userid")
        po = user_by_id(userid)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("attendance_security_html/crud.html", table=table)


# CRUD update
@app.route('/update_aadya/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        userid = request.form.get("userid")
        name = request.form.get("name")
        po = user_by_id(userid)
        if po is not None:
            po.update(name)
    return redirect(url_for('crud.crud'))


# CRUD delete
@app.route('/delete_aadya/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        userid = request.form.get("userid")
        po = user_by_id(userid)
        if po is not None:
            po.delete()
    return redirect(url_for('crud'))


# Search Form
@app.route('/search_aadya/')
def search():
    """loads form to search Users data"""
    return render_template("search.html")


# Search request and response
@app.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(users_ilike(term)), 200)
    return response


if __name__ == "__main__" :
    # runs the application on the repl development server
    app.run(debug=True, port="5223")