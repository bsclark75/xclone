from tests.utils import get_user_count, login, create_user

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

def test_should_redirect_destroy_if_not_logged_in(client, test_user):
    before_count = get_user_count

    # Perform the delete request
    response = client.delete(f"/users/{test_user.id}")

    # Get count after
    after_count = get_user_count

    # Assert no difference
    assert before_count == after_count

def test_should_redirect_destroy_if_not_admin(client, test_user):
    """Test that deleting a user redirects if not admin."""
    user1, _ = create_user("Jane Doe", "jane.doe@example.com", "password123")
    login(client, user1.email, "password123")
    before_count = get_user_count()
    response = client.get(f"/users/{test_user.id}/delete", follow_redirects=True)
    #print(response.data)
    after_count = get_user_count()
    assert before_count == after_count
    assert b"You must be logged in to access this page." in response.data

