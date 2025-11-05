# app/models.py
from datetime import datetime
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------
# SERVICE MODEL
# -------------------------------
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    duration_minutes = db.Column(db.Integer)
    base_price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Service {self.name}>"

# -------------------------------
# MANY-TO-MANY RELATIONSHIP TABLE
# -------------------------------
booking_services = db.Table(
    "booking_services",
    db.Column("booking_id", db.Integer, db.ForeignKey("booking.id"), primary_key=True),
    db.Column("service_id", db.Integer, db.ForeignKey("service.id"), primary_key=True),
)

# -------------------------------
# BOOKING MODEL
# -------------------------------
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120))
    vehicle_model = db.Column(db.String(100))
    registration_no = db.Column(db.String(50))
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Pending")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Many-to-many with services
    services = db.relationship(
        "Service",
        secondary=booking_services,
        backref=db.backref("bookings", lazy="dynamic")
    )

    def __repr__(self):
        return f"<Booking {self.customer_name} - {self.date}>"

# -------------------------------
# TESTIMONIAL MODEL
# -------------------------------
class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    text = db.Column(db.Text)
    rating = db.Column(db.Integer)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------------------
# GALLERY IMAGE MODEL
# -------------------------------
class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    image_url = db.Column(db.String(255))
    caption = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------------------
# MECHANIC MODEL
# -------------------------------
class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    specialty = db.Column(db.String(200))
    profile_image = db.Column(db.String(255))
    bio = db.Column(db.Text)

# -------------------------------
# ADMIN USER MODEL
# -------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
