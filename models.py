from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()

class Users(UserMixin, db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)
    flag = db.Column(db.String(200), default="Inactive")

class Admin(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.Integer, nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    dob = db.Column(db.Date, nullable = False)

class Company(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    contact = db.Column(db.Integer, nullable = False, unique = True)
    website = db.Column(db.String(100), nullable = False, unique = True)
    approval = db.Column(db.String(100), default="Inactive")

    drives = db.relationship('Drive', backref='company')

class Student(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.Integer, nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    dob = db.Column(db.Date, nullable = False)

    application = db.relationship('Application', backref = 'student')
    drive = db.relationship('Drive', backref = 'student')

class Drive(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable= False)
    eligibility = db.Column(db.String(500), nullable = False)
    deadline = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String(50), default = "Pending")

    application = db.relationship('Application', backref = 'drive')

class Application(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    date = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String(200), nullable = False, default = "Applied")
