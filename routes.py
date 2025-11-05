from app import app
from flask import render_template
from app import app, db
from app.models import Service

@app.route('/')
def home():
    return "<h1>MotorCare is running fine 🚗</h1>"
from flask import render_template

@app.route("/services")
def services():
    all_services = Service.query.all()
    return render_template("services.html", services=all_services)

@app.route("/")
def home():
    from app.models import Service
    featured = Service.query.limit(3).all()
    return render_template("home.html", featured_services=featured)
