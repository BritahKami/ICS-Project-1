from flask import Blueprint, render_template, session

pages = Blueprint('pages', __name__)

# Homepaage
@pages.route('/')
def homepage():
    userID = session.get('userID')
    if (userID) and (userID != "None"):
            return render_template("home/home.html", userID=userID)
    return render_template('home/home.html')

# Under construction pages
@pages.route('/404')
def comingsoon():
    return render_template('other/comingsoon.html')

@pages.route('/about')
def about():
    return render_template('about/about.html')

@pages.route('/gigs')
def gigs():
    return render_template('gigs/gigs.html')

@pages.route('/addgigs')
def addgigs():
    return render_template('gigs/addgigs.html')

@pages.route('/jobs')
def jobs():
    return render_template('other/comingsoon.html')

@pages.route('/contact')
def contact():
    return render_template('other/comingsoon.html')

@pages.route('/blog')
def blog():
    return render_template('other/comingsoon.html')

@pages.route('/testimonials')
def testimonials():
    return render_template('other/comingsoon.html')

@pages.route('/developers')
def developers():
    return render_template('other/comingsoon.html')

@pages.route('/FAQs')
def faqs():
    return render_template('other/comingsoon.html')

@pages.route('/reviews')
def reviews():
    return render_template('reviews/reviews.html')

@pages.route('/add_reviews')
def add_reviews():
    return render_template('reviews/addreviews.html')

@pages.route('/project')
def project():
    return render_template('project/project.html')

@pages.route('/addproject')
def addproject():
    return render_template('project/addproject.html')

