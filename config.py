import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, "instance")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Default DB (overridden in subclasses)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(instance_dir, "app.db")

    # Email (override in subclasses)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 25))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "false").lower() in ["true", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Flask-Mail console backend setting
    MAIL_BACKEND = "smtp"  # default, override in subclasses


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL", "sqlite:///" + os.path.join(instance_dir, "dev.db")
    )

    # Show emails in console
    MAIL_BACKEND = "console"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL", "sqlite:///" + os.path.join(instance_dir, "test.db")
    )

    # Allow choice: default console unless TEST_EMAIL is set
    MAIL_BACKEND = "console" if not os.environ.get("TEST_EMAIL") else "smtp"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("SQLALCHEMY_DATABASE_URI")
        or os.getenv("DATABASE_URL")
        or "sqlite:///xclone.db"
    )

    def __init__(self):
        if not self.SQLALCHEMY_DATABASE_URI:
            raise RuntimeError("DATABASE_URL must be set in production!")

    # Always real email
    MAIL_BACKEND = "smtp"
    MAIL_SERVER="mailhog"
    MAIL_PORT=1025
    MAIL_USE_TLS=False
    MAIL_USE_SSL=False
    MAIL_DEFAULT_SENDER="noreply@example.com"


