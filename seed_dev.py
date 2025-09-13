from faker import Faker
from app import create_app, db
from app.models import User
from datetime import datetime
#import random

fake = Faker()

def seed_users(num_users=99):
    app = create_app()

    with app.app_context():
        # Drop & recreate database tables (optional, uncomment if you want a clean DB)
        db.drop_all()
        db.create_all()
        print("Removing and recreating database")

        users = []
        user = User(name="Admin User",
                    email="admin@example.com",
                    admin=True,
                    activated=True,
                    activated_at=datetime.now())
        user.set_password("password123")
        users.append(user)

        for _ in range(num_users):
            name = fake.name()
            email = fake.unique.email()

            user = User(name=name, email=email, activated=True, activated_at=datetime.now())
            user.set_password("password123")  # Default password for all test users
            users.append(user)
            db.session.add(user)

        db.session.commit()
        print(f"✅ Successfully seeded {len(users)} random users into dev.db.")

if __name__ == "__main__":
    seed_users(99)
