from threading import Thread
from flask import render_template
from flask_mail import Message
from flask_babel import _
from flask import current_app
from app import mail


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_account_activation_email(user):
    token = user.get_account_activation_token()
    send_mail(
        subject=_("OGN Devices Database - Account Activation"),
        sender=current_app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("emails/account_activation.txt", user=user, token=token),
        html_body=render_template("emails/account_activation.html", user=user, token=token),
    )


def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_mail(
        subject=_("OGN Devices Database - Password Reset"),
        sender=current_app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("emails/reset_password.txt", user=user, token=token),
        html_body=render_template("emails/reset_password.html", user=user, token=token),
    )


def send_device_claim_email(device_claim):
    token = device_claim.get_token()
    send_mail(
        subject=_("OGN Devices Database - Device Claim"),
        sender=current_app.config["ADMINS"][0],
        recipients=[device_claim.owner.email],
        text_body=render_template("emails/device_claim.txt", device_claim=device_claim, token=token),
        html_body=render_template("emails/device_claim.html", device_claim=device_claim, token=token),
    )
