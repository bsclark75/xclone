from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy

assets = Environment()

def init_assets(app):
    assets.init_app(app)
    scss = Bundle("scss/main.scss",
                  filters="libsass",
                  output="css/style.css")
    if 'scss_all' not in assets:
        assets.register('scss_all', scss)

db = SQLAlchemy()
