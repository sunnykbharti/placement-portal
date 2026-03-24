from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager
from models import db, Users

# ─── App & DB setup ───────────────────────────────────────────────
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travail.sqlite'
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)

# ─── Login manager ──────────────────────────────────────────────
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# ─── Register Blueprints ──────────────────────────────────────────
from routes.auth    import auth_bp
from routes.admin   import admin_bp
from routes.student import student_bp
from routes.company import company_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)


with app.app_context():
    db.create_all()
    # admin = Users(username="admin1", password="0", role="admin", flag="Active")
    # db.session.add(admin)
    # db.session.commit()
#---------------------------------------- Loading user --------------------------
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#------------------------------ when user enters the portal redirect to - 
@app.route('/')
def home():
     return render_template("company/create-drive.html")


if __name__ == '__main__':
    app.run(debug = True)