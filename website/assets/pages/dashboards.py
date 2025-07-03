from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from website.database.connector import dbconnector
from utils import errhandler
import os 
from werkzeug.utils import secure_filename


# Admin Blueprint Instance
dash = Blueprint('dash', __name__)

# Database Connection
conn = dbconnector()

#allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    for key in ['userID', 'fname', 'lname', 'uname', 'email']:
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
            internships=internshipsDetails
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
    
    if request.method == 'POST':
        image = request.files.get('image')
        title = request.form.get('title')
        description = request.form.get('description')

        # Validating Entries
        if not (image and title and description):
            flash('Kindly fill in all fields', category='error')

            return redirect(request.url)
        
        if image and allowed_file(image.filename):
            
            try:
                #secure and save the file
                filename= secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))

                # inserting into database
                cursor = conn.cursor(dictionary=True)
                cursor.execute("INSERT INTO projects (image, title, description) VALUES (%s, %s, %s)", (filename, title, description))
                conn.commit()

                flash('Your project has been added successfully', category="success")

                return redirect(url_for('pages.homepage'))

            # Handling Exceptions
            except Exception as e:
                errhandler(e, 'pages/project')

                flash('An error has occurred. Try again later', category='error')

            # Closing Cursor
            finally:
                if 'cursor' in locals() and cursor is not None:
                    cursor.close()
        
        else:
            flash("Invalid image format. Allowed types: png, jpg, jpeg, gif.", category='error')
            return redirect(request.url)


    return render_template('dashboard/students/student.html')