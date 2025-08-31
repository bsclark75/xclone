import os
from flask import Flask
from app.extensions import db, migrate, assets, init_assets, bcrypt
from app.models import User
from app.helpers import gravatar_for

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config["SECRET_KEY"] = "supersecretkey"  # Replace with something secure


    # Automatically enable debug if FLASK_ENV=development
    if os.environ.get("FLASK_ENV") == "development":
        app.config["DEBUG"] = True

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    init_assets(app)
    bcrypt.init_app(app)


    # Import models so Alembic sees them
    from app import models

    # Register blueprints
    from app.routes import main, sessions_bp
    app.register_blueprint(main)
    app.register_blueprint(sessions_bp)

    with app.app_context():
        db.create_all()
        # Check for default user
        if not User.query.filter_by(email="admin@example.com").first():
            default_user = User(name="Admin", email="admin@example.com")
            default_user.set_password("changeme123")
            db.session.add(default_user)
            db.session.commit()

    # Make helper available inside templates
    app.jinja_env.globals.update(gravatar_for=gravatar_for)
    return app

