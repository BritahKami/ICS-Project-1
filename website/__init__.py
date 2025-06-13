from flask import Flask
from .config import env

def create_app():
    global app

    app = Flask(__name__)

    app.config['SECRET_KEY'] = env.SECRET_KEY

    # Blueprints
    from .assets.pages.pages import pages
    from .assets.auth.auth import auth

    # Registering Blueprints
    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app