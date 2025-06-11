from flask import Blueprint

pages = Blueprint('pages', __name__)

# Homepaage
@pages.route('/')
def homepage():
    return '<h1>Flask App is running</h1>'