from flask import Blueprint, flash, redirect, url_for, request
from app.services.account_activations import aa_edit

aa_bp = Blueprint(
    "account_activations",
    __name__,
    url_prefix="/account-activations"
)

@aa_bp.route("/<path:token>/edit", methods=["GET", "POST"])
def edit(token):
    # token is automatically passed as a string
    # do whatever you need (lookup user, verify token, etc.)
    #print(f"Token received: {repr(token)}")
    uid = request.args.get('uid', type=int)
    user = aa_edit(token, uid)
    if user:
        flash("Account activated!", "success")
        return redirect(url_for("users.show_user", user_id=user.id))
    else:
        flash("Invalid activation link", "danger")
        return redirect(url_for("main.index"))
    

