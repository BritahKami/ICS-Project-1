from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from website.database.connector import dbconnector
from utils import errhandler

# Processes Blueprint Object
process = Blueprint('process', __name__)

# Database Connection
conn = dbconnector()

# Newsletters Process
@process.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    # Validating Acess Method
    if request.method == 'POST':
        # Capturing Form Entries
        email = request.form.get('email')

        # Input Validation
        if (not email) and ('@' not in email):
            # Error Message
            flash("Please enter a valid email address", category="error")

            # Redirecting
            return redirect(request.url)

        try:
            # Initializing Cursor
            cursor = conn.cursor(dictionary=True)

            # Checking Whether Email Already Exists
            cursor.execute("SELECT * FROM newsletters WHERE email = %s", (email,))
            exists = cursor.fetchone()

            if exists and exists != None:
                # Error Message
                flash("An active similar email is already registered for the newsletter service", category='error')

                # Redirecting
                return redirect(request.url)

            # Inserting Email to Database
            cursor.execute("INSERT INTO newsletters (email)  VALUES (%s)",(email,))

            # Committing Transaction
            conn.commit()

            # Success Message
            flash("You have successfully opted into our newsletter service", category="success")

            # Redirecting
            return redirect(request.url)

        # Exception Handling
        except Exception as e:
            # Transaction Rollback
            conn.rollback()

            # Logging Error
            errhandler(e, 'process/newsletters')

            # Error Message
            flash("An error occurred processing your request", category='error')

            # Redirecting
            return redirect(request.url)

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    # Redirecting
    return redirect(url_for("pages.homepage"))

# Add Item
@process.route('/addItem/', methods=['GET', 'POST'])
def addItem():
    # Validating if the User Has Access
    if not (session['userID']):
        flash("You are not authorized to access this service", category='error')

        # Clearing Session
        session.clear()

        # Redirecting
        return redirect(url_for(auth.signin))

    # Checking Request Method
    if request.method == 'POST':
        # Capturing Form Entries
        title = request.form.get('title')
        option = request.form.get('option')
        description = request.form.get('description')
        icon = request.files['image']

        # Validating Entries
        if not (title or option or description or icon):
            # Error Message
            flash("Please fill in all fields", category="error")

            # Redirecting
            return redirect(request.url)

        # Image Path Processing
        from utils import imghandler
        icon = imghandler(
            icon,
            path='uploads',
            subPath="items",
            operation='add'
        )

        print(icon)

        # Operations
        try:
            # Initializing Cursor
            cursor = conn.cursor(dictionary=True)

            # Checking if the User Has a Valid Business Account
            cursor.execute("SELECT * FROM businesses WHERE userID = %s", (session['userID'],))
            business = cursor.fetchone()

            # Validating Query Result
            if business and (business != None):
                # Capturing Business ID
                businessID = business['businessID']

                # Verifying UserID Matches Session Data
                if business['userID'] != session['userID']:
                    # Error Message
                    flash("Your credentials are corrupted. You cannot complete this operation", category="error")

                    # Redirecting
                    return redirect(auth.logout)

                else:
                    userID = business['userID']
            else:
                # Error Message
                flash("You do not have an active business account", category="error")

                # Redirecting
                return redirect(auth.logout)

            # Executing Query
            cursor.execute(f"INSERT INTO {option.lower() + 's'} (title, description, icon, userID, businessID) VALUES (%s, %s, %s, %s, %s)", (title, description, icon, userID, businessID))

            # Committing to Database
            conn.commit()

            # Success Message
            flash(f"Your {option} has been successfully added", category="success")

            # Redirecting
            return redirect(url_for('dash.dashboard'))

        # Handling Errors
        except Exception as e:
            # Database Rollback
            conn.rollback()

            # Logging Error
            errhandler(e, 'process/add-items')

            # Error Message
            flash("An error occurred adding your item", category="error")

            # Redirecting
            return redirect(request.url)

        # Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    return redirect(url_for('dash.dashboard'))