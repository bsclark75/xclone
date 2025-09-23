from app.models import User
from app.helpers import log_in


def aa_edit(token):
    user = User.query.filter_by(activation_digest=token).first_or_404()
    if user and not user.activated and user.authenticated("activation", token):
        user.activate()
        log_in(user)
        return user
    return None
