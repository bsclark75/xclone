from flask import session
from app.models import User

def gravatar_for(user):
    import hashlib
    email = user.email.strip().lower()
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=100"
    return f'<img src="{gravatar_url}" alt="{user.name}\'s Gravatar" class="gravatar">'

def current_user():
    user_id = session.get('user_id')
    if user_id:
        return user_id
    return None

def logged_in():
    if current_user():
        return True
    return False