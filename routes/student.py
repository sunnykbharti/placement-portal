from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from datetime import datetime
from models import db, Users, Student

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_name  = request.form.get("student_name")
        student_phone = request.form.get("student_phone")
        student_email = request.form.get("student_email")
        date          = request.form.get("dob")
        dob           = datetime.strptime(date, '%Y-%m-%d').date()
        resume        = request.form.get("resume")
        password      = request.form.get("password")

        existing_student = Student.query.filter_by(student_name=student_name).first()
        existing_user    = Users.query.filter_by(username=student_email).first()

        if existing_user or existing_student:
            return render_template("form.html", error="This User already exists! Kindly check the credentials and try again.")

        try:
            new_stud = Student(
                student_name=student_name,
                student_phone=student_phone,
                student_email=student_email,
                dob=dob,
                resume=resume
            )
            db.session.add(new_stud)

            new_user = Users(username=student_email, password=password, role="student")
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("auth.login", message="Registered Successfully! Kindly wait for Admin approval!"))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return render_template("form.html", error="An error occurred.")

    return render_template("form.html")


@student_bp.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("student/student_dashboard.html")