# tests/utils.py
from app.models import User
from app.extensions import db

def create_user(name="Test User", email="test@example.com", password="password123"):
    """Create a persisted user using the model's bcrypt-based password setter."""
    user = User(name=name, email=email)
    user.set_password(password)  # bcrypt via model
    db.session.add(user)
    db.session.commit()
    return user

def signup(client, name="Test User", email="test@example.com",
           password="password123", confirm_password=None, follow=True):
    """Post to /signup with reasonable defaults."""
    return client.post(
        "/signup",
        data={
            "name": name,
            "email": email,
            "password": password,
            "confirm_password": confirm_password or password,
        },
        follow_redirects=follow,
    )

def login(client, email, password, remember_me=False):
    """Helper to log in the test user."""
    return client.post(
        "/sessions",
        data=dict(
            email=email,
            password=password,
            remember_me="1" if remember_me else "0"  # <-- FIXED
        ),
        follow_redirects=False
    )

