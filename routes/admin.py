from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from models import db, Users, Company, Student, Drive, Application

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
    companies    = Company.query.all()
    students     = Student.query.all()
    drives       = Drive.query.all()
    applications = Application.query.all()
    return render_template('admin/dashboard.html',
                           companies=companies,
                           students=students,
                           drives=drives,
                           applications=applications)


# ── Approve a company ───────────────────────────────────────
@admin_bp.route('/company/approve/<int:company_id>')
@login_required
@admin_required
def approve_company(company_id):
    company = Company.query.get(company_id)
    if company:
        company.approval = 'Active'
        db.session.commit()
    return redirect(url_for('admin.dashboard'))


# ── Blacklist a company ─────────────────────────────────────
@admin_bp.route('/company/blacklist/<int:company_id>')
@login_required
@admin_required
def blacklist_company(company_id):
    company = Company.query.get(company_id)
    if company:
        company.approval = 'Blacklisted'
        # also cancel all their drives
        Drive.query.filter_by(company_id=company.id).update({'status': 'Cancelled'})
        db.session.commit()
    return redirect(url_for('admin.dashboard'))


# ── Blacklist a student ─────────────────────────────────────
@admin_bp.route('/student/blacklist/<int:student_id>')
@login_required
@admin_required
def blacklist_student(student_id):
    student = Student.query.get(student_id)
    user    = Users.query.filter_by(username=student.student_email).first()
    if student:
        student.flag = 'Blacklisted'  # we'll use student flag column
        if user:
            user.flag = 'Inactive'
        db.session.commit()
    return redirect(url_for('admin.dashboard'))


# ── View a single drive ─────────────────────────────────────
@admin_bp.route('/drive/<int:drive_id>')
@login_required
@admin_required
def view_drive(drive_id):
    drive = Drive.query.get(drive_id)
    return render_template('admin/view_drive.html', drive=drive)


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