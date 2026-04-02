from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from models import db, Users, Company, Student, Drive, Application
from sqlalchemy import or_

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ── Helper: only admin can access ──────────────────────────
def admin_required(f):
    from functools import wraps
    from flask_login import current_user
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ── Dashboard (shows everything) ───────────────────────────
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    tot_company = Company.query.count()
    act_company = Company.query.filter_by(approval="Active").count()
    inact_company = Company.query.filter(Company.approval!="Active").count()

    tot_students = Student.query.count()
    act_students = Student.query.filter_by(status="Active").count()
    inact_students = Student.query.filter(Student.status!="Active").count()

    tot_drives = Drive.query.count()
    act_drives = Drive.query.filter_by(status="Active").count()
    inact_drives = Drive.query.filter(Drive.status!="Active").count()

    tot_applications = Application.query.count()
    short_applications = Application.query.filter_by(status="Accepted")

    return render_template('admin/summary.html',
                           tot_company=tot_company,
                           act_company=act_company,
                           inact_company=inact_company,
                           tot_students=tot_students,
                           act_students=act_students,
                           inact_students=inact_students,
                           tot_drives=tot_drives,
                           act_drives=act_drives,
                           inact_drives=inact_drives,
                           tot_applications=tot_applications,
                           short_applications=short_applications
                           )

@admin_bp.route('/company')
@login_required
@admin_required
def viewCompany():
    # company = Company.query.all()
    companies=[]
    query = request.args.get('name')
    if query :
       companies = Company.query.filter(
            or_(
                Company.company_name.contains(query),
                Company.id.contains(query),
                Company.hr_contact.contains(query)
            )
        ).all()
    else:
        companies = Company.query.all()
    return render_template('admin/companies.html',companies=companies)

@admin_bp.route('/student')
@login_required
@admin_required
def viewStudent():
    students=[]
    query = request.args.get('name')
    if query :
       students = Student.query.filter(
            or_(
                Student.student_name.contains(query),
                Student.id.contains(query),
                Student.student_phone.contains(query)
            )
        ).all()
    else:
        students = Student.query.all()
    return render_template('admin/students.html',students=students)

@admin_bp.route('/drive')
@login_required
@admin_required
def viewDrive():
    drives=[]
    query = request.args.get('name')
    if query :
       drives = Drive.query.filter(
            or_(
                Drive.title.contains(query),
                Drive.id.contains(query)
            )
        ).all()
    else:
        drives = Drive.query.all()
    return render_template('admin/drives.html',drives=drives)

@admin_bp.route('/applications')
@login_required
@admin_required
def viewApplication():
    applications=[]
    name = request.args.get('name')
    if name :
        applications = Application.query.filter(Application.student_id.ilike(f'%{name}%'))
    else:
        applications = Application.query.all()
    return render_template('admin/applications.html',applications=applications)

# ── Approve a company ───────────────────────────────────────
@admin_bp.route('/company/approve/<int:company_id>')
@login_required
@admin_required
def approve_company(company_id):
    company = Company.query.get(company_id)
    if company:
        company.approval = 'Active'
        db.session.commit()
    return redirect(url_for('admin.viewCompany'))


# ── Blacklist a company ─────────────────────────────────────
@admin_bp.route('/company/blacklist/<int:company_id>')
@login_required
@admin_required
def blacklist_company(company_id):
    company = Company.query.get(company_id)
    if company:
        company.approval = 'Blacklisted'
        Drive.query.filter_by(company_id=company.id).update({'status': 'Cancelled'})
        db.session.commit()
    return redirect(url_for('admin.viewCompany'))


# ── Blacklist a student ─────────────────────────────────────
@admin_bp.route('/student/blacklist/<int:student_id>')
@login_required
@admin_required
def blacklist_student(student_id):
    student = Student.query.get(student_id)
    user    = Users.query.filter_by(username=student.student_email).first()
    if student:
        student.status = 'Blacklisted'
        if user:
            user.flag = 'Inactive'
        db.session.commit()
    return redirect(url_for('admin.viewStudent'))

# -------------------Appriving Drive ---------------
@admin_bp.route('/company/approve/drive/<int:drive_id>')
@login_required
@admin_required
def approve_Drive(drive_id):
    drive = Drive.query.get(drive_id)
    if drive:
        drive.status = 'Active'
        db.session.commit()
    return redirect(url_for('admin.viewDrive'))

# -------------------Cancel Drive ---------------
@admin_bp.route('/company/cancel/drive/<int:drive_id>')
@login_required
@admin_required
def cancel_Drive(drive_id):
    drive = Drive.query.get(drive_id)
    if drive:
        drive.status = 'Cancelled By Admin'
        db.session.commit()
    return redirect(url_for('admin.viewDrive'))

# ── View a single drive ─────────────────────────────────────
@admin_bp.route('/drive/<int:drive_id>')
@login_required
@admin_required
def view_drive(drive_id):
    drive = Drive.query.get(drive_id)
    drive = Drive.query.get(drive_id)
    applications = Application.query.filter_by(drive_id=drive_id).all()
    students = []
    for application in applications:
        student = Student.query.get(application.student_id)
        students.append(student)
    return render_template("admin/view_drive.html", drive=drive, applications=applications, students=students)

# ── View a single application ───────────────────────────────
@admin_bp.route('/application/<int:app_id>')
@login_required
@admin_required
def view_application(app_id):
    application = Application.query.get(app_id)
    student     = Student.query.get(application.student_id)
    drive       = Drive.query.get(application.drive_id)
    return render_template('admin/view_application.html',
                           application=application,
                           student=student,
                           drive=drive)
