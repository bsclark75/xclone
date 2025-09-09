from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import User
from app.services.user_service import update_user
from app.utils.auth import logged_in_user

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user, title=user.name)

@users_bp.route("<int:user_id>/edit", methods=["GET", "POST"])
@logged_in_user
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        try:
            update_user(user,
                        request.form.get("name"),
                        request.form.get("email"),
                        request.form.get("password"),
                        request.form.get("confirm_password"))
            flash("User updated successfully!", "success")
            return redirect(url_for("users.show_user", user_id=user.id))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("users/edit.html", user=user, title="Edit Profile")
    return render_template("users/edit.html", user=user, title="Edit Profile")