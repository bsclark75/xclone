from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.user_service import create_user
from app.services.user_mailer import send_activation_email

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("home.html", title="Home")

@main_bp.route("/home")
def home():
    return render_template("home.html", title="Home")

@main_bp.route("/help")
def help():
    return render_template("help.html", title="Help")

@main_bp.route("/about")
def about():
    return render_template("about.html", title="About")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")

@main_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            user = create_user(request.form.get("name"),
                    request.form.get("email"),
                    request.form.get("password"),
                    request.form.get("confirm_password"))
            send_activation_email(user)
            flash("Please check your email to activate your account", "info")
            return redirect(url_for("main.home"))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("users/new.html", title="Sign Up")

    return render_template("users/new.html", title="Sign Up")
