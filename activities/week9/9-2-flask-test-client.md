# Creating fixtures for a Flask app, database session and Flask test client

To test the routes you will use a combination of:

- [Flask test client](https://flask.palletsprojects.com/en/3.0.x/testing/#fixtures) to create a running Flask app in a
  Pytest fixture
- [Pytest](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#choosing-a-test-layout-import-rules) for test
  assertions

## Create a Flask test client as a pytest fixture

This allows you to create a Flask test app with a client that can be used to make HTTP requests to routes.

This is explained with code in the [Flask documentation](https://flask.palletsprojects.com/en/stable/testing/#fixtures).

The code is shown below with a couple of extra lines to use a separate version of the database for testing. You could
also add code after the 'yield' to remove the database once the testing is completed.

Add this to `conftest.py` and amend `from my_project import create_app` to import your`create_app` function:.

Note that the fixtures below do not have a defined scope so will be used as 'function' scope. If your app takes a
while to create and start, you may prefer to change this to module or session scope.

```python
import importlib.resources
import pytest
from my_project import create_app


@pytest.fixture()
def app():
    app = create_app()
    # Location for the temporary testing database
    db_path = importlib.resources.files('student.data') / 'para_testdb.sqlite'
    db_path_str = str(db_path)

    # Update the app config for testing
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path_str,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
```

### Database fixture

For testing purposes, it is useful to know the state of the database before any tests occur. One approach is to define
a fixture that rolls back any changes made during a test after the test has occurred so that the database is in the
original state before the next test is run. For example:

```python
from sqlalchemy.orm import Session


@pytest.fixture(scope='function', autouse=True)
def db_session(app):
    """Creates a new database session for a test.

    Creates a new database session for each test function.
    Begins a transaction before each test and rolls it back afterward to ensure no changes persist between tests.
    Uses autouse=True to automatically apply this fixture to every test function.
    """

    with app.app_context():
        connection = db.engine.connect()

        # begin a non-ORM transaction
        transaction = connection.begin()

        # bind an individual Session to the connection
        db_session = Session(bind=connection)
        yield db_session

        db_session.close()
        transaction.rollback()
        connection.close()
```

[Next activity](9-3-flask-route-tests.md)