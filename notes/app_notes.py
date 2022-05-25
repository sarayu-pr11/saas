import markdown
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from cruddy.query import user_by_id
from cruddy.model import Notes

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_notes = Blueprint('notes', __name__,
                      url_prefix='/notes',
                      template_folder='notes/',
                      static_folder='static',
                      static_url_path='static')


@app_notes.route('/notes')
@login_required
def notes():
    # defaults are empty, in case user data not found
    user = ""
    list_notes = []

    # grab user database object based on current login
    uo = user_by_id(current_user.userID)

    # if user object is found
    if uo is not None:
        user = uo.read()  # extract user record (Dictionary)
        for notes in uo.notes:  # loop through each user note
            notes = notes.read()  # extract note record (Dictionary)
            notes['note'] = markdown.markdown(notes['note'])  # convert markdown to html
            list_notes.append(notes)  # prepare note list for render_template
        if list_notes is not None:
            list_notes.reverse()
    # render user and note data in reverse chronological order
    return render_template('', user=user, notes=list_notes)


# Notes create/add
@app_notes.route('/create/', methods=["POST"])
@login_required
def create():
    """gets data from form and add to Notes table"""
    if request.form:
        # construct a Notes object
        notes_object = Notes(
            request.form.get("notes"), current_user.userID
        )
        # create a record in the Notes table with the Notes object
        notes_object.create()
    return redirect(url_for('notes.notes'))
