
"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_restful import Api, Resource
import requests
from cruddy.att_model import attend

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_attend = Blueprint('attend', __name__,
                     url_prefix='/attend',
                     template_folder='templates/attend/',
                     static_folder='static',
                     static_url_path='assets')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(app_attend)

""" Application control for CRUD is main focus of this File, key features:
    1.) User table queries
    2.) app routes (Blueprint)
    3.) API routes
    4.) API testing
"""

""" attend table queries"""


# User/attend extraction from SQL
def users_all():
    #converts Users table into JSON list
    return [peep.read1() for peep in attend.query.all()]


def users_ilike(term):
    #filter attend table by term into JSON list 
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = attend.query.filter((attend.name.ilike(term)) | (attend.fav_res.ilike(term)))
    return [peep.read() for peep in table]


# User extraction from SQL
def user_by_id(userid):
    #finds User in table matching userid 
    return attend.query.filter_by(userID=userid).first()


# User extraction from SQL
def user_by_fav_food(fav_food):
    #finds User in table matching fav_res 
    return attend.query.filter_by(fav_food=fav_food).first()


""" app route section """


# Default URL
@app_attend.route('/at')
def crud1():
    """obtains all attend from table and loads Admin Form"""
    return render_template("attendance_security_html/crud_attendance.html", table=users_all())


# CRUD create/add
@app_attend.route('/at', methods=["POST"])
def create1():
    """gets data from form and add it to attend table"""
    if request.form:
        po = attend(
            request.form.get("fav_food"),
            request.form.get("fav_res"),
            request.form.get("name"),
        )
        po.create1()
    return redirect("at")


# CRUD read
@app_attend.route('/read_at', methods=["POST"])
def read1():
    """gets userid from form and obtains corresponding data from attend table"""
    table = []
    if request.form:
        userid = request.form.get("userid")
        po = user_by_id(userid)
        if po is not None:
            table = [po.read1()]  # placed in list for easier/consistent use within HTML
    return render_template("attendance_security_html/crud_attendance.html", table=table)


# CRUD update
@app_attend.route('/update_at/', methods=["POST"])
def update1():
    """gets userid and absent from form and filters and then data in  attend table"""
    if request.form:
        userid = request.form.get("userid")
        absent = request.form.get("absent")
        po = user_by_id(userid)
        if po is not None:
            po.update1(absent)
    return redirect(url_for('crud.crud'))


# CRUD delete
@app_attend.route('/delete_at/', methods=["POST"])
def delete1():
    """gets userid from form delete corresponding record from attend table"""
    if request.form:
        userid = request.form.get("userid")
        po = user_by_id(userid)
        if po is not None:
            po.delete1()
    return redirect(url_for('crud.crud'))


# Search Form
@app_attend.route('/search/')
def search1():
    """loads form to search attend data"""
    return render_template("search.html")


# Search request and response
@app_attend.route('/search/term/', methods=["POST"])
def search_term1():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(users_ilike(term)), 200)
    return response


""" API routes section """


class UsersAPI:
    # class for create/post
    class _Create(Resource):
        def post(self, name, fav_res, fav_food):
            po = attend(name, fav_res, fav_food)
            person = po.create()
            if person:
                return person.read()
            return {'message': f'Processed {fav_food}'}, 210

    # class for read/get
    class _Read(Resource):
        def get(self):
            return users_all()

    # class for read/get
    class _ReadILike(Resource):
        def get(self, term):
            return users_ilike(term)

    # class for update/put
    class _Update(Resource):
        def put(self, fav_food):
            po = user_by_fav_food(fav_food)
            if po is None:
                return {'message': f"{fav_food} is not found"}, 210
            po.update(fav_food)
            return po.read1()

    class _UpdateAll(Resource):
        def put(self, fav_food, name, password, phone):
            po = user_by_fav_food(fav_food)
            if po is None:
                return {'message': f"{fav_food} is not found"}, 210
            po.update(fav_food, password, phone)
            return po.read1()

    # class for delete
    class _Delete(Resource):
        def delete1(self, userid):
            po = user_by_id(userid)
            if po is None:
                return {'message': f"{userid} is not found"}, 210
            data = po.read()
            po.delete()
            return data

    # building RESTapi resource
    api.add_resource(_Create, '/create/<string:name>/<string:fav_res>/<string:password>/<string:phone>')
    api.add_resource(_Read, '/read/')
    api.add_resource(_ReadILike, '/read/ilike/<string:term>')
    api.add_resource(_Update, '/update/<string:fav_food>/<string:name>')
    api.add_resource(_UpdateAll, '/update/<string:fav_food>/<string:name>/<string:password>/<string:phone>')
    api.add_resource(_Delete, '/delete/<int:userid>')


""" API testing section """


def api_tester():
    # local host URL for model
    url = 'http://localhost:5222/crud'

    # test conditions
    API = 0
    METHOD = 1
    tests = [
        ['/create/Wilma Flintstone/wilma@bedrock.org/123wifli/0001112222', "post"],
        ['/create/Fred Flintstone/fred@bedrock.org/123wifli/0001112222', "post"],
        ['/read/', "get"],
        ['/read/ilike/John', "get"],
        ['/read/ilike/com', "get"],
        ['/update/wilma@bedrock.org/Wilma S Flintstone/123wsfli/0001112229', "put"],
        ['/update/wilma@bedrock.org/Wilma Slaghoople Flintstone', "put"],
        ['/delete/4', "delete"],
        ['/delete/5', "delete"],
    ]

    # loop through each test condition and provide feedback
    for test in tests:
        print()
        print(f"({test[METHOD]}, {url + test[API]})")
        if test[METHOD] == 'get':
            response = requests.get(url + test[API])
        elif test[METHOD] == 'post':
            response = requests.post(url + test[API])
        elif test[METHOD] == 'put':
            response = requests.put(url + test[API])
        elif test[METHOD] == 'delete':
            response = requests.delete(url + test[API])
        else:
            print("unknown RESTapi method")
            continue

        print(response)
        try:
            print(response.json())
        except:
            print("unknown error")


def api_printer():
    print()
    print("attend table")
    for user in users_all():
        print(user)


"""validating api's requires server to be running"""
if __name__ == "__main__":
    api_tester()
    api_printer()
