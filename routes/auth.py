from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from models import Users

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
                return redirect(url_for("student.dashboard"))
            elif user.role == "company":
                return redirect(url_for("company.dashboard"))
        else:
            return render_template("app_login.html", time=time, error="Invalid credentials!")

    return render_template("app_login.html", time=time, msg=msg)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))