from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
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

    if not user:
        flash("Invalid email or password", "danger")
        return render_template("sessions/new.html", email=email, remember_me=remember_me)
    session = log_in(user)

    # ✅ Create a redirect response
    response = make_response(redirect(url_for("main.index")))

    # ✅ Delegate remember-me to helpers
    if remember_me == "1":
        response = remember(user, response)
    else:
        response = forget(user, response)

    flash("Logged in successfully!", "success")
    return response

# DELETE /sessions → Logout
@sessions_bp.route("/logout", methods=["DELETE", "POST"])
def destroy():
    response = make_response(redirect(url_for("main.index")))
    response = log_out(response)
    flash("Logged out successfully", "info")
    return response
