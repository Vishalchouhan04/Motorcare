"""
Seed script: populates the DB with sample services, testimonials, bookings, and admin user.
Run: python scripts/seed.py
"""
import json
import os
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Service, Testimonial, GalleryImage, Booking, User

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SEED_FILE = os.path.join(BASE_DIR, "seed_data.json")

app = create_app()
app.app_context().push()

def seed():
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Services
    for s in data.get("services", []):
        if not Service.query.filter_by(slug=s["slug"]).first():
            svc = Service(
                name=s["name"],
                slug=s["slug"],
                description=s.get("description"),
                category=s.get("category"),
                duration_minutes=s.get("duration_minutes"),
                base_price=s.get("base_price"),
                image_url=s.get("image_url"),
                active=True
            )
            db.session.add(svc)

    # Testimonials
    for t in data.get("testimonials", []):
        if not Testimonial.query.filter_by(name=t["name"], text=t["text"]).first():
            tt = Testimonial(
                name=t["name"],
                text=t["text"],
                rating=t.get("rating", 5),
                approved=t.get("approved", False)
            )
            db.session.add(tt)

    # Gallery
    for g in data.get("gallery", []):
        if not GalleryImage.query.filter_by(title=g["title"]).first():
            gi = GalleryImage(
                title=g["title"],
                image_url=g.get("image_url"),
                caption=g.get("caption")
            )
            db.session.add(gi)

    db.session.commit()

    # Admin user
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
    if not User.query.filter_by(username=admin_user).first():
        user = User(username=admin_user, password=generate_password_hash(admin_pass))
        db.session.add(user)
        db.session.commit()
        print(f"Created admin user: {admin_user}")

    # Sample bookings: create 3
    if not Booking.query.first():
        services = Service.query.limit(2).all()
        for i in range(3):
            b = Booking(
                customer_name=f"Customer {i+1}",
                phone=f"999000{i+1}00",
                email=f"customer{i+1}@example.com",
                vehicle_model="Hero Splendor",
                registration_no=f"MH12AB{i+1}234",
                date=date.today() + timedelta(days=i+1),
                time_slot="10:00-11:00",
                status="Pending",
                notes="Seed booking"
            )
            b.services = services
            db.session.add(b)
        db.session.commit()
        print("Created sample bookings")

    print("Seeding complete.")

if __name__ == "__main__":
    seed()
