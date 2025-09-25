import pytest
from app import create_app, db
from config import TestConfig
from app.models import User

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
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

@pytest.fixture
def admin_user(app):
    """Creates and returns a test user."""
    user = User(name="Brian Clark", email="brian@example.com", admin=True, activated= True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_user(app):
    """Create a sample user for login tests."""
    user = User(name="John Doe", email="johndoe@example.com")
    user.set_password("password123")
    user.activated = True    
    db.session.add(user)
    db.session.commit()
    return user