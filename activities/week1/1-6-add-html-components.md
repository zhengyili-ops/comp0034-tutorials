# 6. Adding HTML components to the layout

In this activity you will add the HTML components to the layout. Chart components will be added next week.

## Information to support the activities

You will need to refer to the [Dash html components reference](https://dash.plotly.com/dash-html-components) for
paragraph (html.P), heading 1 (html.H1) and image (html.Img).

#### Row 1

Refer to the [Dash html components reference](https://dash.plotly.com/dash-html-components) for
paragraph (html.P) and heading 1 (html.H1).

The first row has a heading level 1 with the app name and a paragraph with some descriptive
text (or use [lorem ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum)
placeholder text).

For example:

```python
html.H1("Paralympics Data Analytics"),
html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent congue luctus elit nec gravida.")
```

Add an `html.H1` and `html.P` inside the `children=[]` of the column in row one in your `app.layout`.

#### Row 2

The second row has two columns:

- column 1 contains an [HTML select (dropdown)](https://www.w3schools.com/tags/tag_select.asp).
- column 2 contains an [input of type=checklist](https://www.w3schools.com/tags/tag_input.asp)

The dropdown and checkbox can be created in Dash using either:

- [Dash Bootstrap Components (dbc)](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/input/)
  which includes
  `dbc.Select()` and `dbc.Checklist()`; or
- [Dash Core Components (dcc)](https://dash.plotly.com/dash-core-components) which includes `dcc.Dropdown` and
  `dcc.Checklist`

Use the appropriate syntax depending on the type you want to use.

The following example uses the `dbc` version of the components.

As with row 1, you need to add these to the 'children=' attribute of the relevant Column.

```python
# Column 1 children
dbc.Select(
    options=[
        {"label": "Events", "value": "events"},  # The value is in the format of the column heading in the data
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events",  # The default selection
    id="dropdown-input",  # id uniquely identifies the element, will be needed later for callbacks
),

# Column 2 children
html.Div(
    [
        dbc.Label("Select the Paralympic Games type"),
        dbc.Checklist(
            options=[
                {"label": "Summer", "value": "summer"},
                {"label": "Winter", "value": "winter"},
            ],
            value=["summer"],  # Values is a list as you can select 1 AND 2
            id="checklist-input",
        ),
    ]
)
```

### Row 3

Refer to the [Dash html components reference](https://dash.plotly.com/dash-html-components) for `html.Img`.

Images are placed in the `/assets` directory. To reference these in the `src=` parameter use the `app.get_asset_url()`
function. In the brackets specify the file name and any subdirectory below the `/assets` directory.

In this example you also need to add a Boostrap class name which you can find in
the [Bootstrap reference](https://getbootstrap.com/docs/5.0/content/images/#responsive-images). Confusingly, the syntax
for adding a class to a dbc component is not `class=` but `className=`.

For example to define responsive images using the image files in the `/assets` directory:

```python
# Column 1 children
# className="img-fluid" is a Bootstrap class and prevents the image spanning the next column
html.Img(src=app.get_asset_url('line-chart-placeholder.png'), className="img-fluid"),

# Column 2 children
html.Img(src=app.get_asset_url('bar-chart-placeholder.png'), className="img-fluid"),
```

#### Row 4

This row has:

- column 1: a map visualisation with markers for events. Add a placeholder image for now.
- column 2: a card that displays details for a selected paralympic event, this will be dynamically generated when the
  event is clicked on. Add sample text for now.

You should be able to add the image to column 1 using the same approach you just used in row 3.

The card is more challenging. Refer to
the [dbc.Card reference](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/).

```python
# Column 2 children
dbc.Card([
    dbc.CardImg(src=app.get_asset_url("logos/2022_Beijing.jpg"), top=True),
    dbc.CardBody([
        html.H4("Beijing 2022", className="card-title"),
        html.P("Number of athletes: XX", className="card-text", ),
        html.P("Number of events: XX", className="card-text", ),
        html.P("Number of countries: XX", className="card-text", ),
        html.P("Number of sports: XX", className="card-text", ),
    ]),
],
    style={"width": "18rem"},
)
```

Run the app and check it displays as you expected. The design could be improved so feel free to make any changes you
wish!

[Next activity](1-7-multipage-app.md)