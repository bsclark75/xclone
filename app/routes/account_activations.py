from flask import Blueprint

aa_bp = Blueprint("account_activations", __name__, url_prefix="/account-activations")

@aa_bp.route("<string:token>/edit")
