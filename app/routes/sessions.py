from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, session
from app.services.user_service import authenticate_user, remember, forget
from app.helpers import log_in, log_out

sessions_bp = Blueprint("sessions", __name__, url_prefix="/sessions")

# GET /sessions/new → Show login form
@sessions_bp.route("/new", methods=["GET"])
def new():
    return render_template("sessions/new.html")

# POST /sessions → Handle login
@sessions_bp.route("", methods=["POST"])
def create():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password")
    remember_me = request.form.get("remember_me")

    user = authenticate_user(email, password)
    next_page = session.pop("next", None)
    response = make_response(redirect(next_page or url_for("main.index")))    
    if user:
        if user.activated:
            log_in(user)
            if remember_me == "1":
                response = remember(user, response)
            else:
                response = forget(user, response)
            return response
        else:
            message = "Account not activated."
            message += "Check your email for the activation link"
            flash(message, "warning")
            return render_template("index.html")
    else:
        flash("Invalid email/password combination", "danger")
        return render_template("sessions/new.html")

# DELETE /sessions → Logout
@sessions_bp.route("/logout", methods=["DELETE", "POST"])
def destroy():
    response = make_response(redirect(url_for("main.index")))
    response = log_out(response)
    flash("Logged out successfully", "info")
    return response
