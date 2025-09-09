# app/utils/auth.py
from functools import wraps
from flask import session, redirect, url_for, flash

def logged_in_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("sessions.new"))  # Update with your login endpoint name
        return f(*args, **kwargs)
    return decorated_function
