# Introduction to testing a Flask app

TODO: activity 3 is incomplete, more work needed on routes that interact with the database. The session_db fixture is
also not rollbacking the transactions.

## Types of tests

So far you have learned:

- Unit tests with pytest (COMP0035 week 9).
- Integration/end-to-end/function tests from a browser with chromedriver, Selenium webdriver, pytest and Dash test
  fixtures (COMP0024 week 4)

You also learned the following in COMP0035 with some repetition in COMP0034:

- how to run coverage, and understand some of the reports that can be produced
- how to use GitHub Actions workflow to run tests automatically on GitHub's servers when a commit is pushed to GitHub
- using 'GIVEN-WHEN-THEN' to describe a test
- structuring a test with the ARRANGE-ACT-ASSERT pattern
- configuring Pytest in pyproject.toml

In this tutorial you will learn how to use the Flask test client to test the Flask routes. This may be referred to as
integration testing.

## Set up the test environment

To do this you need to:

1. Install pytest
2. Create a tests directory and test files
3. Install your app code

### 1. Install pytest

Make sure you have installed pytest and selenium in your Python environment e.g.: `pip install pytest`

You may also need to configure your IDE to support running pytest tests, follow the relevant documentation:

- [Pycharm help: Testing frameworks](https://www.jetbrains.com/help/pycharm/testing-frameworks.html)
- [Python testing in VS Code](https://code.visualstudio.com/docs/python/testing)

### 2. Create a test folder and files

- Create a folder called `tests`. Refer to
  the [pytest documentation](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#choosing-a-test-layout-import-rules)
  for alternate test directory structures.
- Create a Python test file in the `tests` folder called `test_routes.py`. You will add the tests to this.
- Create an empty Python file in the `tests` folder called `conftest.py`. You will add the fixtures to this.

### 3. Install your app code

This uses `pyproject.toml` which has metadata about your project code and how to configure pytest.

In the Terminal of your IDE, install the paralympics code using `pip install -e .`

Note: The `.` is part of the command and not a typo!

[Next activity](9-2-flask-test-client.md)