from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from website.database.connector import dbconnector
from utils import errhandler

pages = Blueprint('pages', __name__)
conn = dbconnector()

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
    return render_template('jobs/jobs.html')

# Contact Page
@pages.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        comment = request.form.get('comment')
        rating = request.form.get('rating')

        # Validating Entries
        if not (fname and lname and comment and rating):
            # Error Message
            flash('Kindly fill in all fields', category='error')

            # Redirecting
            return redirect(request.url)

        # Populating Database
        try:
            # Initializing Cursor
            cursor = conn.cursor(dictionary=True)

            # Executing Query
            cursor.execute("INSERT INTO reviews (fname, lname, comment, rating) VALUES (%s, %s, %s, %s)", (fname, lname, comment, rating))

            # Committing to Database
            conn.commit()

            # Success Message
            flash('Your reviews have been added successfully', category="success")

            # Redirecting
            return redirect(url_for('pages.homepage'))

        # Handling Exceptions
        except Exception as e:
            # Logging Error
            errhandler(e, 'pages/contact')

            # Error Message
            flash('An error occurred processing your review. Try again later', category='error')

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()


    return render_template('contact/contact.html')

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

