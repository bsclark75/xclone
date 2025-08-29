from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_assets import Environment, Bundle
from flask_bcrypt import Bcrypt

# Initialize empty extension instances
db = SQLAlchemy()
migrate = Migrate()
assets = Environment()
bcrypt = Bcrypt()

def init_assets(app):
    """Initialize SCSS/Assets"""
    assets.init_app(app)

    scss = Bundle(
        "scss/main.scss",
        filters="libsass",
        output="css/style.css"
    )

    # Avoid duplicate registration error
    if 'scss_all' not in assets:
        assets.register('scss_all', scss)
