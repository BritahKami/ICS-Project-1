from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from website.database.connector import dbconnector

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
        return redirect(url_for('pages.homepage'))

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

    return render_template('dashboard/students/student.html')