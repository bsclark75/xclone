# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db  # <- use the same db as models

@pytest.fixture(scope="function")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # fresh DB per test
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def db_session(app):
    # Tables are already created in app(); just yield the session
    try:
        yield db.session
    finally:
        db.session.rollback()
