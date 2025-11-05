# seed_data.py
import json
from app import create_app
from app.extensions import db
from app.models import Service, Testimonial, GalleryImage

app = create_app()

# Load JSON data
data = {
    "services": [
        {
            "name": "General Service",
            "slug": "general-service",
            "description": "Basic inspection and tune-up: oil top-up, chain check, brakes check.",
            "category": "Maintenance",
            "duration_minutes": 45,
            "base_price": 499,
            "image_url": "/static/images/service-general.jpg"
        },
        {
            "name": "Engine Repair",
            "slug": "engine-repair",
            "description": "Diagnosis and engine repair for common faults.",
            "category": "Repair",
            "duration_minutes": 180,
            "base_price": 3500,
            "image_url": "/static/images/service-engine.jpg"
        },
        {
            "name": "Brake & Wheel",
            "slug": "brake-wheel",
            "description": "Brake pad replacement, wheel alignment, tune.",
            "category": "Repair",
            "duration_minutes": 60,
            "base_price": 700,
            "image_url": "/static/images/service-brake.jpg"
        },
        {
            "name": "Battery Replacement",
            "slug": "battery-replacement",
            "description": "Battery testing and replacement with warranty.",
            "category": "Electrical",
            "duration_minutes": 30,
            "base_price": 1800,
            "image_url": "/static/images/service-battery.jpg"
        }
    ],
    "testimonials": [
        {"name": "Rahul", "text": "Quick and honest service!", "rating": 5, "approved": True},
        {"name": "Neha", "text": "Affordable and professional. My bike runs like new.", "rating": 4, "approved": True},
        {"name": "Vikram", "text": "They replaced my battery same-day. Highly recommended.", "rating": 5, "approved": True}
    ],
    "gallery": [
        {"title": "Shop Front", "image_url": "/static/images/shop-front.jpg", "caption": "MotorCare shop front"},
        {"title": "Engine Work", "image_url": "/static/images/engine-work.jpg", "caption": "Mechanic at work"}
    ]
}


with app.app_context():
    db.create_all()

    # --- Seed Services ---
    if not Service.query.first():
        for s in data["services"]:
            db.session.add(Service(**s))
        print("✅ Services added")

    # --- Seed Testimonials ---
    if not Testimonial.query.first():
        for t in data["testimonials"]:
            db.session.add(Testimonial(**t))
        print("✅ Testimonials added")

    # --- Seed Gallery Images ---
    if not GalleryImage.query.first():
        for g in data["gallery"]:
            db.session.add(GalleryImage(**g))
        print("✅ Gallery images added")

    db.session.commit()
    print("🎉 Database seeding complete!")
