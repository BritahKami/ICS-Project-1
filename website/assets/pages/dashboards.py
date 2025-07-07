from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from website.database.connector import dbconnector
from utils import errhandler
import os
from werkzeug.utils import secure_filename


# Admin Blueprint Instance
dash = Blueprint('dash', __name__)

# Database Connection
conn = dbconnector()

# Access Verification Route
@dash.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    # Checking Authentication
    if ('userID' not in session) and ('role' not in session):
        # Error Message
        flash('You are not authorized to access this page', category='error')

        # Clearing Sessions
        session.clear()

        # Redirecting
        return redirect(url_for('auth.signin'))

    # Role Access
    else:
        if session['role'] == 'admin':
            # Redirecting to Admin Dash
            return redirect(url_for('dash.admin'))

        elif session['role'] == 'business':
            # Redirecting to Business Dash
            return redirect(url_for('dash.business'))

        elif session['role'] == 'student':
            # Redirecting to User Dash
            return redirect(url_for('dash.student'))

        else:
            # Error Message
            flash('You are not authorized to acces this page', category='error')

            # Clearing Sessions
            session.clear()

            # Redirecting
            return redirect(url_for('auth.signin'))

# Admin Dashboard Route
@dash.route('/dashboard/admin', methods=['GET', 'POST'])
def admin():
    # Checking Authentication
    if ('userID' not in session) and ('role' not in session):
        # Error Message
        flash('You are not authorized to access this page', category='error')

        # Clearing Sessions
        session.clear()

        # Redirecting
        return redirect(url_for('auth.signin'))

    # Checking Role
    if session['role'] != 'admin':
        # Error Message
        flash('You are not authorized to access this page', category='error')

        # Clearing Sessions
        session.clear()

        # Redirecting
        return redirect(url_for('auth.signin'))

    # Capturing User Details From Session
    user = {}
    for key in ['userID', 'fname', 'lname', 'uname', 'email']:
        if key in session:
            user[key] = session[key]

    try:
        render_template(
            'dashboard/admins/admin.html',
            user=user
        )
    except Exception as e:
        # Logging Error
        errhandler(e, 'dashboards/admin')

        # Error Message
        flash('An error has occurred retrieving your account details. Try again later', category='error')

        # Redirecting
        return redirect(url_for('dash.admin'))

    return render_template('dashboard/admins/admin.html')

