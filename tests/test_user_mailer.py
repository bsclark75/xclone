# tests/test_user_mailer.py
import re
from tests.utils import create_user 

def test_account_activation(app, capsys):
    """
    Test that send_activation_email prints the activation email
    (e.g., when using Flask-Mail console backend).
    """
    from app.services import user_mailer as mailer

    user, token = create_user(name="alice", email="alice@example.com")

    with app.test_request_context():
        mailer.send_activation_email(user,token)

    # Capture what was printed to stdout
    captured = capsys.readouterr()
    out = captured.out

    assert user.email in out
    assert token in out
    assert f"/account-activations/{token}/edit" in out