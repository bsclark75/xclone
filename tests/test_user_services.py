def test_should_sign_up_page(client):
    """Test that the sign-up page loads correctly."""
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_show_user(client, test_user):
    """Test that the user profile page loads correctly."""
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert bytes(test_user.name, 'utf-8') in response.data

def test_should_redirect_index_if_not_logged_in(client, test_user):
    """Test that accessing user profile redirects if not logged in."""
    response = client.get(f"/users", follow_redirects=True)
    assert response.status_code == 200
    assert b"You must be logged in to access this page." in response.data
    assert b"Login" in response.data

