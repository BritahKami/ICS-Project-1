from flask import Flask

def create_app():
    global app

    app = Flask(__name__)

    app.config['SECRET_KEY'] = "flaskapp"

    # Blueprints
    from .blocks.pages.pages import pages

    # Registering Blueprints
    app.register_blueprint(pages, url_prefix='/')

    return app