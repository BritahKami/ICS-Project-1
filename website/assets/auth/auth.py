# Modules
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash

# Database Connection
from website.database.connector import dbconnector

# Utility Functions
from utils import errhandler, message, mailer

import base64
import random
import time

# Auth Blueprint
auth = Blueprint('auth', __name__)

#Database Connection
conn = dbconnector()

# Temporary data
temp = {}

# Logout logic
@auth.route('/logout')
def logout():
    # Validating A session Existence
    if not session['userID']:
        flash('You are not logged in', category='error')

        # Redirecting
        return redirect(url_for('auth.signin'))
    else:
        try:
            # Clearing Session
            session.clear()

            # Success Message
            flash("You have been logged out successfully", category='success')

        except Exception as e:
            # Logging Error
            logger = 'auth/logout'
            errhandler(e, logger)

            # Error Message
            flash("An unexpected error occured. Please try again later", category='error')

            # Redirecting
            return redirect(url_for('pages.homepage'))

        finally:
            #Redirecting
            return redirect(url_for('auth.signin'))

# Access Verifier
@auth.route('/verifier', methods=['GET','POST'])
def verifier():
    if request.method == 'POST':
        code = request.form.get('code')

        if not (code):

            # Error Message
            flash('Verification code is required to complete your authentication', category='error')

            # Redirecting
            return redirect(request.url)

        try:
            # Checking Code Expiry
            if ('code' in temp) and (time.time() < temp['expiry']):

                # Validating Codes Match
                if temp['code'] == code:
                    # Success Message
                    flash('Sign in successful', category='success')

                    # Clearing Temp & Session
                    temp.clear()

                    # Redirecting
                    return redirect(url_for('auth.portal'))
                else:
                    # Error Message
                    flash('Invalid code', category='error')

                    # Clearing Temp & Session
                    temp.clear()
                    session.clear()

                    # Redirecting
                    return redirect(url_for('auth.signin'))
            else:
                # Error Message
                flash('The code has expired', category='error')

                # Clearing Temp & Session
                temp.clear()
                session.clear()

                # Redirecting
                return redirect(url_for('auth.signin'))

        except Exception as e:
            # Logging
            errhandler(e, 'auth/verifier')

            # Error Message
            flash("An unexpected error occured. Please try again later", category='error')

            # Return Message
            return redirect(url_for('auth.signin'))

    return render_template('auth/verifier.html', email=session['email'] if 'email' in session else None)

# Signin logic
@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    # Capturing Form Entries
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Entry Validation
        if not (email and password):

            # Error Message
            flash('Please fill all the fields', category='error')

            # Redirecting
            return redirect(request.url)

        try:
            # Querying Database
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            # Validating Profile Existence
            if not user or user == None:

                #Error Message
                flash("User does not exist", category='error')

                #Redirecting
                return redirect(request.url)

            # Validating Passwords
            if not check_password_hash(user['password'], password):

                # Error Message
                flash("Incorrect password", category='error')

                # Redirecting
                return redirect(request.url)

            # Generating Verification Code
            verification = str(random.randint(100000, 999999))
            email = user['email']
            expiry = time.time() + 300

            # Populating Temp Dictionary
            temp['email'] = email
            temp['code'] = verification
            temp['expiry'] = expiry

            emailBody = f"""
            Hello {user['fname']} {user['lname']},

            Thank you for signing in to our platform.

            Your verification code is:
            {verification}

            This code will expire in 5 minutes.
            """

            # Checking if Mail is Sent
            mailSent = mailer(email, "Verification Code", emailBody)

            if mailSent:
                #Success Message
                flash('A verification code has been sent to your email', category='success')

                # Populating Session
                session['userID'] = user['userID']
                session['fname'] = user['fname']
                session['lname'] = user['lname']
                session['uname'] = user['uname']
                session['email'] = user['email']
                session['role'] = user['role']

                #Redirecting
                return redirect(url_for('auth.verifier'))
            else:
                #Error Message
                flash('An error occurred processing your verification code')

                # Clearing Sessions
                session.clear()

                # Clearing Temp Data
                temp.clear()

                #Redirecting
                return redirect(url_for('pages.homepage'))

        except Exception as e:
            # Error Logging
            errhandler(e, 'auth/signin')

            # Error Message
            flash("An unexpected error occured. Please try again later", category='error')

            # Clearing Sessions
            session.clear()

            # Clearing Temp Data
            temp.clear()

            # Redirecting
            return redirect(url_for('pages.homepage'))

        #Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
    return render_template('auth/signin.html')

