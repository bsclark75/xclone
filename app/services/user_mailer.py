from flask import render_template, url_for
from flask_mailman import EmailMultiAlternatives
#from app import mailer

def send_activation_email(user):
    activation_url = url_for("account_activations.edit", token=user.activation_digest, _external=True)
    subject = "Activate Your Account"
    to = [user.email]

    # Render templates
    text_body = render_template("emails/activation.txt", user=user, activation_url=activation_url)
    html_body = render_template("emails/activation.html", user=user, activation_url=activation_url)

    # Create message with both text + HTML parts
    msg = EmailMultiAlternatives(subject, text_body, to=to)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
