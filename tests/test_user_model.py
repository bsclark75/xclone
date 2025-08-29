from app.models import User
from sqlalchemy.exc import IntegrityError
import pytest

def test_create_valid_user(db_session):
    # Arrange
    user = User(name="Alice Johnson", email="alice@example.com")

    # Act
    db_session.add(user)
    db_session.commit()

    # Assert
    saved_user = User.query.filter_by(email="alice@example.com").first()
    assert saved_user is not None
    assert saved_user.name == "Alice Johnson"
    assert saved_user.email == "alice@example.com"

def test_user_requires_name_not_blank(db_session):
    with pytest.raises(ValueError, match="Name cannot be empty or whitespace"):
        user1 = User(name="  ", email="bob@example.com")
        db_session.add(user1)
        db_session.commit()

def test_user_requires_email_not_blank(db_session):
    with pytest.raises(ValueError, match="Email cannot be empty or whitespace"):
        user1 = User(name="Robert Doe", email="")
        db_session.add(user1)
        db_session.commit()

def test_name_too_long(db_session):
    with pytest.raises(ValueError, match="Name can not be longer than 50 characters"):
        user1 = User(name="a" * 51, email="bob@examaple.com")
        db_session.add(user1)
        db_session.commit()

def test_email_too_long(db_session):
    long_email = "a" * 246 + "@example.com"  # total > 255
    with pytest.raises(ValueError, match="Email cannot be longer than 255 characters"):
        user = User(name="Charlie", email=long_email)
        db_session.add(user)
        db_session.commit()

def test_valid_formatted_email_address(db_session):
    valid_addresses = [
        "user@example.com",
        "USER@foo.COM",
        "A_US-ER@foo.bar.org",
        "first.last@foo.jp",
        "alice+bob@baz.cn"
    ]
    for valid_address in valid_addresses:
        user = User(name="Jon Doe", email=valid_address)
        db_session.add(user)
        db_session.commit()
        saved_user = User.query.filter_by(email=valid_address.lower()).first()
        assert saved_user is not None

def test_invalid_formatted_email_address(db_session):
    invalid_addresses = ["user@example,com", "user_at_foo.org", "user.name@example.", "foo@bar_baz.com", "foo@bar+baz.com"]
    for invalid_address in invalid_addresses:
        with pytest.raises(ValueError, match="Invalid email format"):
            user = User(name="Jon Doe", email=invalid_address)
            db_session.add(user)
            db_session.commit()

def test_user_email_must_be_unique(db_session):
    # Create the first user
    user1 = User(name="Alice", email="alice@example.com")
    db_session.add(user1)
    db_session.commit()

    # Attempt to create a second user with the same email
    with pytest.raises(ValueError, match="Email already exists"):
        user2 = User(name="Bob", email="alice@example.com")
        db_session.add(user2)
        db_session.commit()

def test_user_email_case_insensitive(db_session):
    user1 = User(name="Alice", email="User@Example.com")
    db_session.add(user1)
    db_session.commit()

    with pytest.raises(ValueError, match="Email already exists"):
        user2 = User(name="Bob", email="user@example.com")
        db_session.add(user2)
        db_session.commit()
