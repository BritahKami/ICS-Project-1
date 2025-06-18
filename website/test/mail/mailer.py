# Modules
from flask import Blueprint, flash, redirect, url_for
from flask_mail import Message
from utils import errhandler, syshandler, MAIL

# Mailer Blueprint
mailer = Blueprint('mailer', __name__)

# Mailer Route
@mailer.route("/mail", methods=["GET", "POST"])
def sendMail():

    # Message
    msg = Message(
        # Subject
        subject="Test Email",

        # Sender
        sender='',
        # Recipients
        recipients=[''],

        # Mail Body
        body="""\
Hello there,

This is a test email sent from Flask.

Kind regards,
""",
    )

    try:
        # Sending Mail
        MAIL.send(msg)

        # Logging Success
        syshandler('Mail Sent', 'server/mail')

        # Success Message
        flash("Mail sent successfully", category="success")

    except Exception as e:
        # Logging Error
        errhandler(e, 'server/mail')

        # Error Message
        flash("Failed to send mail", category="error")

    finally:
        #Redirecting
        return redirect(url_for("pages.homepage"))
