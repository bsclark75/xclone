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