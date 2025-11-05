from app import create_app, db
from app.models import Service

app = create_app()
app.app_context().push()

# Clear old data
Service.query.delete()

# Sample service data
services = [
    Service(name="General Service", slug="general-service", description="Complete two-wheeler check-up, oil change, brake inspection, and cleaning.", category="General", base_price=499),
    Service(name="Engine Repair", slug="engine-repair", description="Engine tuning, part replacement, and performance optimization.", category="Engine", base_price=1499),
    Service(name="Brake & Wheel Service", slug="brake-wheel", description="Brake pad replacement, wheel alignment, and balancing.", category="Brake", base_price=799),
    Service(name="Electrical & Battery", slug="electrical-battery", description="Battery check, replacement, and electrical diagnostics.", category="Electrical", base_price=999),
    Service(name="Tyre & Tube Replacement", slug="tyre-tube", description="Quick tyre or tube replacement for all two-wheelers.", category="Tyres", base_price=699),
]

db.session.bulk_save_objects(services)
db.session.commit()
print("✅ Seeded sample services successfully!")
