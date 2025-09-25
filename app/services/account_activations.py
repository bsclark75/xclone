from app.models import User
from app.helpers import log_in
#from app.extensions import bcrypt


def aa_edit(token,uid):
    #print(uid)
    user = User.query.filter_by(id=uid).first_or_404()
    #print(f"aa_edit: User: {user}")
    #print(user.authenticated("activation", token))
    if user and not user.activated and user.authenticated("activation", token):
        #print(f"aa_edit: Ready to activate user")
        user.activate()
        log_in(user)
        return user
    return None
