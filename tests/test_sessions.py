import pytest
from app import create_app, db
from app.models import User
from tests.utils import create_user

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

def test_current_user_returns_right_user_when_session_is_none(client, test_user):
    """Test current_user returns the correct user when session is None but remember-me cookies exist."""
    # Generate a remember token for the test user
    test_user.remember()
    db.session.commit()

    with client:
        # Clear the session
        with client.session_transaction() as sess:
            sess.pop("user_id", None)

        # Set cookies to simulate remember-me
        client.set_cookie("user_id", str(test_user.id))
        client.set_cookie("remember_token", test_user.remember_token)

        # Hit a route that uses current_user
        response = client.get("/home")
        assert response.status_code == 200

        # Import current_user inside the request context
        from app.helpers import current_user
        assert current_user().id == test_user.id


def test_current_user_returns_none_when_remember_digest_is_wrong(client, test_user):
    # Generate a remember token for the test user
    test_user.remember()
    db.session.commit()

    with client:
        # Clear the session
        with client.session_transaction() as sess:
            sess.pop("user_id", None)

        # Set cookies to simulate remember-me
        client.set_cookie("user_id", str(test_user.id))
        client.set_cookie("remember_token", test_user.new_token())

        # Hit a route that uses current_user
        response = client.get("/home")
        assert response.status_code == 200

        # Import current_user inside the request context
        from app.helpers import current_user
        assert current_user() == None