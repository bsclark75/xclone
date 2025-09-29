from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.password_resets import setup_password_reset, reset_password
from app.helpers import get_user, valid_user, log_in

password_reset_bp = Blueprint("password_resets", __name__, url_prefix="/password_resets")

@password_reset_bp.route("/new", methods=["GET"])
def new():
    return render_template("password_resets/new.html")

@password_reset_bp.route("", methods=["POST"])
def create():
    email = request.form.get("email", "").strip().lower()
    user = setup_password_reset(email)
    #print(f"Test: user: {user}")
    if user:
        flash("Email sent with password reset instructions", "info")
        return redirect(url_for("main.index"))
    else:
        flash("Email address not found", "danger")
        return render_template("password_resets/new.html")


@password_reset_bp.route("/<token>/edit", methods=["GET"])
def edit(token):
    uid = request.args.get("uid", type=int)
    user = get_user("id", uid)
    if valid_user(user, token):
        return render_template("password_resets/edit.html", user=user, token=token)
    else:
        flash("User not found", "danger")
        return redirect(url_for( "main.index"))

@password_reset_bp.route("<token>", methods=["POST"])
def update(token):
    # get input values
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("password_confirmation", "")

    # look up user by email
    user = get_user("email", email)

    success, message = reset_password(user, password, confirm)

    if success:
        # log the user in
        log_in(user)
        flash(message, "success")
        return redirect(url_for("users.show_user", user_id=user.id))
    else:
        flash(message, "danger")
        # re-render form with token
        return render_template("password_resets/edit.html", token=token, user=user)
