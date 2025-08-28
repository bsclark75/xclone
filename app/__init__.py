from flask import Flask
from .routes import main
from .extensions import db, assets, init_assets

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    init_assets(app)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main)

    return app
