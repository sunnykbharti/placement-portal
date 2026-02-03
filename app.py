from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("app_login.html")

if __name__ == '__main__':
    app.run(debug = True)