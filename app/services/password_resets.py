from app.models import User
from datetime import datetime
from app import db

def setup_password_reset(email):
    user = User.query.filter_by(email=email).first()
    if user:
        token = user.create_reset_digest()
        user.send_password_reset_email(token)
        user.reset_sent_at = datetime.now()
        db.session.commit()
        return user
    else:
        return None

def reset_password(user, password, confirm):
    """
    Handles the business logic of resetting a password.
    Returns (success: bool, message: str)
    """
    if not user:
        return False, "User not found or link is expired"

    if user.password_reset_expired():
        return False, "Link is expired"

    if password == "":
        return False, "Password can not be empty"

    if password != confirm:
        return False, "Passwords do not match"

    # update password hash
    user.set_password(password)
    # commit changes
    db.session.commit()

    return True, "Password has been reset"
