from flask import Flask, flash

from utils import errhandler, mail as MAIL
from config import env
from datetime import datetime

def create_app():
    global app

    # Initializing Flask
    app = Flask(__name__)

    # Configuring Secret Key
    app.config['SECRET_KEY'] = env.SECRET_KEY

    # Importing Blueprints
    from website.assets.pages.pages import pages
    from website.assets.auth.auth import auth
    from website.assets.pages.dashboards import dash
    from website.assets.processes.processes import process

    # Registering Blueprints
    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(dash, url_prefix='/')
    app.register_blueprint(process, url_prefix='/')

    # Image configuration
    UPLOAD_FOLDER = 'website/static/uploads'
    app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER


    """
    Flask Mail
    """
    # Mail Configurations
    app.config.update(
        MAIL_SERVER=env.MAIL_SERVER,
        MAIL_PORT=env.MAIL_PORT,
        MAIL_USERNAME=env.MAIL_USERNAME,
        MAIL_PASSWORD=env.MAIL_PASSWORD,
        MAIL_USE_TLS= env.MAIL_USE_TLS,
        MAIL_USE_SSL=env.MAIL_USE_SSL,
        # MAIL_DEFAULT_SENDER=env.MAIL_SENDER,
        # MAIL_SENDER=env.MAIL_SENDER,
        # MAIL_RECEIVER=env.MAIL_RECEIVER,

        # Defaults
        MAIL_MAX_EMAILS = None,
        MAIL_ASCII_ATTACHMENTS = False
    )

    # Binding Extensions
    MAIL.init_app(app)

    # Context Processors
    @app.context_processor
    def inject_current_date():
        weekday = datetime.now().strftime("%A")
        day = datetime.now().strftime("%d")
        month = datetime.now().strftime("%B")
        year = datetime.now().year
        today = f'{weekday} - {month} {day}, {year}'
        return {"today": today}

    @app.context_processor
    def inject_current_year():
        return {"current_year": datetime.now().year}

    @app.context_processor
    def inject_current_message():
        current_hour = datetime.now().hour

        if 5 <= current_hour < 12:
            message = "morning"
        elif 12 <= current_hour < 17:
            message = "afternoon"
        elif 17 <= current_hour < 22:
            message = "evening"
        else:
            message = "night"

        return {"current_message": message}

    @app.context_processor
    def inject_reviews():
        # Rendering stars based on rating
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

        # Importing Database Connector File
        from website.database.connector import dbconnector

        # Initializing Database Connector
        conn=dbconnector()

        # Querying DB for User Reviews
        try:
            # Initializing Cursor
            cursor=conn.cursor(dictionary=True)

            # Querying for Reviews
            cursor.execute("SELECT * FROM reviews")

            # Storing Result
            reviews=cursor.fetchall()

            # Dictionary to Store Retrieved Info
            reviewsData=[]
            if reviews and reviews != None:
                for review in reviews:
                    review['stars'] = starsprocess(review['rating'])
                    reviewsData.append(review)

            return {'reviewsData' : reviewsData}

        # Handling Exceptions
        except Exception as e:
            # Logging Error
            errhandler(e, 'server/init')

            # Returning Message
            flash('An error occurred fetching user reviews', category='Error')

        #Closing Cursor
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    # Returning App Instance
    return app