# Signup logic
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # Capturing Form Entries
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        uname = request.form.get('uname')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        dob = request.form.get('DOB')

        institution = request.form.get('institution')
        yomStart = request.form.get('yomStart')
        yomFinish = request.form.get('yomFinish')
        email = request.form.get('email')
        faculty = request.form.get('faculty')
        course = request.form.get('course')

        password = request.form.get('password')
        confpass = request.form.get('confpass')
        role = request.form.get('role')

        # Assigning Default Profile Picture
        from utils import imghandler
        profilepic = imghandler(subPath='accounts')

        # Validating Entries
        if not (fname and lname and uname and phone and gender and dob and institution and yomStart and yomFinish and email and faculty and course and password and confpass and role and profilepic):
            # Error Message
            flash("Please fill in all fields")

            # Redirecting
            return redirect(request.url)

        try:
            # Query Cursor
            cursor = conn.cursor(dictionary=True)

            # Checking If The User Already Exists
            cursor.execute("SELECT * FROM users WHERE uname = %s", (uname,))
            user = cursor.fetchone()

            if user and user != None:
                # Error Message
                flash("An active profile already exists", category='error')

                # Redirecting
                return redirect(url_for('auth.signin'))

            # Validating Passwords Match
            if (password != confpass):
                flash("Passwords do not match", category='error')
                return redirect(request.url)

            # Hashing Password
            hash = generate_password_hash(password)

            # Inserting User Into Database
            cursor.execute("INSERT INTO users (fname, lname, uname, email, gender, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)", (fname, lname, uname, email, gender, hash, role))

            # Getting Last Inserted userID
            userID = cursor.lastrowid

            # Inserting Student into Database
            cursor.execute("INSERT INTO students (DOB, phone, institution, yomStart, yomFinish, email, facultyID, courseID, profilePic, userID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (dob, phone, institution, yomStart, yomFinish, email, faculty, course, profilepic, userID))

            # Committing Transactions
            conn.commit()

            #Success Message
            flash("Account created successfully", category='success')

            #Redirecting
            return redirect(url_for('auth.signin'))

        except Exception as e:
            # Transaction Rollback
            conn.rollback()

            # Logging Error
            logger = 'auth/signup'
            errhandler(e, logger)

            # Error Message
            flash("An unexpected error occured. Please try again later", category='error')

            # Redirecting
            return redirect(url_for('pages.homepage'))

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    # Capturing Faculties, Courses, Country Codes & Industries
    try:
        # Initializing Cursor
        cursor = conn.cursor(dictionary=True)

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

    except Exception as e:
        # Logging Error
        errhandler(e, 'auth/signup')

        # Error Message
        flash("An unexpected error occurred. Please try again later", category='error')

        # Redirecting
        return redirect(request.url)

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

    # Rendering Template
    return render_template(
        'auth/signup.html',
        faculties = facultiesData,
        courses = coursesData,
        countries = countriesData,
        industries = industriesData
    )

# Businesses Signup Logic
@auth.route('/signup/business', methods=['POST'])
def signupBusiness():
    # Validating Request Method
    if request.method == 'POST':
        # Clearing Sessions
        session.clear()

        # Capturing Form Entries
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        uname = request.form.get('uname')
        gender = request.form.get('gender')

        bname = request.form.get('bname')
        email = request.form.get('email')

        origin = request.form.get('origin')
        city = request.form.get('city')
        phone = request.form.get('phone')

        industry = request.form.get('industry')

        password = request.form.get('password')
        confpass = request.form.get('confpass')
        role = request.form.get('role')

        # Assigning Default Profile Picture
        from utils import imghandler
        profilePic = imghandler(subPath='accounts')

        # Validating Entries
        if not (fname and lname and uname and gender and bname and email and origin and city and phone and password and confpass and role and profilePic):
            # Error Message
            flash("Please fill in all fields")

            # Redirecting
            return redirect(request.url)

        try:
            # Initializing Cursor
            cursor = conn.cursor(dictionary=True)

            # Checking If The User Already Exists
            cursor.execute("SELECT * FROM users WHERE uname = %s", (uname,))
            user = cursor.fetchone()

            if user and user != None:
                # Error Message
                flash("An active similar user profile already exists", category='error')

                # Redirecting
                return redirect(url_for('auth.signin'))

            # Checking If The Business Already Exists
            cursor.execute("SELECT * FROM businesses WHERE email = %s", (email,))
            business = cursor.fetchone()

            if business and business != None:
                # Error Message
                flash("An active similar business profile already exists", category='error')

                # Redirecting
                return redirect(url_for('auth.signin'))

            # Validating Passwords Match
            if (password != confpass):
                flash("Passwords do not match", category='error')
                return redirect(request.url)

            # Hashing Password
            hash = generate_password_hash(password)

            # Inserting User Into Database
            cursor.execute("INSERT INTO users (fname, lname, uname, email, gender, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)", (fname, lname, uname, email, gender, hash, role))

            # Getting Last Inserted userID
            user = cursor.lastrowid

            # Inserting Business into Database
            cursor.execute("INSERT INTO businesses (bname, email, country, city, phone, industry, userID, icon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (bname, email, origin, city, phone, industry, user, profilePic))

            # Committing Transactions
            conn.commit()

            #Success Message
            flash("Business account created successfully", category='success')

            #Redirecting
            return redirect(url_for('auth.signin'))

        except Exception as e:
            # Transaction Rollback
            conn.rollback()

            # Logging Error
            logger = 'auth/signup-business'
            errhandler(e, logger)

            # Error Message
            flash("An unexpected error occured. Please try again later", category='error')
            return redirect(url_for('pages.homepage'))

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    else:
        flash("Invalid access method", category='error')

# Portal logic
@auth.route('/controller')
def portal():
    return redirect(url_for('pages.homepage'))

# Editing Student Profile
@auth.route('/edit-account/student', methods=['POST'])
def editStudentAccount():
    # Verifying Session
    if 'userID' not in session:
        # Error Message
        flash("Unauthorized access. Please sign in first.", category='error')

        # Redirecting
        return redirect(url_for('auth.signin'))

    userID = session['userID']

    # Validating Request Method
    if request.method == 'POST':
        # Get form fields
        firstName = request.form.get('fname')
        lastName = request.form.get('lname')
        userName = request.form.get('username')
        gender = request.form.get('gender')
        dateOfBirth = request.form.get('dob')
        facultyID = request.form.get('faculty')
        courseID = request.form.get('course')
        email = request.form.get('email')
        phoneNumber = request.form.get('phone')
        role = request.form.get('role')
        profilePic = request.files.get('profilePic')

        # Capturing Form Entries
        try:
            # Initializing Cursor
            cursor = conn.cursor(dictionary=True)

            # Update users table
            userFields = []
            userValues = []

            # Setting Fields to Update
            if firstName: userFields.append("fname = %s"); userValues.append(firstName)
            if lastName: userFields.append("lname = %s"); userValues.append(lastName)
            if userName: userFields.append("uname = %s"); userValues.append(userName)
            if gender: userFields.append("gender = %s"); userValues.append(gender)
            if email: userFields.append("email = %s"); userValues.append(email)
            if role: userFields.append("role = %s"); userValues.append(role)

            if userFields:
                userQuery = f"UPDATE users SET {', '.join(userFields)} WHERE userID = %s"
                cursor.execute(userQuery, userValues + [userID])

            # Update students table
            studentFields = []
            studentValues = []

            if dateOfBirth: studentFields.append("DOB = %s"); studentValues.append(dateOfBirth)
            if phoneNumber: studentFields.append("phone = %s"); studentValues.append(phoneNumber)
            if facultyID: studentFields.append("facultyID = %s"); studentValues.append(facultyID)
            if courseID: studentFields.append("courseID = %s"); studentValues.append(courseID)
            if email: studentFields.append("email = %s"); studentValues.append(email)

            # Handling Profile Pictures
            if profilePic and profilePic.filename != '':

                # Profile Picture Processing
                from utils import imghandler
                profilePicPath = imghandler(
                    img=profilePic,
                    subPath='accounts'
                )

                studentFields.append("profilePic = %s")
                studentValues.append(profilePicPath)

            if studentFields:
                studentQuery = f"UPDATE students SET {', '.join(studentFields)} WHERE userID = %s"
                cursor.execute(studentQuery, studentValues + [userID])

            # Committing Transactions
            conn.commit()

            # Success Message
            flash("Your profile has been updated successfully.", category='success')

            # Updating Session Data
            session.update({
                'fname': firstName if firstName else session.get('fname'),
                'lname': lastName if lastName else session.get('lname'),
                'uname': userName if userName else session.get('uname'),
                'email': email if email else session.get('email'),
                'role': role if role else session.get('role')
            })

            # Redirecting
            return redirect(url_for('dash.dashboard'))

        # Handling Exceptions
        except Exception as e:
            # Transaction Rollback
            conn.rollback()

            # Logging Error
            errhandler(e, 'auth/editStudentAccount')

            # Error Message
            flash("An error occurred while updating your profile. Please try again later.", category='error')

            # Redirecting
            return redirect(url_for('dash.dashboard'))

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

# Editing Business Profile
@auth.route('/edit-account/business', methods=['POST'])
def editBusinessAccount():
    # Session Validation
    if 'userID' not in session:
        flash("Unauthorized access. Please sign in first.", category='error')
        return redirect(url_for('auth.signin'))

    userID = session['userID']

    # Validating Request Method
    if request.method == 'POST':

        # Get form values
        firstName = request.form.get('fname')
        lastName = request.form.get('lname')
        userName = request.form.get('username')
        gender = request.form.get('gender')
        businessName = request.form.get('bname')
        email = request.form.get('email')
        industryID = request.form.get('industry')
        countryID = request.form.get('country')
        city = request.form.get('city')
        phoneNumber = request.form.get('phone')
        role = request.form.get('role')
        profilePic = request.files.get('profilePic')

        # Database Operations
        try:
            # Initializing Cursor
            cursor = conn.cursor(dictionary=True)

            # Users Update Lists
            userFields = []
            userValues = []

            # Setting Fields to Update
            if firstName: userFields.append("fname = %s"); userValues.append(firstName)
            if lastName: userFields.append("lname = %s"); userValues.append(lastName)
            if userName: userFields.append("uname = %s"); userValues.append(userName)
            if gender: userFields.append("gender = %s"); userValues.append(gender)
            if email: userFields.append("email = %s"); userValues.append(email)
            if role: userFields.append("role = %s"); userValues.append(role)

            if userFields:
                userQuery = f"UPDATE users SET {', '.join(userFields)} WHERE userID = %s"
                cursor.execute(userQuery, userValues + [userID])

            # Update businesses table
            businessFields = []
            businessValues = []

            if businessName: businessFields.append("bname = %s"); businessValues.append(businessName)
            if email: businessFields.append("email = %s"); businessValues.append(email)
            if industryID: businessFields.append("industry = %s"); businessValues.append(industryID)
            if countryID: businessFields.append("country = %s"); businessValues.append(countryID)
            if city: businessFields.append("city = %s"); businessValues.append(city)
            if phoneNumber: businessFields.append("phone = %s"); businessValues.append(phoneNumber)

            # Handling Profile Pictures
            if profilePic and profilePic.filename != '':
                # Profile Picture Processing
                from utils import imghandler
                profilePicPath = imghandler(
                    img=profilePic,
                    subPath='accounts'
                )
                businessFields.append("icon = %s")
                businessValues.append(profilePicPath)

            if businessFields:
                businessQuery = f"UPDATE businesses SET {', '.join(businessFields)} WHERE userID = %s"
                cursor.execute(businessQuery, businessValues + [userID])

            # Committing Transactions
            conn.commit()

            # Updating Session Data
            session.update({
                'fname': firstName if firstName else session.get('fname'),
                'lname': lastName if lastName else session.get('lname'),
                'uname': userName if userName else session.get('uname'),
                'email': email if email else session.get('email'),
                'role': role if role else session.get('role')
            })

            # Success Message
            flash("Your business profile has been updated successfully.", category='success')

            # Redirecting
            return redirect(url_for('dash.dashboard'))

        except Exception as e:
            # Transaction Rollback
            conn.rollback()

            # Logging Error
            errhandler(e, 'auth/editBusinessAccount')

            # Error Message
            flash("An error occurred while updating your profile. Please try again later.", category='error')

            # Redirecting
            return redirect(url_for('dash.dashboard'))

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
