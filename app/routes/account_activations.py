from flask import Blueprint

aa_bp = Blueprint(
    "account_activations",
    __name__,
    url_prefix="/account-activations"
)

@aa_bp.route("/<string:token>/edit", methods=["GET", "POST"])
def edit(token):
    # token is automatically passed as a string
    # do whatever you need (lookup user, verify token, etc.)
    return f"Editing activation for token: {token}"

