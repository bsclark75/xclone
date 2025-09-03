from flask import session, g, request, make_response
from app.models import User
from config import Config
from itsdangerous import URLSafeTimedSerializer

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
        if user and user.verify_token(remember_token):
            log_in(user)  # Store back into session
            return user

    return None

def logged_in():
    if current_user():
        return True
    return False

def remember(user):
    user.remember()
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    encrypted_user_id = serializer.dumps(user.id)
    response = make_response("Cookie has been set!")  
    response.set_cookie("user_id", encrypted_user_id, max_age=60*60*24*30, httponly=True, samesite="Lax")
    response.set_cookie("remember_token", user.remember_token, max_age=60*60*24*30, httponly=True, samesite="Lax")
    return response

def log_in(user):
    session["user_id"] = user.id
    return session

def log_out():
    session.pop("user_id", None)
    current_user = None