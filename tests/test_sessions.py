import pytest
from app import create_app, db
from app.models import User
from tests.utils import create_user

@pytest.fixture
def test_user(app):
    """Create a sample user for login tests."""
    user = create_user(name="John Doe", email="johndoe@example.com", password="password123")
    
    db.session.add(user)
    db.session.commit()
    return user

def test_login_success(client, test_user):
    """Test logging in with valid credentials."""
    response = client.post("/sessions", data={
        "email": "johndoe@example.com",
        "password": "password123"
    }, follow_redirects=True)

    # ✅ Successful login should redirect to home page and flash success message
    assert response.status_code == 200
    assert b"Logged in successfully!" in response.data

def test_login_failure(client, test_user):
    """Test logging in with invalid credentials."""
    response = client.post("/sessions", data={
        "email": "johndoe@example.com",
        "password": "wrongpassword"
    }, follow_redirects=True)

    # ✅ Should flash danger message and stay on login page
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data
