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

