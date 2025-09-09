from tests.utils import create_user, login

def test_unsuccessful_edit(client):
    user=create_user()
    login(client, user.email, "password123")
    resp=client.post(f"/users/{user.id}/edit", data={
        "name": "",  # Invalid: name cannot be empty
        "email": "invalid-email",  # Invalid email format
        "password": "short",  # Invalid: too short
        "confirm_password": "mismatch"  # Does not match password
    }, follow_redirects=True)
    html=resp.get_data(as_text=True)
    assert resp.status_code==200
    assert "Update your profile" in html

def test_should_redirect_update_when_not_logged_in(client):
    user=create_user()
    resp=client.post(f"/users/{user.id}/edit", data={
        "name": "",  # Invalid: name cannot be empty
        "email": "invalid-email",  # Invalid email format
        "password": "short",  # Invalid: too short
        "confirm_password": "mismatch"  # Does not match password
    }, follow_redirects=True)
    html=resp.get_data(as_text=True)
    assert resp.status_code==200
    assert "You must be logged in to access this page." in html
    assert "Login" in html    

def test_should_redirect_edit_when_not_logged_in(client):
    user=create_user()
    resp=client.get(f"/users/{user.id}/edit", follow_redirects=True)
    html=resp.get_data(as_text=True)
    assert resp.status_code==200
    assert "You must be logged in to access this page." in html
    assert "Login" in html

def test_successful_edit(client):
    user=create_user()
    login(client, user.email, "password123")
    resp=client.post(f"/users/{user.id}/edit", data={
        "name": "New Name",
        "email": "jdoe@example.com",
        "password": "",  # No password change
        "confirm_password": ""
    }, follow_redirects=True)
    html=resp.get_data(as_text=True)
    assert resp.status_code==200
    assert "User updated successfully!" in html
    assert "New Name" in html
    