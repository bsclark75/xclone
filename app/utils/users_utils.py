from app.models import User

def get_user(field, value):
    # field: column name as string, value: value to match
    user = User.query.filter_by(**{field: value}).first()
    return user

def get_user_or_404(field, value):
    from flask import abort
    user = get_user(field, value)
    if not user:
        abort(404)
    return user