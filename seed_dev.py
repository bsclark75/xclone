from flask_migrate import upgrade
from app import create_app, db
from app.models import User
from datetime import datetime
from faker import Faker
import os

fake = Faker()

def reset_and_seed(num_users=50):
    # Ensure you're using dev config
    app = create_app("config.DevelopmentConfig")
    with app.app_context():
        # Remove the existing database file manually (for SQLite)
        db_path = os.path.join(app.instance_path, "dev.db")
        if os.path.exists(db_path):
            os.remove(db_path)
            print("🗑️ Removed old dev.db")

        # Run migrations to rebuild tables
        upgrade()

        # Seed the database
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
