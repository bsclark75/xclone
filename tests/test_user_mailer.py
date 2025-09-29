# tests/test_user_mailer.py
import re
from tests.utils import create_user
from app.services import user_mailer as mailer 

def test_account_activation(app, capsys):
    """
    Test that send_activation_email prints the activation email
    (e.g., when using Flask-Mail console backend).
    """

    user, token = create_user(name="alice", email="alice@example.com")

    with app.test_request_context():
        mailer.send_activation_email(user,token)

    # Capture what was printed to stdout
    captured = capsys.readouterr()
    out = captured.out

    assert user.email in out
    assert token in out
    assert f"/account-activations/{token}/edit" in out

def test_password_reset(app, capsys, test_user):
    token = test_user.create_reset_digest()
    
    with app.test_request_context():
        mailer.send_password_reset(test_user,token)

    captured = capsys.readouterr()
    out = captured.out
    assert "Password reset" in out
    assert test_user.email in out
    assert token in out
    