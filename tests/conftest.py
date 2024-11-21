import os

import pytest
from dash.testing.application_runners import import_app
from selenium.webdriver.chrome.options import Options


def pytest_setup_options():
    """pytest extra command line arguments for running chrome driver

     For GitHub Actions, or similar container, run Chrome headless. There is no display to show the browser.
     To run locally on your computer and see the browser, maximise it and do not use headless.
     If you run it headless on your computer the tests still run, but you will not see the browser.
    """
    options = Options()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    return options
