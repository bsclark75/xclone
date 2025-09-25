from tests.utils import create_user, login

def test_unsuccessful_edit(client, test_user):
    login(client, test_user.email, "password123")
    resp=client.post(f"/users/{test_user.id}/edit", data={
        "name": "",  # Invalid: name cannot be empty
        "email": "invalid-email",  # Invalid email format
        "password": "short",  # Invalid: too short
        "confirm_password": "mismatch"  # Does not match password
    }, follow_redirects=True)
    html=resp.get_data(as_text=True)
    print(html)
    assert resp.status_code==200
    assert "Update your profile" in html

def test_should_redirect_update_when_not_logged_in(client, test_user):
    resp=client.post(f"/users/{test_user.id}/edit", data={
        "name": "",  # Invalid: name cannot be empty
        "email": "invalid-email",  # Invalid email format
        "password": "short",  # Invalid: too short
        "confirm_password": "mismatch"  # Does not match password
    }, follow_redirects=True)
    html=resp.get_data(as_text=True)
    assert resp.status_code==200
    assert "You must be logged in to access this page." in html
    assert "Login" in html    

def test_should_redirect_edit_when_not_logged_in(client, test_user):
    resp=client.get(f"/users/{test_user.id}/edit", follow_redirects=True)
    html=resp.get_data(as_text=True)
    assert resp.status_code==200
    assert "You must be logged in to access this page." in html
    assert "Login" in html

def test_successful_edit(client, test_user):
    login(client, test_user.email, "password123")
    resp=client.post(f"/users/{test_user.id}/edit", data={
        "name": "New Name",
        "email": "jdoe@example.com",
        "password": "",  # No password change
        "confirm_password": ""
    }, follow_redirects=True)
    html=resp.get_data(as_text=True)
    assert resp.status_code==200
    assert "User updated successfully!" in html
    assert "New Name" in html

def test_should_redirect_edit_when_logged_in_as_wrong_user(client, test_user):
    user2, _ = create_user(name="Jane Doe", email="jane.doe@example.com")
    user2.activated = True
    login(client, user2.email, "password123")
    resp = client.get(f"/users/{test_user.id}/edit", follow_redirects=True)
    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "You do not have permission to access this page." in html
    assert "Home" in html

def test_should_redirect_update_when_logged_in_as_wrong_user(client, test_user):
    user2, _ = create_user(name="Jane Doe", email="jane.doe@example.com")
    user2.activated = True
    login(client, user2.email, "password123")
    resp = client.post(f"/users/{test_user.id}/edit", data={
        "name": "Hacker",
        "email": "jane.doe@example.com",
        "password": "",
        "confirm_password": ""
    }, follow_redirects=True)
    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "You do not have permission to access this page." in html
    assert "Home" in html

def test_successful_edit_with_friendly_forwarding(client, test_user):

    # Step 1: Try to access edit page while logged out → should redirect to login
    resp = client.get("/users/1/edit")
    assert resp.status_code == 302
    assert "/sessions/new" in resp.location

    # Step 2: Follow login flow, friendly forwarding should redirect us back
    resp = login(client, test_user.email, "password123")
    assert resp.status_code == 302
    assert resp.location.endswith(f"/users/{test_user.id}/edit")

    # Step 3: Now load the edit form
    resp = client.get(resp.location)
    assert resp.status_code == 200
    assert "Edit Profile" in resp.get_data(as_text=True)
    # Step 4: Submit valid changes
    resp = client.post(f"/users/{test_user.id}/edit", data={
        "name": "New Name",
        "email": "jdoe@example.com",
        "password": "",  # No password change
        "confirm_password": ""
    }, follow_redirects=True)
    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "User updated successfully!" in html
    assert "New Name" in html

