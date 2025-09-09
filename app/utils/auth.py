# app/utils/auth.py
from functools import wraps
from flask import session, redirect, url_for, flash
from app.helpers import is_current_user, store_location
from app.models import User

def logged_in_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            store_location()
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("sessions.new"))
        return f(*args, **kwargs)
    return decorated_function

def correct_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming your route uses <int:id> for the user
        user = User.query.get_or_404(kwargs.get("user_id"))
        
        # If the logged-in user is NOT the requested user, block access
        if not is_current_user(user):
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("main.index"))  # Adjust to your home route
        
        # Otherwise, allow the request through
        return f(*args, **kwargs)
    return decorated_function
