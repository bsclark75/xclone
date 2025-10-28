from app.models import User, db
from sqlalchemy.exc import IntegrityError
from app.services.user_mailer import send_activation_email
from app.utils.users_utils import get_user


def create_user(name, email, password, confirm_password):
    """Handles user creation with validation."""
    #print("Create user starts here")
    # Basic validation
    if password != confirm_password:
        raise ValueError("Passwords do not match.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")

    email = email.strip().lower()
    if not email or "@" not in email:
        raise ValueError("Invalid email address.")

    # Create the user instance
    user = User(name=name, email=email)
    user.set_password(password)
    token = user.create_activation_digest()
    #print(user)
    db.session.add(user)
    try:
        db.session.commit()
        #print("Successfully commited")
        send_activation_email(user, token)
        return user

    except IntegrityError:
        db.session.rollback()
        raise ValueError("A user with this email already exists.")  # Nice UX

    except ValueError as e:
        db.session.rollback()
        raise e

    #except Exception:
    #    db.session.rollback()
    #    raise ValueError("An unexpected error occurred while creating the user.")


def update_user(user, name, email, password=None, confirm_password=None):
    """Handles user profile updates with validation."""
    if not name.strip():
        raise ValueError("Name cannot be empty.")

    email = email.strip().lower()
    if not email or "@" not in email:
        raise ValueError("Invalid email address.")

    user.name = name
    user.email = email

    if password:
        if password != confirm_password:
            raise ValueError("Passwords do not match.")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        user.set_password(password)

    try:
        db.session.commit()
        return user

    except IntegrityError:
        db.session.rollback()
        raise ValueError("A user with this email already exists.")  # Nice UX

    except ValueError as e:
        db.session.rollback()
        raise e

    except Exception:
        db.session.rollback()
        raise ValueError("An unexpected error occurred while creating the user.")

def authenticate_user(email, password):
    """Authenticate a user by email and password."""
    email = email.strip().lower()
    user = get_user("email", email)
    if user and user.check_password(password):
        return user
    return None

def remember(user, response):
    """Generate a remember token, save it, and attach cookie to response."""
    token = user.remember()

    # Attach cookie directly to the response
    response.set_cookie(
        "remember_digest",
        token,
        max_age=30 * 24 * 60 * 60,  # 30 days
        httponly=True,
        samesite="Lax"
    )
    response.set_cookie(
        "user_id",
        str(user.id),
        max_age=30 * 24 * 60 * 60,
        httponly=True,
        samesite="Lax"
    )
    return response

def forget(user, response):
    """Remove remember token and delete cookie from response."""
    user.forget()
    response.delete_cookie("remember_digest")
    return response

def destory_user(user_id):
    user = get_user("id", user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def promote_user(user_id):
    user = get_user("id", user_id)
    if user:
        user.admin = True
        db.session.commit()
        return True
    return False

def confirm_user(user_id):
    user = get_user("id", user_id)
    if not user:
        return None, None, None

    if not user.admin:
        message = "Are you sure you trust this user with admin privileges?"
        action = "promote"
    else:
        message = "Are you sure you want to demote this user from admin privileges?"
        action = "demote"

    return user, message, action

def demote_user(user_id):
    user = get_user("id", user_id)
    if user:
        user.admin = False
        db.session.commit()
        return True
    return False