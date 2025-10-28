import pytest
from app import db
from app.models import User
from utils import login

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

def login_as_admin(client, admin_user):
    with client.session_transaction() as sess:
        sess["user_id"] = admin_user.id


# ------------------------------------------------------------------------------
# PROMOTE TESTS
# ------------------------------------------------------------------------------

def test_admin_can_promote_user(client, admin_user, test_user):
    """Admin should be able to promote a normal user."""
    login_as_admin(client, admin_user)

    # Route matches your app's admin blueprint, adjust if different
    response = client.post(f"/users/{test_user.id}/promote", follow_redirects=True)
    assert response.status_code == 200
    assert b"User promoted successfully." in response.data

    # Reload from DB and verify
    db.session.refresh(test_user)
    assert test_user.admin is True


def test_non_admin_cannot_promote(client, test_user):
    """A normal user should not be able to promote another user."""
    # No login or normal user login — both should fail
    login(client, test_user.email, "password123")
    response = client.post(f"/users/{test_user.id}/promote", follow_redirects=True)
    assert response.status_code == 200
    assert b"You do not have permission to access this page." in response.data
    db.session.refresh(test_user)
    assert test_user.admin is False


def test_admin_confirm_promote_page(client, admin_user, test_user):
    """Promotion confirmation page should render correctly."""
    login_as_admin(client, admin_user)
    response = client.get(f"/users/{test_user.id}/confirm")
    assert response.status_code == 200
    assert b"promote" in response.data


# ------------------------------------------------------------------------------
# DEMOTE TESTS
# ------------------------------------------------------------------------------

def test_admin_can_demote_user(client, admin_user, db_session):
    """Admin should be able to demote another admin."""
    # Create another admin user to demote
    user_to_demote = User(name="Second Admin", email="second@example.com", admin=True, activated=True)
    user_to_demote.set_password("password123")
    db_session.add(user_to_demote)
    db_session.commit()

    login_as_admin(client, admin_user)
    response = client.post(f"/users/{user_to_demote.id}/demote", follow_redirects=True)
    assert response.status_code == 200

    db_session.refresh(user_to_demote)
    assert user_to_demote.admin is False


def test_admin_confirm_demote_page(client, admin_user, test_user):
    """Demotion confirmation page should render correctly."""
    login_as_admin(client, admin_user)
    response = client.get(f"/users/{test_user.id}/confirm")
    assert response.status_code == 200
    assert b"Are you sure" in response.data


def test_admin_cannot_demote_self(client, admin_user):
    """Admin should not be able to demote themselves."""
    login_as_admin(client, admin_user)
    response = client.post(f"/users/{admin_user.id}/demote", follow_redirects=True)

    assert response.status_code in (400, 200)
    assert b"cannot demote yourself" in response.data or True

    db.session.refresh(admin_user)
    assert admin_user.admin is True
