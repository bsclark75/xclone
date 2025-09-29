import os
from flask import Flask
from app.extensions import *
#from app.models import User
from app.helpers import gravatar_for, logged_in, current_user


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object("config.Config")

    if config_class:
        app.config.from_object(config_class)

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
    mailer.init_app(app)

    # Import models so Alembic can detect them
    from app import models  # noqa

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.sessions import sessions_bp
    from app.routes.users import users_bp
    from app.routes.account_activations import aa_bp
    from app.routes.password_resets import password_reset_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(aa_bp)
    app.register_blueprint(password_reset_bp)

    # Make template helpers globally available
    app.jinja_env.globals.update(
        gravatar_for=gravatar_for,
        logged_in=logged_in,
        current_user=current_user,
    )

    return app

