from flask import Blueprint, render_template, session, request, redirect, url_for, flash,current_app
from website.database.connector import dbconnector
from utils import errhandler
import os 
from werkzeug.utils import secure_filename


pages = Blueprint('pages', __name__)
conn = dbconnector()

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@pages.route('/project', methods=['GET'])
def project():
    try:
        cursor= conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM projects")
        projects=cursor.fetchall()

        if not projects or projects==None:
            flash("No projects to show", category="error")

            return render_template('project/project.html')
        return render_template('project/project.html', projects=projects)
    
    except Exception as e:
        errhandler(e, 'pages/projects')
        flash('An error has occurred.', category="error")
        return redirect(url_for('pages.homepage'))
    
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

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

@pages.route('/gigs', methods=['GET'])
def gigs():
    try:
        cursor= conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM gigs")
        gigs=cursor.fetchall()

        if not gigs or gigs==None:
            flash("No gigs to show", category="error")

            return render_template('gigs/gigs.html')
        return render_template('gigs/gigs.html', gigs=gigs)
    
    except Exception as e:
        errhandler(e, 'pages/gigs')
        flash('An error has occurred.', category="error")
        return redirect(url_for('pages.homepage'))
    
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


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

@pages.route('/add_reviews', methods=['GET', 'POST'])
def add_reviews():
    if request.method == 'POST':
    
        user = session.get('userID')
        # profile validation
        if not user or user==None:
            flash('Please create an account first', category='error')

            return redirect(url_for('auth.signup'))
        try: 
        #capturing entires
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            comment = request.form.get('comment')

            if not (fname and lname and comment):
                flash('Kindly fill in all fields', category='error')

                return redirect(request.url)
           
        # inserting into database
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO reviews(userID,fname, lname, comment) VALUES (%s, %s, %s, %s)", (user,fname, lname, comment))
            conn.commit()

            flash("Thank you for your review", category='success')

            return redirect(url_for('pages.reviews'))
            
        # Log the error
        except Exception as e:
            errhandler(e, 'pages/addreviews')
            flash("An error has occured", category='error')
            return redirect(url_for('pages.homepage'))
        
        # Close cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    return render_template('reviews/addreviews.html')


@pages.route('/reviews', methods=['GET'])
def reviews():
    try:
        # retrieving from database
        cursor= conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reviews")
        reviews=cursor.fetchall()

        #check if there are reviews in the database
        if not reviews or reviews==None:
            flash("No reviews to show", category='error')
            
            return render_template('reviews/reviews.html')
        return render_template('reviews/reviews.html', reviews=reviews)
    
    except Exception as e:
        errhandler(e, 'pages/reviews')
        flash("An error has occured", category='error')

        return redirect(url_for('pages.homepage'))
    
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


# @pages.route('/addproject')
# def addproject():
#     return render_template('project/addproject.html')

