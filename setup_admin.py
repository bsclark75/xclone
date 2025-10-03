from app import create_app, db
from app.models import User
from datetime import datetime
from flask_migrate import upgrade


def setup_admin():
    app = create_app("config.ProductionConfig")
    with app.app_context():
            db.create_all()
            #upgrade()
            admin = User(
            name="Admin User",
            email="admin@example.com",
            admin=True,
            activated=True,
            activated_at=datetime.utcnow()
        )
            admin.set_password("password123")
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created.")
        

if __name__ == "__main__":
    setup_admin()
