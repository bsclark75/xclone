import pytest
from app import create_app, db
from app.models import User

@pytest.fixture(scope="function")
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"  # Use in-memory DB
    )

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

@pytest.fixture
def new_user(app):
    """Creates and returns a test user."""
    user = User(name="Brian Clark", email="brian@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_user(app):
    """Create a sample user for login tests."""
    user = User(name="John Doe", email="johndoe@example.com")
    user.set_password("password123")    
    db.session.add(user)
    db.session.commit()
    return user