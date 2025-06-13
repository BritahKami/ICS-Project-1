from flask import Blueprint, render_template, session

pages = Blueprint('pages', __name__)

# Homepaage
@pages.route('/')
def homepage():
    userID = session.get('userID')
    if (userID) and (userID != "None"):
            return render_template("home/home.html", userID=userID)
    return render_template('home/home.html')