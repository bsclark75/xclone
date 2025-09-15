# seed_db.py
from flask_migrate import downgrade, upgrade
from app import create_app, db
from app.models import User
from datetime import datetime
from faker import Faker

fake = Faker()

def reset_and_seed(num_users=50):
    app = create_app()
    with app.app_context():
        # Roll back to base, then upgrade through all migrations
        downgrade("base")
        upgrade()

        # Seed users
        admin = User(
            name="Admin User",
            email="admin@example.com",
            admin=True,
            activated=True,
            activated_at=datetime.utcnow()
        )
        admin.set_password("password123")
        db.session.add(admin)

        for _ in range(num_users):
            u = User(
                name=fake.name(),
                email=fake.unique.email(),
                activated=True,
                activated_at=datetime.utcnow()
            )
            u.set_password("password123")
            db.session.add(u)

        db.session.commit()
        print(f"✅ Reset DB and seeded {num_users+1} users.")

if __name__ == "__main__":
    reset_and_seed()
