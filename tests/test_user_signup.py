import pytest
from app.models import User
from tests.utils import signup, create_user, get_user_count
import re
from urllib.parse import urlparse

def test_successful_signup(client, capsys):
    before_count = get_user_count()

    signup(client, "Alice", "alice@example.com", "password123", "password123")

    captured = capsys.readouterr()
    after_count = get_user_count()
    assert after_count == before_count + 1
    #print(f"{captured.out}")
    # extract activation URL (allow for newlines in HTML email)
    match = re.search(r"http://localhost[^\s\"']+", captured.out)
    assert match, f"Activation link not found in output: {captured.out}"
    activation_url = match.group(0)

    #path = urlparse(activation_url).path
    #print(activation_url)
    resp = client.get(activation_url, follow_redirects=True)
    assert resp.status_code == 200
    # optionally check that the user is now active in DB
    user = User.query.filter_by(email="alice@example.com").first()
    assert user.activated

def test_signup_invalid_email(client):
    response = signup(client, name="Bob", email="foo@invalid")
    assert b"Invalid email format" in response.data
    assert User.query.filter_by(email="foo@invalid").first() is None


def test_signup_duplicate_email(client):
    create_user(name="Charlie", email="charlie@example.com")
    response = signup(client, name="Another", email="charlie@example.com")
    assert b"Email already exists" in response.data


@pytest.mark.parametrize("password", ["123", "abc"])
def test_signup_weak_password(client, password):
    response = signup(client, name="Dave", email="dave@example.com", password=password)
    assert b"Password must be at least 6 characters" in response.data
    assert User.query.filter_by(email="dave@example.com").first() is None
