from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

"""This needs to be isolated to support blueprints and models"""
# Setup of key Flask object (app)
app = Flask(__name__)
dbURI = 'sqlite:///model/myDB.db'
UPLOAD_FOLDER = 'static/uploads/files/'
# Setup SQLAlchemy object and properties for the database (db)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Setup properties for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)
Migrate(app, db)

# Setup LoginManager object (app)
# LoginManager lets application and Flask-Login work together
login_manager = LoginManager()

# Configure application for login
login_manager.init_app(app)