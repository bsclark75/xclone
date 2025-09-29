from flask import render_template, url_for
from flask_mailman import EmailMultiAlternatives
#from app import mailer

def send_activation_email(user, token):
    #print(f"send_activation_email: {user.id}")
    activation_url = url_for("account_activations.edit", token=token, uid=user.id, _external=True)
    #print(f"send_activation_email: {activation_url}")
    subject = "Activate Your Account"
    to = [user.email]

    # Render templates
    text_body = render_template("emails/activation.txt", user=user, activation_url=activation_url)
    html_body = render_template("emails/activation.html", user=user, activation_url=activation_url)
    #print("message is ready")
    # Create message with both text + HTML parts
    msg = EmailMultiAlternatives(subject, text_body, to=to)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
    #print("message sent")

def send_password_reset(user, token):
    reset_url = url_for("password_resets.edit", token=token, uid=user.id, _external=True)
    subject = "Reset Your Account"
    to = [user.email]
    text_body = render_template("emails/password_reset.txt", user=user, reset_url=reset_url)
    html_body = render_template("emails/password_reset.html", user=user, reset_url=reset_url)
    msg = EmailMultiAlternatives(subject, text_body, to=to)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
    