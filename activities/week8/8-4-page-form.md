from flask import render_template

# Using forms on pages

Forms in web pages provide a structured way for users to input data direct, allowing applications to collect and store
user information.

[FlaskWTF](https://pypi.org/project/Flask-WTF/) extends a popular library WTForms for generating forms from Python
classes. You will need to install this `pip install Flask-WTF`.

If you are using SQLAlchemy then also
install [WTForms-SQLAlchemy](https://wtforms-sqlalchemy.readthedocs.io/en/latest/wtforms_sqlalchemy/) as this provides
additional form fields such as a QuerySelectField.

This activity creates a form to allow the teacher to create a quiz and questions.

The general approach to create a form that will capture data from a user using FlaskWTF is:

1. Create a Python form class using FlaskWTF with attributes that match the values needed. If using FlaskSQLAlchemy, the
   attributes need to match the class in `models.py`. If using sqlite3 the attributes need to match those in the table
   schema.
2. Create a Jinja/HTML template that displays the form and provides a button to submit the completed form.
3. Create a route that when a GET request is made displays the form, and on POST (form submission) checks the fields are
   valid and if they are saves the data to the database.

## Create the form class

To create a form class use a Flask-WTF form class.

A quiz has the following attributes:

```text
"quiz_id"	PK INTEGER
"quiz_name"	TEXT NOT NULL
"close_date" TEXT
```

The form should have a field that matches each of the fields needed for the database table (except the `quiz_id` as this
is added automatically by the database).

You can also add validation rules to the attributes. These will check that the data the user enters is valid before
trying to save it to the database.

To define a form start with
the [Flask-WTF documentation](https://flask-wtf.readthedocs.io/en/1.2.x/quickstart/#creating-forms).

WTForms provides guidance on secure forms, file uploads and recaptcha. For other fields types you will need to
refer to the [WTForms documentation](https://wtforms.readthedocs.io/en/3.0.x/).

Create a new module called `forms.py`.

The following shows code to create a form for a Quiz.

The close_date field has two validators, one allows it to be NULL, the other checks the format if it is not NULL.

```python
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Optional, Regexp


class QuizForm(FlaskForm):
    quiz_name = StringField('Quiz Name', validators=[DataRequired()])
    close_date = StringField('Date', [
        Optional(),
        Regexp(r'^\d{1,2}/\d{1,2}/\d{4}$', message="Date must be in the format DD/MM/YYYY")
    ])
```

## Template

The template needs to generate an HTML form that matches the fields in form class.

- [Rendering fields](https://wtforms.readthedocs.io/en/3.1.x/crash_course/#rendering-fields) is explained in the WTForms
  documentation. Code is also added to display any field validation errors.
- `{{ form.hidden_tag() }}` is explained in
  the [Flask-WTF documentation](https://flask-wtf.readthedocs.io/en/1.2.x/quickstart/#creating-forms).
- `action=""` means when the form is submitted, stay on the same page.
- You can add values for
  the [form input attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#attributes). For example,
  the size of the input box for the quiz name and Bootstrap class.
- The form below uses [Bootstrap styling](https://getbootstrap.com/docs/4.0/components/forms/).

Save the code below as `quiz.html`.

```html
{% extends 'layout.html' %}
{% block title %}Chart{% endblock %}
{% block content %}
<div class="col-md-6">
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.quiz_name.label }} {{ form.quiz_name(size=40, class="form-control") }}
        </div>
        <div class="form-group">
            {{ form.close_date.label }} {{ form.close_date(class="form-control") }}
        </div>
        <br>
        <button type="submit" class="btn btn-primary">Save Quiz</button>
    </form>
    {% if form.errors %}
    <ul class="errors">
        {% for field_name, field_errors in form.errors|dictsort if field_errors %}
        {% for error in field_errors %}
        <li>{{ form[field_name].label }}: {{ error }}</li>
        {% endfor %}
        {% endfor %}
    </ul>
    {% endif %}
</div>
{% endblock %}
```

### Rendering fields with a Jinja macro

You can define each field; though if you have a lot of fields, use
a [Jinja macro](https://jinja.palletsprojects.com/en/stable/templates/#macros) to generate them.

The macro code can be saved in the `/templates` directory. Copy `form_macros.html` from the `placeholder` directory.
There is one macro to render a field and another that will render all the fields in the form.

For example:

```html

<form method="post" novalidate>
    <!-- Uses macro to render all the fields in the form
    the variable 'form' is passed to the template from the route function in render_template() -->
    {{ render_form(form) }}
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

## Route

The route needs to receive two types of request:

- GET: When the page is first loaded, this returns and empty form
- POST: When the form is submitted

### GET

The GET route logic is:

1. Create an instance of a QuizForm
2. Render the template for the quiz page and pass the form to it

Add this first and check that the form renders on the page.

```python
from student.flask_paralympics.forms import QuizForm


@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    render_template('quiz.html', form=form)
```

### POST

[How to get the form data](https://wtforms.readthedocs.io/en/3.1.x/crash_course/#how-forms-get-data)

The POST route logic is:

1. Check the form passes the validation that was set in the QuizForm class
    - If not, render the template for the quiz page and pass the form to it with the current values (you can get the
      current values from the form in the HTTP request using `request.form`)
2. If yes, get the values from the form and try to save the quiz to the database
    - For SQLAlchemy: Create a quiz object, add and commit.
    - For sqlite3: Construct a SQL statement and commit.
3. If the quiz is saved, flash a success message and redirect to the route for the quiz page. This introduces two new
   Flask functions:

    - [Redirect](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.redirect) to a different route
    - [message flashing](https://flask.palletsprojects.com/en/3.0.x/patterns/flashing/)

The full code could look like this:

```python
from flask import render_template, flash, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from student.flask_paralympics.forms import QuizForm
from student.flask_paralympics.models import Quiz

@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # If the form has been submitted, use the values from it which are accessed using request.form
    form = QuizForm(request.form)

    if request.method == 'POST' and form.validate():
        # Get the values from the form
        quiz_name = form.quiz_name.data
        close_date = form.close_date.data

        # Create a Quiz object
        quiz = Quiz(quiz_name=quiz_name, close_date=close_date)

        # Check it does not already exist.
        existing_quiz = db.session.query(Quiz).filter(Quiz.quiz_name == quiz_name).first()

        # If it does, display a message and do not add it.
        if existing_quiz:
            flash(f"Quiz with name {quiz_name} already exists.")
        # Otherwise, try to add it to the database
        else:
            try:
                db.session.add(quiz)
                db.session.commit()
                # Display a message to confirm it has been added
                flash('Quiz added!', 'success')
                return redirect(url_for('main.index'))
            except SQLAlchemyError as e:
                # If there is an error, display a message and return to the previous form
                flash(f'Error adding quiz: {e}', 'danger')

    return render_template('quiz.html', form=form)

```

To use sqlite3 instead of SQLAlchemy try:

```python
from flask import Blueprint, flash, redirect, render_template, request, url_for

from student.flask_paralympics.db import get_db
from student.flask_paralympics.forms import QuizForm

@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # If the form has been submitted, use the values from it which are accessed using request.form
    form = QuizForm(request.form)

    if form.validate_on_submit():
        print("submitted")
        # Get the values from the form
        quiz_name = form.quiz_name.data
        close_date = form.close_date.data

        # check if a quiz with the same name already exists
        db = get_db()
        existing_quiz = db.execute("SELECT * FROM quiz WHERE quiz_name = ?", (quiz_name,)).fetchone()

        # If it does, display a message and do not add it.
        if existing_quiz:
            flash(f"Quiz with name {quiz_name} already exists.")
        # Otherwise, try to add it to the database
        else:
            try:
                quiz_sql = "INSERT INTO quiz (quiz_name, close_date) VALUES (?, ?)"
                db.execute(quiz_sql, (quiz_name, close_date))
                db.commit()
                # Display a message to confirm it has been added
                flash('Quiz added!', 'success')
                return redirect(url_for('main.index'))
            except sqlite3.Error as e:
                # If there is an error, display a message and return to the previous form
                flash(f'Error adding quiz: {e}', 'danger')
    return render_template('quiz.html', form=form)
```

You also need to add an area to `layout.html` where the flashed messages can be displayed, e.g.

```jinja
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <p class="text-warning">{{ message }}</p>
            {% endfor %}
        {% endif %}
    {% endwith %}
```

## Try it yourself

Try to create at least create one form, template and route yourself so that you understand how to do it. For example, 
add the ability to create a question.

Following the approach above, add forms to add a question to a quiz and to add answer choices to a question. You could
amend the quiz template, form, and route and combine the question and answer choices with this; or you can create
separate forms, templates and routes for each.

There is far more that needs to be done to make the quiz feature function. You could also try adding:

- Create a page that has the options to add quiz, question and answer choice on the same page
- A form that retrieves the quiz and questions from the database and allows the teacher to edit and save changes.
  See <https://wtforms.readthedocs.io/en/3.1.x/crash_course/#editing-existing-objects>.
- Forms that allows a student to enter the quiz, get a score, and optionally save their score to the database.

[Next activity](8-5-page-chart.md)