from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from models import Users, Student, Company

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    time = datetime.now()
    msg  = request.args.get("message")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)

            # Redirect based on role
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            elif user.role == "student":
                student = Student.query.filter_by(student_email=current_user.username).first()
                if student.status=="Active" :
                    return redirect(url_for("student.dashboard"))
                return redirect(url_for("auth.login", message=f'Status : {student.status}, Kindly contact Admin'))
            elif user.role == "company":
                company = Company.query.filter_by(company_email=current_user.username).first()
                if company.approval=="Active":
                    return redirect(url_for("company.dashboard"))
                return redirect(url_for("auth.login", message=f'Status : {company.approval}, Kindly contact Admin'))
        else:
            return render_template("app_login.html", time=time, error="Invalid credentials!")

    return render_template("app_login.html", time=time, message=msg)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login",message="You have successfully logged out!!!!!"))