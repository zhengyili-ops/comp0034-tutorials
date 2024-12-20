# Using the Flask Test Client to test routes

## Approach

The general structure of this type of test is:

1. ARRANGE: Pass the Flask test client fixture to the test function.
2. ACT: Use the test client to make an HTTP request to one of your routes. Assign the response object to a variable.
3. ASSERT: Access parameter of the response object and use assertions to check the validity.

As a reminder, you can use a fixture by passing it as parameter to the test function. This passes the 'client' fixture
you created in the last activity to a test function:

```python
def some_test(client):
```

To make an HTTP request using the 'client' you can make a request. The requests can be any HTTP method and you can also
pass request parameters.

This is explained in the Flask documentation
in [Sending Requests with the Test Client](https://flask.palletsprojects.com/en/stable/testing/#sending-requests-with-the-test-client)
which you should read now.

This is a simple example of a GET request to the home page ('/'). The variable 'response' will be used to access the
HTTP
response that is returned from the GET request to the '/' route of your app:

```python
response = client.get("/")
```

The [Flask response object](https://flask.palletsprojects.com/en/stable/api/#flask.Response) has various attributes, you
most will likely use the following:

- the HTTP status code (`request.status_code`)
- page content (`response.data`).
- page header details such as the content type (`response.header["Content-Type"]`)
- the JSON payload (`response.json`)

The more common [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) you might expect are:

- 404 NOT FOUND
- 200 OK for successful GET, DELETE, or PATCH requests
- 201 CREATED for POST or PUT requests creating a new resource
- 500 INTERNAL SERVER ERROR This might indicate a problem with the request, or might indicate a problem in the server
  side code.

To see what the attributes of the Flask response object look like; add the following code to `test_routes.py` and run
it.:

```python
def test_print_response_params(client):
    """
    This is just so you can see what type of detail you get in a response object.
    Don't use this in your tests!
    """
    response = client.get("/")
    print("Printing response.headers:")
    print(response.headers)
    print('\n Printing response.headers["Content-Type"]:')
    print(response.headers['Content-Type'])
    print("Printing response.status_code:")
    print(response.status_code)
    print("Printing response.data:")
    print(response.data)
    print("Printing response.json:")
    print(response.json)
```

Now delete the code you just added as you don't need it in the test code.

## Test the home page is successful when accessed using a GET HTTP request

Aspects to check that show the home page was returned include:

- status code should be 200 OK
- should have the words "summer" and "winter" in the page content
- should have several urls in the content

A test should test one thing, that does not necessarily mean one assertion. You could decide to have 3 tests for the
above, or one test with three assertions.

For example:

```python
def test_index(client):
    """
    GIVEN a Flask test client
    WHEN a request is made to /
    THEN the status code should be 200
    AND the words "Winter" and "Summer" should be in the page content
    AND at least 25 urls should be in the content
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b'Winter' in response.data
    assert b'Summer' in response.data

    count_href = response.data.count(b'href')
    print(count_href)
    assert count_href >= 25
```

### Test for an HTTP method that is not allowed

Write a test that an HTTP POST request for the home page route should return an HTTP error.

This route only accepts GET requests so it should return an 'HTTP Method not allowed' status
code, [405](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405).

```python
def test_index_fails_post_request(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /
    THEN the status code should be 405
    """
    response = client.post("/")
    assert response.status_code == 405
```

Now add tests yourself using GET for:

- /event/1 - this should return a page with details of an event that include 'Highlights'
- '/event/1000' - this should return a 404 Not found status code and include the words 'Event not found'

### Test a POST route with form data

Refer to
the [Flask test documentation for passing form data](https://flask.palletsprojects.com/en/stable/testing/#form-data).

The following tests that a prediction can be made. To do this you need to make a request that simulates the prediction
form being submitted.

```python
def test_prediction_form_post_success(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /predict with valid form data
    THEN the status code should be 200
    AND there should be "prediction" in the page content
    """
    form_data = {
        "year": 2030,
        "team": "Germany",
    }

    response = client.post("/predict", data=form_data)
    assert response.status_code == 200
    assert b'Prediction' in response.data
```

### Test a POST route that adds to the database

When you add a new Quiz, if it is successful it redirects you to the home page. To test this you need to enable the
request to follow any redirects using `follow_redirects=True`.

It should also succeed in adding a row to the database. This will use the db_session fixture that is auto used by all
tests.

```python
def test_new_quiz_form_post_success(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /quiz with valid form data
    THEN the status code should be 200
    AND it should redirect to '/'
    AND there should be "Quiz added!" in the page content
    AND there should be one more row in the database than before
    """
    form_data = {
        "quiz_name": "Test New Quiz",
        "close_date": "01/01/2025",
    }

    response = client.post("/quiz", data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Quiz added!' in response.data

    # Check that the new quiz is in the database
    from student.flask_paralympics.models import Quiz
    quiz = db_session.query(Quiz).filter(Quiz.quiz_name == "Test Quiz").first()
    assert quiz is not None
```

Run the test and look at the error report to see why it fails.

You need to turn off CSRF protection for the tests. Update the fixture that creates the app to configure
`'WTF_CSRF_ENABLED': False`

## Write your own route tests

This depends on which routes you have written. Look at your routes and try to write tests that:

- test what happens when the route succeeds
- test what happens when an unexpected value is passed
- test what happens when the wrong method is used
- test that adds data to the database
- test that updates data in the database
- test the deletes data from the database

## Unit tests

You can also write unit tests for the 'helper' functions that are used by your routes. These do not require the test
client as they are not accessed as HTTP requests and don't require the Flask app to be running.

Functions that you could write unit tests for include `make_prediction` and `get_teams` (only the sqlite3 version of the
activities will have get_teams).

You can also write tests for the Python classes in `models.py` and `forms.py`.

Unit testing with pytest was covered in COMP0035. An example of tests for `make_prediction` are:

```python
def test_prediction_returns_int():
    """
    GIVEN a function to make_prediction
    WHEN a request is made to get_prediction with valid data
    THEN the result should be an integer
    """
    from student.flask_paralympics.paralympics import make_prediction
    prediction = make_prediction(2030, "Germany")
    assert isinstance(prediction, int)


def test_prediction_no_data_returns_error():
    """
    GIVEN a function to make_prediction
    WHEN a request is made to get_prediction with invalid data
    THEN the result should be an error message with 'Error making prediction'
    """
    from student.flask_paralympics.paralympics import make_prediction
    prediction = make_prediction(2030, "Invalid")
    assert "Error making prediction" in prediction
```
