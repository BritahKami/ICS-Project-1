from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from ...database.connector import dbconnector
from utils import errhandler, message
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import random
import time

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
            return redirect(url_for('views.homepage'))

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

            # Populating Session
            session['userID'] = user['userID']
            session['fname'] = user['fname']
            session['lname'] = user['lname']
            session['uname'] = user['uname']
            session['email'] = user['email']
            session['role'] = user['role']

            # Generating Verification Code
            verification = str(random.randint(100000, 999999))
            email = session['email']
            expiry = time.time() + 300

            # Populating Temp Dictionary
            temp['email'] = email
            temp['code'] = verification
            temp['expiry'] = expiry

            # Printing Verification Code on Terminal
            txt = f'Verification code for email: {email} is:\n{verification}\nYour code expires in 5 minutes'
            message(txt)

            #Success Message
            flash('A verification code has been sent to your terminal', category='success')

            #Redirecting
            return redirect(url_for('auth.verifier'))

        except Exception as e:
            # Error Logging
            errhandler(e, 'auth/signin')

            # Error Message
            flash("An unexpected error occured. Please try again later", category='error')

            # Redirecting
            return redirect(url_for('views.homepage'))

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
        email = request.form.get('email')
        # phone = request.form.get('phone')
        gender = request.form.get('gender')
        password = request.form.get('password')
        confpass = request.form.get('confpass')
        role = request.form.get('role')

        # Profile Picture
        # profilepic = picHandler()

        # Validating Entries
        if not (fname and lname and uname and email and gender and password and confpass and role):
            flash("Please fill in all fields")
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
            conn.commit()

            #Success Message
            flash("Account created successfully", category='success')

            #Redirecting
            return redirect(url_for('auth.signin'))

        except Exception as e:
            # Logging Error
            logger = 'auth/signup'
            errhandler(e, logger)

            # Error Message
            flash("An unexpected error occured. Please try again later", category='error')
            return redirect(url_for('views.homepage'))

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    return render_template('auth/signup.html')

# Portal logic
@auth.route('/controller')
def portal():
    return redirect(url_for('pages.homepage'))