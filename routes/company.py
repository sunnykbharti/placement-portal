from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Users, Company, Drive, Application, Student
from datetime import datetime

company_bp = Blueprint('company', __name__, url_prefix='/company')


@company_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        company_name = request.form.get("company_name")
        hr_contact = request.form.get("hr_contact")
        website = request.form.get("website")
        company_email = request.form.get("company_email")
        location = request.form.get("location")
        password = request.form.get("password")

        existing_company = Company.query.filter_by(company_name=company_name).first()
        existing_user = Users.query.filter_by(username=company_email).first()

        if existing_user or existing_company:
            return render_template("form.html", error="This User already exists! Kindly check the credentials and try again.")

        try:
            newc = Company(
                company_name = company_name,
                hr_contact = hr_contact,
                website = website,
                company_email = company_email,
                location = location
            )
            db.session.add(newc)

            newu = Users(username = company_email, password = password, role = "company")
            db.session.add(newu)
            db.session.commit()

            return redirect(url_for("auth.login", message="Registered Successfully! Kindly wait for Admin approval!"))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return render_template("form.html", error="An error occurred.")

    return render_template("form.html")

def company_required(f):
    from functools import wraps
    from flask_login import current_user
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'company':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

#------------------Company's Dashboard -------------------
@company_bp.route('/dashboard', methods=["GET", "POST"])
@login_required
@company_required
def dashboard():
    return render_template("company/dashboard.html")

#--------------------------- Create a new Drive --------------
@company_bp.route('/newDrive', methods=["GET", "POST"])
@login_required
@company_required
def newDrive():
    
    company = Company.query.filter_by(company_email=current_user.username).first()

    if company.approval != 'Active':
        return redirect(url_for('company.dashboard'))
    
    if request.method == "POST":
        name = request.form.get("name")
        title = request.form.get("title")
        description = request.form.get("description")
        eligibility = request.form.get("eligibility")
        deadline = request.form.get("deadline")
        deadline = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        company_id = company.id

        newdrive = Drive(name = name, 
                         title = title, 
                         description = description, 
                         eligibility = eligibility, 
                         deadline = deadline,
                         company_id = company_id
                         )
        db.session.add(newdrive)
        db.session.commit()
        
        return redirect(url_for("company.allDrives"))
    return render_template("company/create-drive.html")

# ── View ALL drives for this company ──────────────────
@company_bp.route('/drives')
@login_required
@company_required
def allDrives():
    company = Company.query.filter_by(company_email=current_user.username).first()
    drives  = Drive.query.filter_by(company_id=company.id).all()
    for d in drives:
        if d.deadline < datetime.now():
            d.status = "Deadline Passed"
    db.session.commit()
    upcoming_drives = Drive.query.filter(
        Drive.company_id==company.id,
        Drive.deadline>datetime.now()).all()
    return render_template("company/view-drives.html", upcoming_drives=upcoming_drives)

#---------------- View a Drive --------------
@company_bp.route('view/Drive/<int:drive_id>', methods=["GET", "POST"])
@login_required
@company_required
def viewDrive(drive_id):
    drive = Drive.query.get(drive_id)
    applications = Application.query.filter_by(drive_id=drive_id).all()
    students = []
    for application in applications:
        student = Student.query.get(application.student_id)
        students.append(student)
    return render_template("company/drive-details.html", drive=drive, applications=applications, students=students)

#---------------- Withdraw a Drive ------------
@company_bp.route('withdraw/Drive/<int:drive_id>', methods=["GET", "POST"])
@login_required
@company_required
def removeDrive(drive_id):
    drive = Drive.query.get(drive_id)
    if drive:
        drive.status = "Withdrawn By Company"
        db.session.commit()
    return redirect(url_for('company.allDrives'))

# --------------- Shortlist a application ------------------
@company_bp.route('approve/Application/<int:application_id>', methods=["GET", "POST"])
@login_required
@company_required
def approveApplication(application_id):
    application = Application.query.get(application_id)
    application.status="Shortlisted"
    db.session.commit()
    return redirect(url_for('company.allDrives'))
# --------------- Shortlist a application ------------------
@company_bp.route('reject/Application/<int:application_id>', methods=["GET", "POST"])
@login_required
@company_required
def rejectApplication(application_id):
    application = Application.query.get(application_id)
    application.status="Rejected"
    db.session.commit()
    return redirect(url_for('company.allDrives'))

@company_bp.route('/edit-drive/<int:drive_id>', methods=['GET', 'POST'])
@login_required
@company_required
def editDrive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    company = Company.query.filter_by(company_email=current_user.username).first()

    if request.method == 'POST':
        drive.name = request.form.get("name")
        drive.title = request.form.get("title")
        # Ensure you import datetime to parse the string from the form
        drive.deadline = datetime.strptime(request.form.get("deadline"), '%Y-%m-%dT%H:%M')
        
        db.session.commit()
        return redirect(url_for('company.allDrives'))

    return render_template('company/edit-drive.html', drive=drive)