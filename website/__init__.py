from flask import Flask

from utils import errhandler, mail as MAIL
from config import env

def create_app():
    global app

    # Initializing Flask
    app = Flask(__name__)

    # Configuring Secret Key
    app.config['SECRET_KEY'] = env.SECRET_KEY

    # Importing Blueprints
    from .assets.pages.pages import pages
    from .assets.auth.auth import auth

    # Registering Blueprints
    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(mailer, url_prefix='/')

    """
    Flask Mail
    """
    # Mail Configurations
    app.config.update(
        MAIL_SERVER=env.MAIL_SERVER,
        MAIL_PORT=env.MAIL_PORT,
        MAIL_USERNAME=env.MAIL_USERNAME,
        MAIL_PASSWORD=env.MAIL_PASSWORD,
        MAIL_USE_TLS= env.MAIL_USE_TLS,
        MAIL_USE_SSL=env.MAIL_USE_SSL,
        # MAIL_DEFAULT_SENDER=env.MAIL_SENDER,
        # MAIL_SENDER=env.MAIL_SENDER,
        # MAIL_RECEIVER=env.MAIL_RECEIVER,

        # Defaults
        MAIL_MAX_EMAILS = None,
        MAIL_ASCII_ATTACHMENTS = False
    )

    # Binding Extensions
    MAIL.init_app(app)

    # Returning App Instance
    return app