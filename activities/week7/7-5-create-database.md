# Creating the database with SQLAlchemy

## Introduction

You may already have a database with data that you want to use in your app. You do not have to use the following if this
is the case.

Flask-SQLAlchemy can be used to create the database dynamically when the Flask app starts. The code logic will only
create the tables if they are not already present in the database.

It can be useful to create the database this way as it allows you to make changes the Python classes and update the
tables accordingly.

There is a further type of Python package, not covered in this course, that keep track of such database changes. These
include [Flask-Migrate](https://flask-migrate.readthedocs.io/en/stable/)
or [Flask-Alembic](https://flask-alembic.readthedocs.io/en/stable/)

## Generate the tables

Update the `create_app()` function to generate the database tables.

The code goes after the app is initialised for the database.

You need to import the models. To avoid circular imports, put this after the app is created; so **not** at the top of
the
file where you would usually place imports.

If you are using a linter you will need to ignore the warnings about placing the import at the top of the file.

To create the tables for User, Region and Event in the database use a Flask-SQLAlchemy function `db.create_all()`. This
will create the tables if they do not already exist. Add this line _after_ importing the models.

```python
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
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Set the location of the database file in the app's instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'paralympics.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

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

        # This imports the models, the linter will flag warnings!
        from tutor.flask_para_t import models

        # If the database file does not exist, it will be created
        # If the tables do not exist, they will be created but does not overwrite or update existing tables
        db.create_all()

        from student.flask_paralympics import paralympics

    return app
```

## Run  the app to generate the database

Run the app, e.g. `flask --app student.flask_paralympics run --debug`.

As the database does not exist it will be created. You can check this by looking in the instance folder. You should see
a file called `paralympics.sqlite`.

## Add data to the database

There are many ways to add data to a database using Python.

To avoid re-writing the code, the following uses the code that was written in COMP0035. You could re-write the functions
to use just SQLAlchemy without using sqlite3.

Move [add_data.py](../../src/student/placeholder/add_data.py) `add_data.py` from the placeholder directory to [flask_paralympics](../../src/student/flask_paralympics)

Update the `create_app()` function to call the `add_all_data()` function after the tables are created.

```python
def create_app(test_config=None):
    # ... CODE OMITTED FOR BREVITY HERE ...

    with app.app_context():
        # Create the database and tables if they don't already exist
        db.create_all()

        # Import and use the function to add the data to the database
        # The add_all_data checks if the tables are empty first
        from student.flask_paralympics.add_data import add_all_data
        add_all_data()

    # ... CODE OMITTED FOR BREVITY HERE ...    

    return app
```

[Next activity](7-6-queries.md)