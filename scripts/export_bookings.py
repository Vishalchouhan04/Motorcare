"""
Export bookings to CSV.
Run: python scripts/export_bookings.py > bookings.csv
"""
import csv
from app import create_app
from app.extensions import db
from app.models import Booking

app = create_app()
app.app_context().push()

def export():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    writer = csv.writer(__import__("sys").stdout)
    writer.writerow(["id","customer_name","phone","email","vehicle_model","registration_no","date","time_slot","status","services","created_at"])
    for b in bookings:
        svc_names = "|".join([s.name for s in b.services])
        writer.writerow([b.id, b.customer_name, b.phone, b.email or "", b.vehicle_model or "", b.registration_no or "", b.date, b.time_slot or "", b.status, svc_names, b.created_at])

if __name__ == "__main__":
    export()
