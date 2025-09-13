from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import User
from app.services.user_service import update_user, destory_user
from app.utils.auth import logged_in_user, correct_user, admin_user
from flask_paginate import Pagination, get_page_parameter

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user, title=user.name)

@users_bp.route("<int:user_id>/edit", methods=["GET", "POST"])
@logged_in_user
@correct_user
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

@users_bp.route("")
@logged_in_user
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = request.args.get("size", 30, type=int) 

    # Use SQLAlchemy's built-in pagination
    pagination_obj = User.query.order_by(User.name).paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, total=pagination_obj.total, per_page=per_page, css_framework="bootstrap3")

    return render_template("users/index.html", users=pagination_obj.items, pagination=pagination)

@users_bp.route("<int:user_id>/delete", methods=["GET"])
@logged_in_user
@admin_user
def delete(user_id):
    if destory_user(user_id):
        flash("User deleted successfully.", "success")
    else:
        flash("User not found.", "danger")
    return redirect(url_for("users.index"))

