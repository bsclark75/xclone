import pytest
from app.models import User
from tests.utils import signup, create_user

def test_successful_signup(client):
    response = signup(client, name="Alice", email="alice@example.com", password="password123")
    assert response.status_code == 200
    assert b"Account created successfully" in response.data
    assert User.query.filter_by(email="alice@example.com").first() is not None


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
