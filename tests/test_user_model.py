import pytest
from app.models import User
from tests.utils import create_user

def test_create_valid_user(db_session):
    user, _ = create_user(name="Alice Johnson", email="alice@example.com")
    saved_user = User.query.filter_by(email="alice@example.com").first()
    assert saved_user is not None
    assert saved_user.name == "Alice Johnson"


@pytest.mark.parametrize("name", ["", "   "])
def test_user_requires_name_not_blank(db_session, name):
    with pytest.raises(ValueError, match="Name cannot be empty or whitespace"):
        create_user(name=name, email="bob@example.com")


def test_user_requires_email_not_blank(db_session):
    with pytest.raises(ValueError, match="Email cannot be empty or whitespace"):
        create_user(name="Robert Doe", email="   ")


def test_name_too_long(db_session):
    with pytest.raises(ValueError, match="Name cannot be longer than 50 characters"):
        create_user(name="a" * 51, email="bob@example.com")


def test_email_too_long(db_session):
    long_email = "a" * 246 + "@example.com"
    with pytest.raises(ValueError, match="Email cannot be longer than 255 characters"):
        create_user(name="Charlie", email=long_email)


@pytest.mark.parametrize("email", [
    "user@example.com",
    "USER@foo.COM",
    "A_US-ER@foo.bar.org",
    "first.last@foo.jp",
    "alice+bob@baz.cn"
])
def test_valid_formatted_email_address(db_session, email):
    user, _ = create_user(name="Jon Doe", email=email)
    assert user.email == email.lower()


@pytest.mark.parametrize("email", [
    "user@example,com", "user_at_foo.org", "user.name@example.",
    "foo@bar_baz.com", "foo@bar+baz.com"
])
def test_invalid_formatted_email_address(db_session, email):
    with pytest.raises(ValueError, match="Invalid email format"):
        create_user(name="Jon Doe", email=email)


def test_user_email_must_be_unique(db_session):
    create_user(name="Alice", email="alice@example.com")
    with pytest.raises(ValueError, match="Email already exists"):
        create_user(name="Bob", email="alice@example.com")


def test_user_email_case_insensitive(db_session):
    create_user(name="Alice", email="User@Example.com")
    with pytest.raises(ValueError, match="Email already exists"):
        create_user(name="Bob", email="user@example.com")


def test_password_should_be_present(db_session):
    with pytest.raises(ValueError, match="Password cannot be blank"):
        user = User(name="Alice", email="user@example.com")
        user.set_password("   ")  # direct call to model's validator


def test_password_should_have_a_minimum_length(db_session):
    with pytest.raises(ValueError, match="Password must be at least 6 characters"):
        user = User(name="Alice", email="user@example.com")
        user.set_password("123")
