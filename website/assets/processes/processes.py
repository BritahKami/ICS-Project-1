from flask import Blueprint, render_template, flash, request, redirect, url_for
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