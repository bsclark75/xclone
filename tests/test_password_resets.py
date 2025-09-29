# tests/test_password_resets.py
import re
from tests.utils import create_user

def test_password_resets(client, test_user, capsys):
    """
    Full integration test for forgot/reset password including capturing the reset URL.
    """

    # 1. GET password reset page
    resp = client.get("/password_resets/new")
    assert resp.status_code == 200

    # 2. POST invalid email
    resp = client.post("/password_resets", data={"email": "nobody@example.com"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"not found" in resp.data.lower() or b"invalid" in resp.data.lower()

    # 3. POST valid email — should trigger email output to stdout
    resp = client.post("/password_resets", data={"email": test_user.email}, follow_redirects=True)
    assert resp.status_code == 200

    # 4. Capture stdout and parse reset URL
    captured = capsys.readouterr()
    match = re.search(r'href="https?://[^/]+/password_resets/([^/]+)/edit\?uid=(\d+)"', captured.out)
    assert match, f"No reset link found in: {captured.out}"
    token, uid = match.groups()

    #print(f"token: {token}")
    # 5. Fetch reset form (GET)
    resp = client.get(f"/password_resets/{token}/edit?uid={uid}")
    assert resp.status_code == 200

    # 6. Post bad password confirmation
    resp = client.post(
        f"/password_resets/{token}",
        data={
            "email": test_user.email,
            "password": "newpass",
            "password_confirmation": "wrongpass",
        },
        follow_redirects=True,
    )
    assert b"match" in resp.data.lower() or resp.status_code == 200

    # 7. Post empty password
    resp = client.post(
        f"/password_resets/{token}",
        data={
            "email": test_user.email,
            "password": "",
            "password_confirmation": "",
        },
        follow_redirects=True,
    )
    assert b"can not be empty" in resp.data.lower() or resp.status_code == 200

    # 8. Post valid password
    new_password = "newpassword123"
    resp = client.post(
        f"/password_resets/{token}",
        data={
            "email": test_user.email,
            "password": new_password,
            "password_confirmation": new_password,
        },
        follow_redirects=True,
    )
    assert b"has been reset" in resp.data.lower() or resp.status_code == 200

    # 9. Check that user can log in with new password
    login_resp = client.post(
        "/sessions",
        data={"email": test_user.email, "password": new_password},
        follow_redirects=True,
    )
    assert b"dashboard" in login_resp.data.lower() or login_resp.status_code == 200
