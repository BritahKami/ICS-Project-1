from flask import Blueprint, render_template, session, request, redirect, url_for, flash,current_app
from website.database.connector import dbconnector
from utils import errhandler
import os 
from werkzeug.utils import secure_filename

# Pages Blueprint Instance
pages = Blueprint('pages', __name__)

# Database Connection
conn = dbconnector()

# Homepage
@pages.route('/')
def homepage():
    userID = session.get('userID')
    if (userID) and (userID != "None"):
            return render_template("home/home.html", userID=userID)
    return render_template('home/home.html')

# Projects Route
@pages.route('/project', methods=['GET'])
def project():
    # Session Validation
    if 'userID' in session or session['userID'] != None:
        userID = session['userID']

    # Database Operations
    try:
        # Cursors Initialization
        cursor= conn.cursor(dictionary=True)

        # List to Hold Projects
        projectsList = []

        # Capturing All Projects
        cursor.execute("SELECT * FROM projects")
        projects=cursor.fetchall()

        if projects and projects != None:
            # Capture User Details from Users Table & Icon from Students Table
            cursor.execute("SELECT fname, lname FROM users WHERE userID = %s", (userID,))
            user_details = cursor.fetchone()

            cursor.execute("SELECT profilePic FROM students WHERE userID = %s", (userID,))
            student_icon = cursor.fetchone()

            for project in projects:
                projectsList.append({
                    'projectID' : project['projectID'],
                    'title' : project['title'],
                    'description' : project['description'],
                    'image' : project['image'].replace('website/static/uploads/items/', ''),
                    'studentIcon' : student_icon['profilePic'].replace('website/static/uploads/accounts/', ''),
                    'fname' : user_details['fname'],
                    'lname' : user_details['lname'],
                    'studentID' : project['studentID']
                })
        return render_template(
            'project/project.html',
            projects=projectsList,
            userID=userID,
        )

    except Exception as e:
        # Logging Error
        errhandler(e, 'pages/projects')

        # Error Message
        flash('An error has occurred retrieving projects.', category="error")

        # Redirecting
        return redirect(url_for('pages.homepage'))

    # Closing Cursor
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

# Under construction pages
@pages.route('/404')
def comingsoon():
    return render_template('other/comingsoon.html')

@pages.route('/about')
def about():
    return render_template('about/about.html')

@pages.route('/gigs', methods=['GET'])
def gigs():
    # Session Validation
    if 'userID' in session or session['userID'] != None:
        userID = session['userID']

    # Database Operations
    try:
        # Cursors Initialization
        cursor= conn.cursor(dictionary=True)

        # List to Hold Gigs
        gigsList = []

        # Capturing All Gigs
        cursor.execute("SELECT * FROM gigs")
        gigs=cursor.fetchall()

        if gigs and gigs!=None:
            # Capture User Details from Users Table & Icon from Students Table
            cursor.execute("SELECT fname, lname FROM users WHERE userID = %s", (userID,))
            user_details = cursor.fetchone()

            cursor.execute("SELECT profilePic FROM students WHERE userID = %s", (userID,))
            student_icon = cursor.fetchone()

            for gig in gigs:
                gigsList.append({
                    'gigID' : gig['gigID'],
                    'title' : gig['title'],
                    'description' : gig['description'],
                    'price' : gig['price'],
                    'image' : gig['image'].replace('website/static/uploads/items/', ''),
                    'studentIcon' : student_icon['profilePic'].replace('website/static/uploads/accounts/', ''),
                    'fname' : user_details['fname'],
                    'lname' : user_details['lname'],
                    'studentID' : gig['studentID']
                })

        return render_template(
            'gigs/gigs.html',
            userID=userID,
            gigs=gigsList
        )

    except Exception as e:
        # Logging Error
        errhandler(e, 'pages/gigs')

        # Error Message
        flash('An error has occurred.', category="error")

        # Redirecting
        return redirect(url_for('pages.homepage'))

    # Closing Cursor
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


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

# @pages.route('/add_reviews', methods=['GET', 'POST'])
# def add_reviews():
#     if request.method == 'POST':
    
#         user = session.get('userID')
#         # profile validation
#         if not user or user==None:
#             flash('Please create an account first', category='error')

#             return redirect(url_for('auth.signup'))
#         try: 
#         #capturing entires
#             fname = request.form.get('fname')
#             lname = request.form.get('lname')
#             comment = request.form.get('comment')

#             if not (fname and lname and comment):
#                 flash('Kindly fill in all fields', category='error')

#                 return redirect(request.url)
           
#         # inserting into database
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute("INSERT INTO reviews(userID,fname, lname, comment) VALUES (%s, %s, %s, %s)", (user,fname, lname, comment))
#             conn.commit()

#             flash("Thank you for your review", category='success')

#             return redirect(url_for('pages.reviews'))
            
#         # Log the error
#         except Exception as e:
#             errhandler(e, 'pages/addreviews')
#             flash("An error has occured", category='error')
#             return redirect(url_for('pages.homepage'))
        
#         # Close cursor
#         finally:
#             if 'cursor' in locals() and cursor is not None:
#                 cursor.close()

#     return render_template('reviews/addreviews.html')


@pages.route('/reviews', methods=['GET', 'POST'])
def reviews():

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
            rating = request.form.get('rating')


            if not (fname and lname and comment and rating):
                flash('Kindly fill in all fields', category='error')

                return redirect(request.url)
           
        # inserting into database
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO reviews(userID,fname, lname, comment,rating) VALUES (%s, %s, %s, %s, %s)", (user,fname, lname, comment,rating))
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

    def starsprocess(rating):
            stars = ''

            if rating < 15:
                stars = '<i class="ri-star-half-line"></i>'
            elif rating < 25:
                stars = '<i class="ri-star-fill"></i>'
            elif rating < 35:
                stars = '<i class="ri-star-fill"></i><i class="ri-star-half-line"></i>'
            elif rating < 45:
                stars = '<i class="ri-star-fill"></i><i class="ri-star-fill"></i>'
            elif rating < 55:
                stars = '<i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-half-line"></i>'
            elif rating < 65:
                stars = '<i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i>'
            elif rating < 75:
                stars = '<i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-half-line"></i>'
            elif rating < 85:
                stars = '<i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i>'
            elif rating < 95:
                stars = '<i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-half-line"></i>'
            else:
                stars = '<i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i><i class="ri-star-fill"></i>'
            return stars


    try:
        # retrieving from database
        cursor= conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reviews")
        reviews=cursor.fetchall()

        reviewsData=[]
        if reviews and reviews != None:
            for review in reviews:
                review['stars'] = starsprocess(review['rating'])
                reviewsData.append(review)

        return render_template('reviews/reviews.html', reviewsData=reviewsData)


        #check if there are reviews in the database
        # if not reviews or reviews==None:
        #     flash("No reviews to show", category='error')
            
        #     return render_template('reviews/reviews.html')
        # return render_template('reviews/reviews.html', reviews=reviews)
    
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

