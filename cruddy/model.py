
""" database dependencies to support Users db examples """

from random import randrange
from __init__ import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along

# Define the Users table within the model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL

class Notes(db.Model):
    __tablename__ = 'notes'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))

    #
    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, note, userID):
        self.note = note
        self.userID = userID

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "note": self.note,
            "userID": self.userID
        }


class Users(UserMixin, db.Model):
    # define the Users schema
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=False)
    notes = db.relationship("Notes", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, email, password, phone):
        self.name = name
        self.email = email
        self.set_password(password)
        self.phone = phone

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, password="", phone=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(password) > 0:
            self.set_password(password)
        if len(phone) > 0:
            self.phone = phone
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # set password method is used to create encrypted password
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # check password to check versus encrypted password
    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result

    # required for login_user, overrides id (login_user default) to implemented userID
    def get_id(self):
        return self.userID

def model_tester():
    print("--------------------------")
    print("Seed Data for Table: users")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    u1 = Users(name='Jo Buehler', email='jbuehler@stu.powayusd.com', password='123toby', phone="8749207684")
    u2 = Users(name='Melissa Darcey', email='mdarcey@stu.powayusd.com', password='123niko', phone="9064379065")
    u3 = Users(name='Brianna West', email='bwest@stu.powayusd.com', password='123lex', phone="7924670983")
    u4 = Users(name='Kenneth Ozuna', email='kozuna@stu.powayusd.com', password='123whit', phone="2684762094")
    u5 = Users(name='Frank Liao', email='fliao@stu.powayusd.com', password='123qwerty', phone="8587754956")
    u6 = Users(name='John Mortensen', email='jmortensen@stu.powayusd.com', password='123qwerty', phone="8587754956")
    # U7 intended to fail as duplicate key
    u7 = Users(name='James Lafferty', email='jlafferty@stu.powayusd.com', password='ur_mom', phone="8586791294")
    table = [u1, u2, u3, u4, u5, u6, u7]
    for row in table:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + row.name + " note " + str(num) + ". \n Generated by test data."
                row.notes.append(Notes(note=note, userID=row.userID))
            '''add user/note data to table'''
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {row.email}")


def model_printer():
    print("---------------------------")
    print("Create Tables and Seed Data")
    print("---------------------------")
    model_tester()

    print("---------------------------")
    print("Table: " + Users.__tablename__)
    print("Columns: ", Users.__table__.columns.keys())
    print("---------------------------")
    print("Table: " + Notes.__tablename__)
    print("Columns: ", Notes.__table__.columns.keys())
    print("---------------------------")
    print()

    users = Users.query
    for user in users:
        print("User" + "-" * 81)
        print(user.read())
        print("Notes" + "-" * 80)
        for note in user.notes:
            print(note.read())
        print("-" * 85)
        print()



if __name__ == "__main__":
    model_tester()
    model_printer()
