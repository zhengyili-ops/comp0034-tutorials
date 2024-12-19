# Page that returns a prediction from a machine learning model

For this you need to already know how to create a machine learning model as this is not taught in the course.

Code to generate a simple prediction of the total medals for a country is in `placeholder/create_ml_model.py`.

For the Flask activity you can use the `model.pkl` file that has been saved in the `data` package.

## Function to get a prediction
You need to be able to get a prediction using the model.

Add the following function to your code, either in a module of 'helper' functions, or in the file that has the routes.

```python
import importlib.resources

import joblib
import pandas as pd


def make_prediction(year, team):
    """Takes the year and team name and predicts how many total medals will be won

    Parameters:
    year (int): The year of the prediction
    team (str): The name of the team

    Returns:
    prediction (str or int): int of the prediction result, or string if error
    """
    # The predict() method fails if not in DataFrame format
    input_data = pd.DataFrame({'Year': [year], 'Team': [team]})

    # Get a prediction from the model
    with importlib.resources.open_binary('student.data', 'model.pkl') as file:
        model = joblib.load(file)
    try:
        prediction = model.predict(input_data)
        # predict() returns a float so convert to int and handle negative predictions
        return max(0, int(prediction[0]))
    except Exception as e:
        return f"Error making prediction: {e}"
```

## Form

Create a form that contains 2 fields:

- year: the year to predict the total medals for
- team: a list of team names from the Country table in the database

The first version below uses a QuerySelectField which is only available if you are using SQLAlchemy and also install `WTForms-SQLAlchemy`.

```python
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.fields.numeric import IntegerField

def teams():
    """Return a query to get the list of teams for the QuerySelectField.
    https://wtforms-sqlalchemy.readthedocs.io/en/latest/wtforms_sqlalchemy/#wtforms_sqlalchemy.fields.QuerySelectField
    """
    return db.session.execute(db.select(Country).where(Country.member_type != 'dissolved')).scalars()


class PredictionForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired()])
    team = QuerySelectField('Team', query_factory=teams, get_label='name', allow_blank=True, validators=[DataRequired()])
```

This version should work for students not using SQLAlchemy, or who use SQLAlchemy but don't want to use the QuerySelectField:

```python
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired


class PredictionForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired()])
    team = SelectField('Team', choices=[], validators=[DataRequired()])
```

## Page template

The page renders a form with the two fields. The code below is using the render_form macro to do this.

The `<p>` at the end is where the prediction result will be shown when the form has been submitted.

Save this to a template file, e.g. `prediction.html`.

```html
{% extends 'layout.html' %}
{% from 'form_macros.html' import render_form %}
{% block title %}Prediction{% endblock %}
{% block content %}
<div class="col-md-6">
    <form method="POST" action="">
        {{ render_form(form) }}
        <br>
        <button type="submit" class="btn btn-primary">Predict total medals</button>
    </form>
</div>
<br>
<p class="text-bg-info">{{ prediction_text }}</p>
{% endblock %}
```

## Route

The route needs to:

- on GET show an empty prediction form
- on POST take the value form the form and get a prediction

The route to GET the form is as you just created for the Quiz page:

```python
@main.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictionForm()
    return render_template("prediction.html", form=form)
```

The POST route requires:

- Get the values from the form. This is similar to quiz except that the team has a Row result so to access the
  Country.name and not a Country row, use `form.team.data.name`.
- Call the method to get a prediction result
- Send a string with the prediction to the prediction template to display it.

The code might look like this:

```python
import importlib.resources

import joblib
import pandas as pd
from flask import render_template
from student.flask_paralympics.forms import PredictionForm


@main.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictionForm()

    if form.validate_on_submit():
        # Get all values from the form
        year = form.year.data
        team = form.team.data.name

        # Make the prediction
        prediction = make_prediction(year, team)

        # If the prediction returns an error message rather than a number, print a different message
        if type(prediction) != int:
            prediction_text = f"Sorry, insufficient data to predict a result, please select a different team"
        else:
            prediction_text = f"Prediction: {form.team.data.name} will win {prediction} medals in {form.year.data}!"

        return render_template(
            "prediction.html", form=form, prediction_text=prediction_text
        )
    return render_template("prediction.html", form=form)
```

This version should work for students using sqlite3. You could also adapt this to work with SQLAlchemy by changing the 
query in `get_teams()`. 

```python
@main.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictionForm()
    # Set the choices for the SelectField
    form.team.choices = get_teams()

    if form.validate_on_submit():
        # Get all values from the form
        year = form.year.data
        team = form.team.data

        # Make the prediction
        prediction = make_prediction(year, team)

        # If the prediction returns an error message rather than a number, print a different message
        if type(prediction) != int:
            prediction_text = f"Sorry, insufficient data to predict a result, please select a different team"
        else:
            prediction_text = f"Prediction: {form.team.data} will win {prediction} medals in {form.year.data}!"

        return render_template(
            "prediction.html", form=form, prediction_text=prediction_text
        )
    return render_template("prediction.html", form=form)


def get_teams():
    """Get the list of teams for the SelectField in the PredictionForm.

    Returns:
        choices in the format [(value, label), ...]
        """
    db = get_db()
    sql = 'SELECT name FROM Country WHERE member_type != "dissolved"'
    countries = db.execute(sql).fetchall()
    return [(name, name) for name, in countries]
```

Run the app and go to the `/predict` route.

[Next activity](8-7-navbar.md)