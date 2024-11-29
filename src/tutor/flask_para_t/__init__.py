import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Create a SQLAlchemy declarative base object called Base to be used in the models (Python classes)
class Base(DeclarativeBase):
    pass


# Create a SQLAlchemy object called db, the Base object is passed to the SQLAlchemy object
db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    # create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Set the location of the database file called paralympics.db which will be in the app's instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'paralympics.db'),
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialise the database
    # Make sure you already defined SQLALCHEMY_DATABASE_URI in the app.config
    db.init_app(app)

    with app.app_context():
        # Optionally, create the database tables
        # This will only work once the models are defined

        # This imports the models
        from tutor.flask_para_t import models
        # If the database file does not exist, it will be created
        # If the tables do not exist, they will be created but does not overwrite or update existing tables
        db.create_all()

        # Import and use the function to add the data to the database.
        from tutor.data.database import add_data
        # To be able to use the existing database functions from COMP0035 requires an sqlite3 cursor and connection
        # The following code creates these from the SQLAlchemy engine.
        # For your own coursework app, use the SQLAlchemy 'db' object instead.
        con = db.engine.raw_connection()
        cur = db.engine.raw_connection().cursor()
        add_data(cur, con)

        # Register the blueprint
        from tutor.flask_para_t.paralympics_7 import main
        app.register_blueprint(main)

    # return the app
    return app
