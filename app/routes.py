from flask import Blueprint, render_template

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

@main.route("/signup")
def signup():
    return render_template("users/new.html", title="New user")

@main.route("/users/<int:user_id>")
def show_user(user_id):
    from app.models import User
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user, title=user.name)

