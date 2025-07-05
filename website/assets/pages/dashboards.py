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

    # Capturing User Details From Session
    user = {}
    for key in ['userID', 'fname', 'lname', 'uname', 'email']:
        if key in session:
            user[key] = session[key]

    #fetching studentID for the logged in user
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT studentID FROM students WHERE userID = %s", (session['userID'],))
    student_record = cursor.fetchone()

    if not student_record:
        flash("Student profile not found", category="error")
        return redirect(url_for('auth.signin'))

    studentID = student_record['studentID']

    if request.method == 'POST':
        image = request.files.get('image')
        option = request.form.get('option')
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price') if option == 'gig' else None

        # Validating Entries
        if not (image and title and description and option):
            flash('Kindly fill in all fields', category='error')

            return redirect(request.url)
        

        if image and allowed_file(image.filename):

            try:
                #secure and save the file
                filename= secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))

                userID = session['userID']

                # inserting into database
                cursor = conn.cursor(dictionary=True)

                if option.lower() == 'gig':
                    cursor.execute(
                    "INSERT INTO gigs (image, title, description, price, studentID) VALUES (%s, %s, %s, %s, %s)",
                    (filename, title, description, price, studentID)
                )
                    flash("Your gig has been successfully added", category="success")

                elif option.lower() == 'project':
                    cursor.execute(
                    "INSERT INTO projects (image, title, description, studentID) VALUES (%s, %s, %s, %s)",
                    (filename, title, description, studentID)
                )
                    flash("Your project has been successfully added", category="success")

                else:
                    flash("Invalid submission type.", category='error')
                    return redirect(request.url)

                conn.commit()
                return redirect(url_for('dash.student'))


            # Handling Exceptions
            except Exception as e:
                errhandler(e, 'pages/project')

                flash('An error has occurred. Try again later', category='error')

                return redirect(request.url)

            # Closing Cursor
            finally:
                if 'cursor' in locals() and cursor is not None:
                    cursor.close()

        else:
            flash("Invalid image format. Allowed types: png, jpg, jpeg, gif.", category='error')
            return redirect(request.url)

    # Query for projects
    try:
        # Lists for Queried Items
        projectsDetails = []
        gigsDetails = []

        cursor= conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM projects WHERE studentID = %s", (studentID,))
        projects=cursor.fetchall()

        cursor.execute("SELECT gigs.*, users.fname, users.lname FROM gigs JOIN students ON gigs.studentID = students.studentID JOIN users ON students.userID = users.userID WHERE gigs.studentID = %s", (studentID,))
        gigs=cursor.fetchall()

        if projects and projects!=None:
            for project in projects:
                projectsDetails.append({
                    'projectID' : project['projectID'],
                    'title' : project['title'],
                    'description' : project['description'],
                    'image' : project['image']
                })

        if gigs and gigs!=None:
            for gig in gigs:
                gigsDetails.append({
                    'gigID' : gig['gigID'],
                    'title' : gig['title'],
                    'description' : gig['description'],
                    'image' : gig['image'],
                    'price' : gig['price'],
                    'fname': gig['fname'],
                    'lname': gig['lname']
                })

        return render_template(
            'dashboard/students/student.html',
            user=user,
            projects=projectsDetails,
            gigs=gigsDetails
            )
    
    except Exception as e:
        errhandler(e, 'pages/projects')
        flash('An error has occurred.', category="error")
        return redirect(url_for('pages.homepage'))
    
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

    #     return render_template(
    #     'dashboard/students/student.html',
    #     user=user,  projects=projectsDetails, gigs=gigsDetails

    # )