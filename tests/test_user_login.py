import pytest
from app import db
from app.models import User


@pytest.fixture
def new_user(app):
    """Creates and returns a test user."""
    user = User(name="Brian Clark", email="brian@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user

def login(client, email, password):
    """Helper to log in the test user."""
    return client.post(
        "/sessions",  # adjust if your route is different
        data=dict(email=email, password=password),
        follow_redirects=True
    )

# ✅ Test when user is NOT logged in
def test_header_for_logged_out_user(client):
    response = client.get("/")
    html = response.data.decode()
    assert "Log in" in html
    assert "Log Out" not in html
    assert "Users" not in html

# ✅ Test when user IS logged in
def test_header_for_logged_in_user(client, new_user):
    # Log in first
    login(client, "brian@example.com", "password123")

    response = client.get("/")
    html = response.data.decode()

    # Check navbar links
    assert "Log in" not in html
    assert "Log Out" in html
    assert "Users" in html
    #assert new_user.name in html  # Verify current_user's name is displayed

def test_successful_signup_auto_login(client):
    """Test that a new user is automatically logged in after signup."""
    # Send POST request to /signup with valid data
    response = client.post(
        "/signup",
        data={
            "name": "Auto Login",
            "email": "autologin@example.com",
            "password": "securepass123",
            "confirm_password": "securepass123"
        },
        follow_redirects=True
    )

    # Check that we were redirected to the user's profile page
    assert response.status_code == 200
    assert b"Auto Login" in response.data  # The profile page should display the user's name

    # Check flash message for successful signup + login
    assert b"Account created successfully! You are now logged in." in response.data

    # Verify user exists in the database
    user = User.query.filter_by(email="autologin@example.com").first()
    assert user is not None

    # Check session is active by looking for "Log Out" link instead of "Log In"
    assert b"Log Out" in response.data
    assert b"Log in" not in response.data