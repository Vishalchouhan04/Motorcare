from flask import Blueprint, render_template
from app.models import Service

services_bp = Blueprint('services', __name__, url_prefix='/services')

@services_bp.route('/')
def list_services():
    services = Service.query.all()
    return render_template('services.html', services=services)


@services_bp.route("/<slug>")
def service_detail(slug):
    svc = Service.query.filter_by(slug=slug, active=True).first_or_404()
    return render_template("service_detail.html", service=svc)
