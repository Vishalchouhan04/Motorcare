MotorCare - Flask (Full scaffold)
================================

Quick start (local dev)
-----------------------
1. Clone repo and cd into project:
   cd motorcare-flask

2. Create virtualenv and install:
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate      # windows
   pip install -r requirements.txt

3. Copy .env.example -> .env and edit values:
   cp .env.example .env

4. Initialize DB + migrations:
   export FLASK_APP=run.py
   flask db init
   flask db migrate -m "init"
   flask db upgrade

5. Seed sample data:
   python scripts/seed.py

6. Run app:
   python run.py
   Open http://127.0.0.1:5000

Admin
-----
- Default admin creds come from .env: ADMIN_USERNAME and ADMIN_PASSWORD (seed creates admin user).
- Admin routes under /admin. Login page for admin: /admin/login

Deployment notes
----------------
- Use environment variables for SECRET_KEY and DATABASE_URL (Postgres).
- Use Gunicorn for production:
  Procfile: web: gunicorn run:app
- Use S3 or similar for serving media in production.

Features present
----------------
- Home, Services, Booking, Contact, About, Gallery (simple)
- Admin: manage bookings list (simple auth), CSV export
- Models: Service, Booking (m2m), Testimonial, GalleryImage, Mechanic, User (admin)
- Seed script and seed_data.json