# Business Dashboard Route
@dash.route('/dashboard/business', methods=['GET', 'POST'])
def business():
    # Checking Authentication
    if ('userID' not in session) and ('role' not in session):
        # Error Message
        flash('You are not authorized to access this page', category='error')

        # Clearing Sessions
        session.clear()

        # Redirecting
        return redirect(url_for('auth.signin'))

    # Checking Role
    if session['role'] != 'business':
        # Error Message
        flash('You are not authorized to access this page', category='error')

        # Clearing Sessions
        session.clear()

        # Redirecting
        return redirect(url_for('auth.signin'))

    # Capturing User Details From Session
    user = {}
    for key in ['userID', 'fname', 'lname', 'uname', 'email', 'role']:
        if key in session:
            user[key] = session[key]

    # Retrieving Database Info
    try:
        # Initializing Cursor
        cursor = conn.cursor(dictionary=True)

        # Capturing Business Details
        cursor.execute("SELECT * FROM businesses WHERE userID = %s", (session['userID'],))
        business = cursor.fetchone()

        # Capturing Jobs
        cursor.execute("SELECT * FROM jobs WHERE userID = %s", (session['userID'],))
        jobs = cursor.fetchall()

        # Capturing Internships
        cursor.execute("SELECT * FROM internships WHERE userID = %s", (session['userID'],))
        internships = cursor.fetchall()

        # Business Data Lists
        businessDetails = []
        jobsDetails = []
        internshipsDetails = []

        # Querying Database
        cursor.execute("SELECT * FROM faculties")
        faculties = cursor.fetchall()

        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        cursor.execute("SELECT * FROM countries")
        countries = cursor.fetchall()

        cursor.execute("SELECT * FROM industries")
        industries = cursor.fetchall()

        # List Objects for Retrieved Data
        facultiesData = []
        coursesData = []
        countriesData = []
        industriesData = []

        # Verifying Retrieved Data
        if ((not (faculties)) or (faculties == None)) or ((not courses) or (courses == None)) or ((not (countries)) or (countries == None)) or ((not (industries)) or (industries == None)):
            # Error Message
            flash("An error occured retrieving the list of some imported data. Please try again later", category='error')

            # Redirecting
            return redirect(request.url)

        # Appending Faculties to List
        for faculty in faculties:
            facultiesData.append(faculty)

        # Appending Courses to List
        for course in courses:
            coursesData.append(course)

        # Appending Countries to List
        for country in countries:
            countriesData.append(country)

        # Appending Industries to List
        for industry in industries:
            industriesData.append(industry)

        # Validating Query Results
        if business and (business != None):
            # Appending Business Details
            businessDetails.append({
                'businessID': business['businessID'],
                'bname': business['bname'],
                'email': business['email'],
                'country': business['country'],
                'city': business['city'],
                'phone': business['phone'],
                'industry': business['industry'],
                'userID': business['userID'],
                'icon': business['icon']
            })

        # Validating Jobs Query Result
        if jobs and (jobs != None):
            # Appending Jobs Details
            for job in jobs:
                jobsDetails.append({
                    'jobID': job['jobID'],
                    'title': job['title'],
                    'description': job['description'],
                    'icon': job['icon'].replace('website/static/uploads/items/', ''),
                    'userID': job['userID'],
                    'businessID': job['businessID']
                })

        # Validating Internships Query Result
        if internships and (internships != None):
            # Appending Internships Details
            for internship in internships:
                internshipsDetails.append({
                    'internshipID': internship['internshipID'],
                    'title': internship['title'],
                    'description': internship['description'],
                    'icon': internship['icon'].replace('website/static/uploads/items/', ''),
                    'userID': internship['userID'],
                    'businessID': internship['businessID']
                })

        # Rendering Template
        return render_template(
            'dashboard/businesses/business.html',
            user=user,
            business=businessDetails,
            jobs=jobsDetails,
            internships=internshipsDetails,
            faculties = facultiesData,
            courses = coursesData,
            countries = countriesData,
            industries = industriesData
        )


    # Handling Exceptions
    except Exception as e:
        # Logging Error
        errhandler(e, 'dashboards/business')

        # Error Message
        flash('An error has retrieving your account details. Try again later', category='error')

        # Redirecting
        return redirect(url_for('dash.business'))

    # Closing Cursor
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

    return render_template('dashboard/businesses/business.html')


