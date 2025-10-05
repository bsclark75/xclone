from app import create_app, db
from app.models import User

app = create_app('config.ProductionConfig')

with app.app_context():
    # Only create if doesn't exist
    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(
            name="Admin",
            email="admin@example.com",
            admin=True,
            activated=True
        )
        admin.set_password("password123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created.")
    else:
        print("⚠️ Admin user already exists.")
