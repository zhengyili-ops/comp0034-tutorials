from flask import render_template

# Pages generated from data in a database

For this activity you will modify the home page so that it lists all the paralympics with hyperlinks. When you click on
a hyperlink, it should open a more detailed page about that paralympics.

You will need to create:

1. Home page with all paralympics

    - a route that returns events with the event id, host city name, year, type and a URL to the detailed page for that
      paralympics, sorted by type then year.
    - a Jinja template that iterates the events and generates a list of paralympics with the name and year hyperlinked

2. Page for each paralympics

    - a route that takes an event_id and returns details of the event
    - a Jinja template that displays the details

## Home page

### Route

Write a route for `'/'` that gets a list of all paralympics:

1. Query the database and get for each event get the 'event.event_id', 'host.host', 'event.year' and event.type columns.
   Order by type then year.
2. Pass the data to a jinja template to generate the page.

The following code gives a scaffolded solution, you can use this and add the missing code.

Refer to activity 7.6 for query syntax.

```python
@main.route('/', methods=['GET'])
def index():
    """ Returns the home page."""
    # Query the database to get all the events and arrange in date order
    query =  # select Event.event_id Event.type and Event.year and Host.host from Event join to HostEvent using relationship Event.host_events join to HostEvent to Host using relationship HostEvent.host
    events = db.session.execute(query).scalars()
    # Events in this instance is Python objects
    return render_template('events.html', events=events)
```

For sqlite3:

- the table names are lower case, and words are separated with underscore e.g. event.type, host_event.event_id
- complete `query =` using SQL JOIN and specify the ON clause to join event to host_event and host_event to host
- to execute the query you need to use the `db = get_db()` and `db.execute(query).fetchall()` - see activity 7.7.
- the query returns a list of sqlite3 Row results, as this is what is defined in the get_db() function. sqlite3.Row
  tells the connection to return rows that behave like dicts. This allows accessing the columns by name.

### Jinja page template

Create a Jinja template that iterates the data and generates a list of hyperlinks to that paralympics detail page.

You can iterate the data passed to the template using a Jinja for loop e.g.

```jinja
    {%  for event in events %}
        
    {% endfor %}
```

An HTML hyperlink is created using an `<a href="url"></a>` tag where the "url" will be a request to a route that is yet
to be written.

Flask has a function to find a URL from a route, `Flask.url_for()`.

If the route function is named "event" e.g.:

```python
@main.route('/event/<int:event_id>')
def get_event(event_id):
    return "temporary message"
```

then the url will be constructed using:

`<a href="{{ url_for('main.get_event', event_id=event.event_id) }}">{{ event.year }} {{ event.host }}</a>`

- 'main.event' is the blueprint name and the route function name
- 'event_id=' is the parameter passed to the get_event(event_id) function

The full template code looks like this:

```jinja
{% extends "layout.html" %}
{% block title %}Paralympics{% endblock %}
{% block content %}
<h1>Paralympics</h1>
<div class="row">
    <div class="col-4">
        <h2>Summer paralympics</h2>
        {# For loop to iterate each event and add a row linked text #}
        {% for event in events %}
            {% if event.type == 'summer' %}
                {# text with a hyperlink to the page #}
                <a href="{{ url_for('main.get_event', event_id=event.event_id) }}">{{ event.year }} {{ event.host }}</a>
                <br>
            {% endif %}
        {% endfor %}
    </div>
    <div class="col-4">
        <h2>Winter paralympics</h2>
        {# For loop to iterate each event and add a row linked text #}
        {% for event in events %}
            {% if event.type == 'winter' %}
                {# text with a hyperlink to the page #}
                <a href="{{ url_for('main.get_event', event_id=event.event_id) }}">{{ event.year }} {{ event.host }}</a>
                <br>
            {% endif %}
        {% endfor %}
    </div>
</div>
{% endblock %}
```

## Run the app

Run the flask app  `flask --app paralympics_flask run --debug` and check that the route works.

It will fail if you didn't add in the placeholder code for the `get_event` route. If this happens, complete the next
page then try again.

## Event page
Less code is given to allow you to work it out yourself.

### Route

Choose some of the event details to be displayed. Choose any of the attributes from the database tables. You may need to
join tables to get the data you want.

Write the code that will query the database and return these attributes and add it to the route:

```python
@main.route('/event/<int:event_id>')
def get_event(event_id):
    event_data =  # add code to query the database to get the attributes you want for the event
    return render_template('event.html', event=event_data)
```

### Create a template

- Create a template
- Inherit the layout.html
- Add the page title
- Add HTML and Jinja to the "content" block:
    - Choose an HTML layout for example a table, a bootstrap card, paragraphs etc.
    - Use values from the 'event' attributes

```jinja
{% extends "layout.html" %}
{% block title %} Details {% endblock %}
{% block content %}
    {# add your code here #}
{% endblock %}
```

Run the flask app if not still running  `flask --app paralympics_flask run --debug`, go to the home page, click on a
hyperlink

[Next activity](8-3-page-api.md)