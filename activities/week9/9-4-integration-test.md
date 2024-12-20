# (Optional) Integration testing for a Flask app

Using Selenium webdriver was covered in week 4. This activity provides guidance on differences when using it to test a
Flask app.

You are not required to do this for the coursework. This is a learning activity for those who want to use web browser
testing techniques for a Flask app.

Some differences to consider:

- create a fixture to create the chromedriver
- create a fixture to run the Flask app as a live server in a separate thread (the Dash duo fixture did this for you)

You could also consider using Playwright instead of Selenium Webdriver.
This [pretty printed video tutorial](https://www.youtube.com/watch?v=T-y3_T1HgTI) explains how to use Playwright for a
Flask app.

## Create fixtures

Create the chromedriver as a fixture. In Flask you only had to configure the options, not create it as a fixture.

```python
import os
import pytest
from selenium.webdriver import Chrome, ChromeOptions


@pytest.fixture(scope="module")
def chrome_driver():
    """
    Fixture to create a Chrome driver. 
    
    On GitHub or other container it needs to run headless, i.e. the browser doesn't open and display on screen.
    Running locally you may want to display the tests in a large window to visibly check the behaviour. 
    """
    options = ChromeOptions()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    driver = Chrome(options=options)
    yield driver
    driver.quit()
```

## Create a fixture to run the Flask app as a live server

The library `pytest-flask` has a live_server fixture. If you install that, you should be able to use that fixture.

If you are using Windows you may need to try it and see if it works, last year it didn't work for Windows, but they may
have corrected that.

Alternatively you can create your own `live_server` fixture in `conftest.py`.

The Flask app needs to run and be accessible in a browser, while tests are being executed. To achieve this the app needs
to be run in a thread.

Here is an example fixture based on this [forum post](https://github.com/pytest-dev/pytest-flask/issues/54):

```python
import socket
import subprocess
import time
import pytest


@pytest.fixture(scope="session")
def flask_port():
    """Gets a free port from the operating system."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="session")
def live_server(flask_port):
    """Runs the Flask app as a live server for Selenium tests (Paralympic app)
    """
    # Construct the command string to run flask with formatted dictionary
    command = """flask --app 'paralympics_flask:create_app(test_config={"TESTING": True, "WTF_CSRF_ENABLED": False})' run --port """ + str(
        flask_port)
    try:
        server = subprocess.Popen(command, shell=True)
        # Allow time for the app to start
        time.sleep(3)
        yield server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")
```

## Test the server is running

This uses the requests library. The chrome driver navigates the page but does not get HTTP responses. Requests will make
an HTTP request and receives an HTTP response object.

You can [check the documentation](https://requests.readthedocs.io/en/latest/api/#requests.Response) to see what values
you can access from the response. This test checks the status code is 200.

Since the port is dynamically allocated then to get the home page url you need to get the port from the flask_port
fixture.

Add the code to `test_paralympics_flask.py` (or other file name):

```python
import requests


def test_server_is_up_and_running(live_server_flask, flask_port):
    """
    GIVEN a live server
    WHEN a GET HTTP request to the home page is made
    THEN the HTTP response have a status code of 200
    """
    url = f'http://127.0.0.1:{flask_port}/'
    response = requests.get(url)
    assert response.status_code == 200
```

Run the test, e.g. `pytest -v` or a run tests command in your IDE.

## Writing tests

To write Selenium tests, refer to the guidance in week 4 for Dash testing as the principle is the same.

You will need to use the Selenium Webdriver commands to navigate, not the Dash_duo version.

You control the HTML elements and ids in the Flask app in your templates, so it is easier to target specific elements in
Flask than it was in Dash. For example, you are unlikely to need XPATH to locate an element.