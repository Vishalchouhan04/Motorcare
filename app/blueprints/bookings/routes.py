from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Service, Booking
from app.forms import BookingForm
import os

# Optional: Google Sheets Integration
import gspread
from google.oauth2.service_account import Credentials

bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")

# === Google Sheets Setup (optional) ===
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SHEET_NAME = "Prasad Auto Parts"

# Absolute path to credentials.json
CREDENTIALS_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../credentials.json")
)

sheet = None
try:
    print(f"🔍 Using credentials file: {CREDENTIALS_PATH}")
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1

    # Add header if missing
    if sheet.row_count == 0 or not sheet.row_values(1):
        sheet.append_row([
            "Customer Name", "Phone", "Email", "Vehicle Model",
            "Registration No", "Services", "Date", "Time Slot", "Notes"
        ])
    print(f"✅ Connected to Google Sheet: {SHEET_NAME}")
except Exception as e:
    print("⚠️ Google Sheets not connected:", e)


# === ROUTE: Booking Form ===
@bookings_bp.route("/new", methods=["GET", "POST"])
def book_service():
    print("🟢 Entered /bookings/new route")

    form = BookingForm()

    # Load all active services dynamically
    services = Service.query.filter_by(active=True).all()
    form.services.choices = [(s.id, s.name) for s in services]

    # Debug: log when POST request is received
    if request.method == "POST":
        print("📩 Raw POST Data:", request.form)

    # Validation failed
    if request.method == "POST" and not form.validate():
        print("❌ Form validation failed:", form.errors)
        flash("Please correct the errors in the form.", "danger")

    # If form passes validation
    if form.validate_on_submit():
        print("✅ Form validated successfully")

        # Debug print all data
        print("\n----- Booking Form Data -----")
        print(f"Customer Name: {form.customer_name.data}")
        print(f"Phone: {form.phone.data}")
        print(f"Email: {form.email.data}")
        print(f"Vehicle Model: {form.vehicle_model.data}")
        print(f"Registration No: {form.registration_no.data}")
        print(f"Selected Services: {form.services.data}")
        print(f"Date: {form.date.data}")
        print(f"Time Slot: {form.time_slot.data}")
        print(f"Notes: {form.notes.data}")
        print("-----------------------------\n")

        # Save to database
        selected_service_ids = form.services.data
        selected_services = Service.query.filter(Service.id.in_(selected_service_ids)).all()

        booking = Booking(
            customer_name=form.customer_name.data,
            phone=form.phone.data,
            email=form.email.data,
            vehicle_model=form.vehicle_model.data,
            registration_no=form.registration_no.data,
            date=form.date.data,
            time_slot=form.time_slot.data,
            notes=form.notes.data,
        )
        booking.services.extend(selected_services)

        db.session.add(booking)
        db.session.commit()
        print("✅ Booking saved to local database")

        # === Save booking to Google Sheets (if connected) ===
        try:
            global sheet
            if sheet:
                service_names = ", ".join([s.name for s in selected_services])
                row_data = [
                    form.customer_name.data,
                    form.phone.data,
                    form.email.data,
                    form.vehicle_model.data,
                    form.registration_no.data,
                    service_names,
                    str(form.date.data),
                    form.time_slot.data,
                    form.notes.data or "",
                ]
                sheet.append_row(row_data)
                print(f"✅ Booking also saved to Google Sheet: {row_data}")
            else:
                print("⚠️ Skipped Google Sheets: Not connected")
        except Exception as e:
            print("⚠️ Failed to write to Google Sheet:", e)

        flash("✅ Your booking has been successfully submitted!", "success")
        return redirect(url_for("main.home"))

    return render_template("booking.html", form=form)
