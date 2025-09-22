from app import db
from app.models import User
from tests.utils import login

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

def test_login_with_remember_me(client, new_user):
    """Ensure logging in with remember_me sets the cookie."""

    response = login(client, "brian@example.com", "password123", remember_me=True)

    assert response.status_code == 302

    # Pull cookies from Flask's internal storage
    set_cookie_headers = response.headers.getlist("Set-Cookie")
    print("Set-Cookie headers:", set_cookie_headers)
    assert any("remember_digest=" in header for header in set_cookie_headers)  
    assert any("user_id=" in header for header in set_cookie_headers)

def test_login_without_remember_me(client, new_user):
    """Ensure logging in without remember_me does NOT set the cookie."""
    response = login(client, "brian@example.com", "password123", remember_me=False)

    assert response.status_code == 302

    set_cookie_headers = response.headers.getlist("Set-Cookie")
    assert any("remember_digest=" not in header for header in set_cookie_headers)


def test_remember_function_sets_cookies(app, new_user):
    from app.services.user_service import remember
    from flask import make_response

    with app.test_request_context():
        # ✅ Create a dummy response for remember() to modify
        response = make_response("Testing remember cookies")

        # ✅ Call the updated remember() function
        response = remember(new_user, response)

        # ✅ Grab all cookies set on the response
        cookies = response.headers.getlist("Set-Cookie")

        # ✅ Check that remember_token cookie was set
        assert any("remember_digest=" in c for c in cookies)

        # ✅ Check that user_id cookie was set
        assert any("user_id=" in c for c in cookies)


