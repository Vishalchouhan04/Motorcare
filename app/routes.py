from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Service, Booking, Testimonial
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    services = Service.query.limit(3).all()
    testimonials = Testimonial.query.all()
    return render_template('home.html', services=services, testimonials=testimonials)

@main_bp.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)
