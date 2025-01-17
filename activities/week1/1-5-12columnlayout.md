# 5. Create a responsive layout using a 12-column grid layout with Bootstrap

## Responsive design with CSS

The intent of responsive design is to make web pages look good on all devices: desktop, tablets, and phones. There are
techniques to achieve responsive web design such as resize, hide, shrink, enlarge, move the content.

To create a web page that is responsive:

- Set the viewport
- Use responsive images
- Use responsive text
- Use media queries (apply a different style for different screen sizes)
- Optionally, use a grid layout

The **viewport** is the visible area inside the browser window. A `<meta>` viewport element gives the browser
instructions on how to control the page's dimensions and scaling. This gives the browser instructions on how to control
the page's dimensions and scaling. For example the following code would be placed in the `<head>` section of a html
document.

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

- `width=device-width` sets the width of the page to follow the screen-width of the device (varies depending on the
  device).
- `initial-scale=1` sets the initial zoom level when the page is first loaded by the browser.

You already set this for the paralympics app in the last activity.

## Responsive design with Bootstrap in Dash

To use Bootstrap in a responsive way, the minimum you need is:

1. Include the `<meta>` tag in the `<head>` to set the page width to the device
   `<meta name="viewport" content="width=device-width, initial-scale=1">`.
2. Wrap the page contents in an HTML `<div>` tag that has a container CSS class. Bootstrap offers two container classes:
    - `.container` class provides a responsive fixed width container
    - `.container-fluid` class provides a full width container, spanning the entire width of the viewport

As you don't have an HTML file in Dash then to pass in tags that would usually be the head section, you pass them to the
Dash app object. You did this in the previous activity.

```python
from dash import Dash
import dash_bootstrap_components as dbc

# Define a variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Define a variable that contains the meta tags
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Wrap the layout in a Bootstrap container
app.layout = dbc.Container(
    # The rest of the html contents can go here
)
```

You can wrap individual elements in Containers rather than the entire page. The above is just one approach.

## Create the 12 column layout for the Paralympics app

Remove any content you currently have from previous activities inside the `app.layout` so you just have:

```python
# Wrap the layout in a Bootstrap container
app.layout = dbc.Container([
    # The layout will go here
])
```

For this activity, create the following grid structure in your `app.layout` using Dash Bootstrap component (dbc) styles.

<img alt="12 column grid layout" src="../img/grid.png" style="width: 50%;">

You may need to refer to the following:

- [Dash bootstrap components layout documentation](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/)
- [Dash tutorial on styling](https://dash.plotly.com/tutorial#styling-your-app)
- [Bootstrap grid documentation](https://getbootstrap.com/docs/5.0/layout/grid/)

The components you add provide the structure in which to later place other components. If you only create the structure, 
when you load the page it will appear blank. To address this, use placeholder text in the 'children' to show what each
component will be used for. You will later remove this text and add the actual components.

In row 2 there are 'gaps' between the columns. This can be achieved using a style parameter 'offset'.

The first two rows are given for you below. Add rows 3 and 4 yourself.

To structure the code and make it easier to read, each row is defined as a variable, and then these variables added to
the layout. You can just place all the code straight in the layout without using variables.

```python
import dash_bootstrap_components as dbc

# Code to create the app is omitted from the example 

row_one = dbc.Row([
    dbc.Col(['App name and text']),
])

row_two = dbc.Row([
    dbc.Col(children=['drop down'], width=4),
    dbc.Col(children=['check boxes'], width={"size": 4, "offset": 2}),
    # 2 'empty' columns between this and the previous column
])

app.layout = dbc.Container([
    row_one,
    row_two,
])
```

Same but without defining the rows as variables:

```python
import dash_bootstrap_components as dbc

# Code to create the app is omitted from the example 

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(['App name and text']),
    ]),
    dbc.Row([
        dbc.Col(children=['drop down'], width=4),
        dbc.Col(children=['check boxes'], width={"size": 4, "offset": 2}),
    ])
])
```

[Next activity](1-6-add-html-components.md)