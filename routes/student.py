from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from models import db, Users, Student, Drive, Company, Application
import os
from werkzeug.utils import secure_filename

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_name = request.form.get("student_name")
        student_phone = request.form.get("student_phone")
        student_email = request.form.get("student_email")
        date = request.form.get("dob")
        dob = datetime.strptime(date, '%Y-%m-%d').date()
        resume = request.form.get("resume")
        password = request.form.get("password")

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

            return redirect(url_for("auth.login", message="Registered Successfully! Kindly Login!"))
        except Exception as e:
            db.session.rollback()
            return render_template("form.html", error=f'An error occurred, Kindly check your details.')

    return render_template("form.html")

#---------------- wrapper function to allow only student access ---------------
def student_required(f):
    from functools import wraps
    from flask_login import current_user
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

#----------------- Student DashBoard -----------------------
@student_bp.route('/dashboard', methods=["GET", "POST"])
@login_required
@student_required
def dashboard():
    message = request.args.get("message")
    return render_template("student/dashboard.html",message=message)

#--------------------Update Profile -------------------
@student_bp.route('/profile/update', methods=["GET", "POST"])
@login_required
@student_required
def update():
    student = Student.query.filter_by(student_email=current_user.username).first()

    if request.method == "POST":
        student.student_name = request.form.get("name")
        student.student_phone = request.form.get("phone")
        student.student_email = request.form.get("email")
        student_dob = request.form.get("dob")
        student.student_dob = datetime.strptime(student_dob, '%Y-%m-%d').date()

        current_user.username = request.form.get("email")
        db.session.commit()
        return redirect(url_for('auth.logout'))
    return render_template("student/update.html",student=student)

#-------------------- View Drives -----------------------
@student_bp.route('/drives/view', methods=["GET", "POST"])
@login_required
@student_required
def viewDrives():
    student = Student.query.filter_by(student_email=current_user.username).first()
    drives = db.session.query(Drive).outerjoin(
        Application, (Drive.id == Application.drive_id) & (Application.student_id == student.id)
        ).filter(
            Drive.status == "Active",
            Application.id == None
    ).all()
    return render_template("student/view-drives.html", drives=drives)

#---------------Apply for a Drive --------------------
@student_bp.route('/drives/apply/<int:drive_id>', methods=["GET", "POST"])
@login_required
@student_required
def apply(drive_id):
    student = Student.query.filter_by(student_email=current_user.username).first()
    drive = Drive.query.get(drive_id)
    company = Company.query.filter_by(id=drive.company_id).first()
    
    if request.method == "POST" :
        drive_id = drive_id
        student_id = student.id
        dateToday = datetime.today()
        try :
            
            new_application = Application(
                drive_id = drive_id,
                student_id = student_id,
                date = dateToday
            )
            db.session.add(new_application)
            db.session.commit()
            return redirect(url_for('student.dashboard', message="Successfully Applied for the Drive"))
        except Exception as e:
            db.session.rollback()
            return redirect(url_for('student.dashboard', message=e))

    return render_template("student/apply.html",student=student, drive=drive, company=company)
#----------------- Applied Drives -------------------
@student_bp.route('/applications', methods=["GET", "POST"])
@login_required
@student_required
def applications():
    student = Student.query.filter_by(student_email=current_user.username).first()
    applied = Application.query.filter_by(student_id=student.id).all()
    return render_template("student/applications.html", applied=applied)

#------------------ Archives ------------------------
@student_bp.route('/applications/archives', methods=["GET", "POST"])
@login_required
@student_required
def archives():
    return render_template("student/archives.html")

#-------------Upload Resume ---------------------
import os
from werkzeug.utils import secure_filename

# This tells the app to look for a folder named 'resumes' inside 'static'
UPLOAD_FOLDER = os.path.join('static', 'resumes')
ALLOWED_EXTENSIONS = {'pdf'}

@student_bp.route('/upload-resume', methods=['GET', 'POST'])
@login_required
@student_required
def upload_resume():
    if request.method == 'POST':
        # 1. Validation check
        if 'resume_file' not in request.files:
            return "No file part", 400
        
        file = request.files['resume_file']
        
        if file and file.filename != '':
            # 2. Secure and save the file
            filename = secure_filename(f"{current_user.username}_resume.pdf")
            
            # Ensure folder exists
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
                
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            # 3. Update Database
            student = Student.query.filter_by(student_email=current_user.username).first()
            student.resume = filename
            db.session.commit()
            
            return redirect(url_for('student.dashboard', message="Resume Uploaded Successfully!"))

    # If GET request, show the upload form
    return render_template('student/upload-resume.html')