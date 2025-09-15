import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True  # Rebuild automatically when files change
    MAIL_BACKEND = "console"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
