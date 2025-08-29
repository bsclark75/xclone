from flask import Flask
from app.extensions import db, migrate, assets, init_assets

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    init_assets(app)

    # Import models so Alembic sees them
    from app import models

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app

