# Initialise and configure the SQLAlchemy extension

This uses features from [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/#quick-start).

## Create an instance of a SQLAlchemy object from the Flask-SQLAlchemy library

Return to the `__init__.py` for the Flask application package.

Before the `create_app()` function, initialise an instance of a SQLAlchemy object.

[The Flask-SQLAlchemy documentation](https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/#initialize-the-extension)
gives you the code to add:

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
```

## Initialise the SQLAlchemy object for your Flask app

Your factory function `create_app()` needs to take the SQLAlchemy object and register it for the Flask app.

This will make the connection to the database that is defined by the Flask config parameter `"SQLALCHEMY_DATABASE_URI"`.
It can also use a few other parameters
as [documented here](https://flask-sqlalchemy.readthedocs.io/en/stable/api/#flask_sqlalchemy.SQLAlchemy.init_app).

If you have not already done so, add to your code the name and location of the database file. For example:

```python
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paralympics.db"
```

You can then initialise the SQLAlchemy object for the Flask app. This object allows you to access the database "engine"
that you will be familiar with from earlier tutorials.

The full code will look something like this. Only comments relating to SQLAlchemy have been left in the code below.

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
        # Register the blueprint
        from tutor.flask_para_t.paralympics_7 import main
        app.register_blueprint(main)

    return app
```

Run the Flask app and make sure it still runs.

You will not see any visible difference in the pages.

[Next activity](7-3-classes.md)