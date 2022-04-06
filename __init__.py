from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

"""This needs to be isolated to support blueprints and models"""
# Setup of key Flask object (app)
app = Flask(__name__)
dbURI = 'sqlite:///model/myDB.db'
# Setup properties for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)
Migrate(app, db)

# Setup LoginManager object (app)
# LoginManager lets application and Flask-Login work together
# code: login_manager = LoginManager()

# Configure application for login
# code: login_manager.init_app(app)