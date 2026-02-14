from flask import Flask, flash, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from models import db, Users, Admin, Company, Student, Drive, Application

#---------------------------------------- Initialised my app & database ----------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travail.sqlite'
app.config["SECRET_KEY"] = "supersecretkey"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

#---------------------------------------- Loading user --------------------------
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#------------------------------ when user enters the portal redirect to - 
@app.route('/')
def home():
     return redirect(url_for("login"))

#---------------------------- Login page and authentication ------------------------
@app.route('/login', methods = ["GET","POST"])
def login():
    time=datetime.now()
    msg = request.args.get("message")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and user.password == password :
            login_user(user)
            return redirect(url_for("company_registration"))
        else:
            return redirect(url_for("company_registration"))
    return render_template("app_login.html",time=time)

#---------------------------- Company registration ---------------------------
@app.route('/register/company', methods = ["GET","POST"])
def company_registration():
    if request.method == "POST":
        company_name = request.form.get("company_name")
        hr_contact = request.form.get("hr_contact")
        website = request.form.get("website")
        company_email = request.form.get("company_email")
        location = request.form.get("location")
        password = request.form.get("password")

        existing_company = Company.query.filter_by(company_name=company_name).first()

        existing_user = Users.query.filter_by(username=company_email).first()

        # if not existing_company :
        #     newc = Company(company_name=company_name, hr_contact=hr_contact, website=website, company_email=company_email, location=location)

        #     db.session.add(newc)
            
        #     newu = Users(username=company_email, password=password, role="company")

        #     db.session.add(newu)
        #     db.session.commit()
        #     return redirect(url_for("login", message = "WELCOME"))
        if existing_user or existing_company:
            return render_template("form.html", error="This User already exists! Kindly Check the credentials and then try again.")
        
        try :
            newc = Company(company_name=company_name, hr_contact=hr_contact, website=website, company_email=company_email, location=location)

            db.session.add(newc)
            
            newu = Users(username=company_email, password=password, role="company")

            db.session.add(newu)
            db.session.commit()
            return redirect(url_for("login", message="Registered Successfully!, Kindly wait for Admin approval!"))
        except :
            db.session.rollback()
    return render_template("form.html")

#---------------------------- Student registration ---------------------------
@app.route('/register/student', methods = ["GET","POST"])
def student_registration():
    if request.method == "POST":
        student_name = request.form.get("student_name")
        student_phone = request.form.get("student_phone")
        student_email = request.form.get("student_email")
        date = request.form.get("dob")
        dob = datetime.strptime(date, '%Y-%m-%d').date()
        resume = request.form.get("resume")
        password = request.form.get("password")

        existing_student = Student.query.filter_by(student_name=student_name).first()

        existing_user = Users.query.filter_by(username=student_email).first()

        # if not existing_student :
        #     new_stud = Student(student_name=student_name, student_phone=student_phone, student_email=student_email, dob=dob, resume=resume)

        #     db.session.add(new_stud)
            
        #     newu = Users(username=student_email, password=password, role="student")

        #     db.session.add(newu)
        #     db.session.commit()
        #     return redirect(url_for("login", message = "WELCOME"))
        if existing_user or existing_student:
            return render_template("form.html", error="This User already exists! Kindly Check the credentials and then try again.")
        
        try :
            new_stud = Student(student_name=student_name, student_phone=student_phone, student_email=student_email, dob=dob, resume=resume)

            db.session.add(new_stud)
            
            new_user = Users(username=student_email, password=password, role="student")

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login", message="Registered Successfully!, Kindly wait for Admin approval!"))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return render_template("form.html", error="An error occurred.")
    return render_template("form.html")


if __name__ == '__main__':
    app.run(debug = True)