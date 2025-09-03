from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models import User, db
from app.helpers import remember, log_in

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("home.html", title="Home")

@main.route("/home")
def home():
    return render_template("home.html", title="Home")

@main.route("/help")
def help():
    return render_template("help.html", title="Help")

@main.route("/about")
def about():
    return render_template("about.html", title="About")

@main.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")

@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if password != confirm_password:
                flash("Passwords do not match.", "danger")
                return render_template("users/new.html", title="Sign Up")
            
            if len(password) < 6:
                flash("Password must be at least 6 characters long.", "danger")
                return render_template("users/new.html", title="Sign Up")

            # Create new user — model handles hashing & validation
            new_user = User(name=name, email=email)
            new_user.set_password(password)  # triggers hashing in model

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            flash("Account created successfully! You are now logged in.", "success")
            return redirect(url_for("main.show_user", user_id=new_user.id))


        except ValueError as e:
            db.session.rollback()
            flash(str(e), "danger")
            return render_template("users/new.html", title="Sign Up")

    return render_template("users/new.html", title="Sign Up")

@main.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user, title=user.name)

sessions_bp = Blueprint("sessions", __name__, url_prefix="/sessions")

# GET /sessions/new → Show login form
@sessions_bp.route("/new", methods=["GET"])
def new():
    return render_template("sessions/new.html")

# POST /sessions → Handle login
@sessions_bp.route("", methods=["POST"])
def create():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash("Invalid email or password", "danger")
        return redirect(url_for("sessions.new"))

    log_in(user)
    remember(user)
    flash("Logged in successfully!", "success")
    return redirect(url_for("main.show_user", user_id=user.id))

# DELETE /sessions → Logout
@sessions_bp.route("/logout", methods=["DELETE", "POST"])
def destroy():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("main.index"))
