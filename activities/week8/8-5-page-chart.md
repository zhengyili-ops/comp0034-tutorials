# Page with a chart

The interactive charts you created in Dash require JavaScript for the browser-based user interactions. Most chart
libraries for web apps use JavaScript.

For the coursework, only Python code is assessed so please do not spend time writing pages in JavaScript.

You can display charts created in plotly in a browser page. It is also possible to embed your Dash app as a route in
Flask ([see 8-8](8-8-other.md)).

To create a plotly or chart in a page you need:

1. Code that creates a chart
2. A template that displays the chart
3. A route the calls the code to create the chart and passes this to the template

## Create the chart

Use a plotting library to create the chart and then convert it to a format that can be embedded in a webpage.

This example uses `Plotly.express` and converts the chart to HTML using
the [.to_html function](https://plotly.com/python/interactive-html-export/).

Create a function to generate a chart.

You can create a chart using Plotly Express or Go with a pandas DataFrame as you did in the Dash app.

To create a dataframe from a query, use the `pd.read_sql_query()` function.

```python
# Using SQLAlchemy
# Construct the query using FlaskSQLAlchemy
stmt = db.select(Event, Participants).join(Participants)
# Get the data from the database using pandas.read_sql_query, the database engine is from the SQLAlchemy db object
line_chart_df = pd.read_sql_query(stmt, db.get_engine())

# Using sqlite3
# Construct the SQL query string
stmt = 'SELECT * FROM event JOIN participants on event.event_id = participants.event_id;'
# Get the data from the database using pandas.read_sql_query and the sqlite3 database connection from get_db()
df = pd.read_sql_query(stmt, db)
```

There is an example of code to create a line chart in `placeholder/figures.py` (different versions for sqlite3 or
SQLAlchemy).
Move and rename the `figures.py` module to your app package or copy the function into your modules that has the routes.

## Route

The route code creates the chart html by calling the `line_chart()` function.

```python
@main.get('/chart')
def display_chart():
    """ Returns a page with a line chart. """
    line_fig = line_chart(feature="participants", db=db)
    return render_template('chart.html', fig_html=line_fig)
```

Note: if you are using sqlite3, add a line before `line_fig = ` to create the db instance using `db = get_db()`.

## Create a Jinja page template

The chart template needs to have code that will display a plotly chart.

In the route above you passed a variable named `fig_html` that has the html for the chart in. To access the figure in
this use `fig_html.fig`.

You need to turn off auto-escaping when rendering the html which you can do using the `|safe` filter.

The code looks like this: `{{ fig_html.fig | safe }}`. Add this to the content block of the template.

## Run the app

Run the flask app  `flask --app paralympics_flask run --debug` and check that the route
works <http://127.0.0.1:5000/chart>

## Challenge

Can you add a dropdown select to the line chart page and make the chart change dynamically when the different chart type
is selected without using JavaScript?

Hint: Create a select in a form.

The option values for the select are "sports", "participants", "events", and "countries".

[Next](8-6-page-ml.md)