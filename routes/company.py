from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models import db, Users, Company

company_bp = Blueprint('company', __name__, url_prefix='/company')


@company_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        company_name  = request.form.get("company_name")
        hr_contact    = request.form.get("hr_contact")
        website       = request.form.get("website")
        company_email = request.form.get("company_email")
        location      = request.form.get("location")
        password      = request.form.get("password")

        existing_company = Company.query.filter_by(company_name=company_name).first()
        existing_user    = Users.query.filter_by(username=company_email).first()

        if existing_user or existing_company:
            return render_template("form.html", error="This User already exists! Kindly check the credentials and try again.")

        try:
            newc = Company(
                company_name=company_name,
                hr_contact=hr_contact,
                website=website,
                company_email=company_email,
                location=location
            )
            db.session.add(newc)

            newu = Users(username=company_email, password=password, role="company")
            db.session.add(newu)
            db.session.commit()

            return redirect(url_for("auth.login", message="Registered Successfully! Kindly wait for Admin approval!"))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return render_template("form.html", error="An error occurred.")

    return render_template("form.html")


@company_bp.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("admin_dashbaord.html")