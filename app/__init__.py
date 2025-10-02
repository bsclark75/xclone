import os
from flask import Flask
from app.extensions import *
from app.helpers import gravatar_for, logged_in, current_user

def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=True)

    # Pick config
    if config_class:
        app.config.from_object(config_class)
    else:
        env = os.environ.get("FLASK_ENV", "production").lower()
        if env == "development":
            app.config.from_object("config.DevelopmentConfig")
        elif env == "testing":
            app.config.from_object("config.TestingConfig")
        else:
            app.config.from_object("config.ProductionConfig")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    init_assets(app)
    bcrypt.init_app(app)
    mailer.init_app(app)

    from app import models  # noqa

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

    app.jinja_env.globals.update(
        gravatar_for=gravatar_for,
        logged_in=logged_in,
        current_user=current_user,
    )

    return app
