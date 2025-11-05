# app/__init__.py
from flask import Flask
from datetime import datetime
from config import Config
import os
import logging

logging.basicConfig(level=logging.INFO)

# Import uninitialized extensions
from app.extensions import db, migrate, login_manager, csrf


def create_app():
    """Flask application factory."""
    app = Flask(__name__, instance_relative_config=False)

    # --- Configuration ---
    app.config.from_object(Config)
    app.config.setdefault("SECRET_KEY", os.environ.get("SECRET_KEY", "devkey"))
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", os.environ.get("DATABASE_URL", "sqlite:///motorcare.db"))
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # --- Initialize extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # --- Register blueprints ---
    from app.blueprints.main.routes import main_bp
    from app.blueprints.bookings.routes import bookings_bp
    from app.blueprints.services.routes import services_bp
    from app.blueprints.admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(bookings_bp, url_prefix="/bookings")
    app.register_blueprint(services_bp, url_prefix="/services")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # --- Flask-Login setup ---
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = "admin.login"
    login_manager.login_message_category = "warning"

    # --- Context processor (inject current UTC time globally) ---
    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow()}

    # --- Create database tables automatically (for development only) ---
    with app.app_context():
        db.create_all()

    return app