# Student Dashboard Route
@dash.route('/dashboard/student', methods=['GET', 'POST'])
def student():
    # Checking Authentication
    if ('userID' not in session) and ('role' not in session):
        # Error Message
        flash('You are not authorized to access this page', category='error')

        # Clearing Sessions
        session.clear()

        # Redirecting
        return redirect(url_for('auth.signin'))

    # Checking Role
    if session['role'] != 'student':
        # Error Message
        flash('You are not authorized to access this page', category='error')

        # Clearing Sessions
        session.clear()

        # Redirecting
        return redirect(url_for('auth.signin'))

    # Capturing User Details From Session
    user = {}
    for key in ['userID', 'fname', 'lname', 'uname', 'email', 'role']:
        if key in session:
            user[key] = session[key]

    #fetching studentID for the logged in user
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT studentID FROM students WHERE userID = %s", (session['userID'],))
    student_record = cursor.fetchone()

    if (not student_record) or (student_record == None):
        # Error Message
        flash("You are not authorized to access this page", category="error")

        # Clearing Sessions
        session.clear()

        # Redirecting
        return redirect(url_for('auth.signin'))

    # Capturing Student Details
    studentID = student_record['studentID']

    if request.method == 'POST':
        title = request.form.get('title')
        option = request.form.get('option')
        price = request.form.get('price') if option == 'gig' else None
        description = request.form.get('description')
        image = request.files.get('image')

        # Validating Entries
        if not (title and option and description and image):
            # Error Message
            flash('Kindly fill in all fields', category='error')

            # Redirecting
            return redirect(request.url)

        # Image Processing
        from utils import imghandler
        image = imghandler(img = image, subPath = 'items')

        # Database Operations
        try:
            # Initializing Cursor
            cursor = conn.cursor(dictionary=True)

            # For Gigs Option
            if option.lower() == 'gig':
                cursor.execute(
                "INSERT INTO gigs (title, price, description, image, studentID) VALUES (%s, %s, %s, %s, %s)",
                (title, price, description, image, studentID)
            )

            # For Projects Option
            elif option.lower() == 'project':
                cursor.execute(
                "INSERT INTO projects (title, description, image, studentID) VALUES (%s, %s, %s, %s)",
                (title, description, image, studentID)
            )

            else:
                # Error Message
                flash("Invalid operation type.", category='error')

                # Redirecting
                return redirect(request.url)

            # Committing Transaction
            conn.commit()

            # Success Message
            flash(f"Your {option.lower()} has been added successfully", category='success')

            # Redirecting
            return redirect(url_for('dash.dashboard'))

        # Handling Exceptions
        except Exception as e:
            # Transaction Rollback
            conn.rollback()

            # Logging Error
            errhandler(e, 'pages/project')

            # Error Message
            flash('An error has occurred. Try again later', category='error')

            # Redirecting
            return redirect(request.url)

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    # Querying for Gigs & Projects
    try:
        # Lists for Queried Items
        projectsDetails = []
        gigsDetails = []

        # Initializing Cursor
        cursor= conn.cursor(dictionary=True)

        # Fetching Projects
        cursor.execute("SELECT * FROM projects WHERE studentID = %s", (studentID,))
        projects=cursor.fetchall()

        # Fetching Gigs
        cursor.execute("SELECT * FROM gigs WHERE studentID = %s", (studentID,))
        gigs=cursor.fetchall()

        # Querying Database
        cursor.execute("SELECT * FROM faculties")
        faculties = cursor.fetchall()

        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        cursor.execute("SELECT * FROM countries")
        countries = cursor.fetchall()

        cursor.execute("SELECT * FROM industries")
        industries = cursor.fetchall()

        # List Objects for Retrieved Data
        facultiesData = []
        coursesData = []
        countriesData = []
        industriesData = []

        # Verifying Retrieved Data
        if ((not (faculties)) or (faculties == None)) or ((not courses) or (courses == None)) or ((not (countries)) or (countries == None)) or ((not (industries)) or (industries == None)):
            # Error Message
            flash("An error occured retrieving the list of some imported data. Please try again later", category='error')

            # Redirecting
            return redirect(request.url)

        # Appending Faculties to List
        for faculty in faculties:
            facultiesData.append(faculty)

        # Appending Courses to List
        for course in courses:
            coursesData.append(course)

        # Appending Countries to List
        for country in countries:
            countriesData.append(country)

        # Appending Industries to List
        for industry in industries:
            industriesData.append(industry)

        try:
            # Capture User's Names & Icon From Users & Students Tables
            cursor.execute("SELECT fname, lname FROM users WHERE userID = %s", (session['userID'],))
            user_details = cursor.fetchone()

            cursor.execute("SELECT profilePic FROM students WHERE userID = %s", (session['userID'],))
            student_icon = cursor.fetchone()

        except Exception as e:
            # Logging Error
            errhandler(e, 'pages/student')

            # Error Message
            flash("An error occurred retrieving your data", category="error")

            # Clearing Sessions
            session.clear()

            # Redirecting
            return redirect(url_for('auth.signin'))

        # Validating Projects Query Results
        if projects and projects!=None:
            for project in projects:
                projectsDetails.append({
                    'projectID' : project['projectID'],
                    'title' : project['title'],
                    'description' : project['description'],
                    'image' : project['image'].replace('website/static/uploads/items/', ''),
                    'studentIcon' : student_icon['profilePic'].replace('website/static/uploads/accounts/', ''),
                    'fname' : user_details['fname'],
                    'lname' : user_details['lname'],
                    'studentID' : project['studentID']
                })

        # Validating Gigs Query Results
        if gigs and gigs!=None:
            for gig in gigs:
                gigsDetails.append({
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

        print (student_icon['profilePic'].replace('website/static/uploads/accounts/', ''))
        return render_template(
            'dashboard/students/student.html',
            user=user,
            projects=projectsDetails,
            gigs=gigsDetails,
            faculties = facultiesData,
            courses = coursesData,
            countries = countriesData,
            industries = industriesData
        )

    # Handling Exceptions
    except Exception as e:
        errhandler(e, 'pages/projects')
        flash('An error has occurred.', category="error")
        return redirect(url_for('pages.homepage'))

    # Closing Cursor
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()