from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_user, logout_user, login_required, current_user
from ...forms import AdminLoginForm
from ...models import User, Booking
from ...extensions import db
import io, csv

admin_bp = Blueprint("admin", __name__, template_folder="../../templates")

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in", "success")
            return redirect(url_for("admin.bookings"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("admin_login.html", form=form)

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("main.home"))

@admin_bp.route("/bookings")
@login_required
def bookings():
    all_bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin_bookings.html", bookings=all_bookings)

@admin_bp.route("/bookings/<int:booking_id>/status", methods=["POST"])
@login_required
def change_status(booking_id):
    new_status = request.form.get("status")
    booking = Booking.query.get_or_404(booking_id)
    booking.status = new_status
    db.session.commit()
    flash("Status updated", "success")
    return redirect(url_for("admin.bookings"))

@admin_bp.route("/export/bookings.csv")
@login_required
def export_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id","customer","phone","email","vehicle","registration","date","time_slot","status","services","created_at"])
    for b in bookings:
        svc_names = "|".join([s.name for s in b.services])
        writer.writerow([b.id, b.customer_name, b.phone, b.email or "", b.vehicle_model or "", b.registration_no or "", b.date, b.time_slot or "", b.status, svc_names, b.created_at])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name="bookings.csv")
