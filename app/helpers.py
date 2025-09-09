from flask import session, g, request
from app.models import User
from app.services.user_service import forget


def gravatar_for(user):
    import hashlib
    email = user.email.strip().lower()
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=100"
    return f'<img src="{gravatar_url}" alt="{user.name}\'s Gravatar" class="gravatar">'

def current_user():
    # 1. If user_id is in session
    if "user_id" in session:
        if not hasattr(g, "current_user"):
            g.current_user = User.query.get(session["user_id"])
        return g.current_user

    # 2. Else check cookies
    user_id = request.cookies.get("user_id")
    remember_token = request.cookies.get("remember_token")

    if user_id and remember_token:
        user = User.query.get(user_id)
        if user and user.authenticated(remember_token):
            log_in(user)  # Store back into session
            return user

    return None

def logged_in():
    if current_user():
        return True
    return False

def log_in(user):
    session["user_id"] = user.id


def log_out(response):
    if logged_in():
        user = current_user()
        response = forget(user, response)
        session.pop("user_id", None)
    return response

def is_current_user(user):
    cu = current_user()
    return cu and cu.id == user.id

def store_location():
    if request.method == "GET" and "next" not in session:
        session["next"] = request.url