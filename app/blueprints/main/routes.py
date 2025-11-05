# app/blueprints/main/routes.py
from flask import Blueprint, render_template
from app.models import Service, Testimonial

# Create the blueprint
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    """Home page showing active services and approved testimonials"""
    services = Service.query.filter_by(active=True).limit(6).all()
    testimonials = Testimonial.query.filter_by(approved=True).all()
    return render_template(
        "home.html",
        title="Welcome to MotorCare",
        services=services,
        testimonials=testimonials,
    )

@main_bp.route("/about")
def about():
    return render_template("about.html", title="About Us")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us")

@main_bp.route("/services")
def services():
    services = Service.query.filter_by(active=True).all()
    return render_template("services.html", services=services, title="Our Services")
