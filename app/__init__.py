import os
from flask import Flask
from app.extensions import db, migrate, assets, init_assets, bcrypt
from app.models import User
from app.helpers import gravatar_for, logged_in, current_user


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Use environment variable fallback for SECRET_KEY
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "supersecretkey")

    # Enable debug mode automatically when FLASK_ENV=development
    if os.environ.get("FLASK_ENV") == "development":
        app.config["DEBUG"] = True

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    init_assets(app)
    bcrypt.init_app(app)

    # Import models so Alembic can detect them
    from app import models  # noqa

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.sessions import sessions_bp
    from app.routes.users import users_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(users_bp)

    # Make template helpers globally available
    app.jinja_env.globals.update(
        gravatar_for=gravatar_for,
        logged_in=logged_in,
        current_user=current_user,
    )

    # Initialize DB and create default admin ONLY if not testing
    if not app.config.get("TESTING", False):
        with app.app_context():
            _init_db_and_create_default_admin()

    return app


def _init_db_and_create_default_admin():
    """Ensure tables exist before creating a default admin."""
    # Create all tables if they don't exist yet (safe even if using migrations)
    db.create_all()

    # Check if admin user exists
    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(name="Admin", email="admin@example.com")
        admin.set_password("changeme123")
        db.session.add(admin)
        db.session.commit()
