""" This is an example of a minimal Flask application."""
# Import the Flask class from the Flask library
from flask import Flask, render_template

# Create an instance of a Flask application
# The first argument is the name of the application’s module or package. __name__ is a convenient shortcut.
# This is needed so that Flask knows where to look for resources such as templates and static files.
app = Flask(__name__)


# Add a route for the 'home' page
# use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def hello_world():
    # The function returns the message we want to display in the user’s browser. The default content type is HTML,
    # so HTML in the string will be rendered by the browser.
    return 'Hello World!'


# A route that uses a template to generate the page
@app.route('/hello')
def hello_with_template():
    # The function renders a template that generates the home page using HTML
    return render_template('hello.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
