# 7. Multipage app (optional)

## Introduction and information sources

This activity is optional and is included for those that want to learn to create a multi-page app.

This activity assumes you completed activities 1-4 which cover how to define the layout and apply responsive styling
with Dash Bootstrap Components.

It covers the additional steps required to create a navigation menu and include separate pages.

The following references provide further information and examples:

- [Dash tutorial on multi page apps](https://dash.plotly.com/urls)
- [Dash dbc.Navbar() documentation](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/)
- [GitHub repository with multi-page app examples](https://github.com/AnnMarieW/dash-multi-page-app-demos) - this gives
  examples and code that solves particular challenges associated with multi-page apps.
- [Introducing Dash pages -- A better way to make multi-page apps](https://youtu.be/pJMZ0r84Rqs) video by Adam Schroeder
  and Chris Parmer.
- Charming Data Videos by Adam
  Schroeder: [Creating Multi Page Apps - Part I Getting Started](https://youtu.be/Hc9_-ncr4nU)
  and [Creating Multi Page Apps - Part II Sidebar and Layout Enhancements](https://www.youtube.com/watch?v=MtSgh6FOL7I)

## Paralympics multi-page app

There are three basic steps for creating a multi-page app with Dash Pages:

1. Create individual `.py` files for each page in your app, and put them in a `/pages` directory.

2. In each of these page files:

    - Add a `dash.register_page(__name__)`, which tells Dash that this is a page in your app.
    - Define the page's content within a _variable_ called `layout` or a _function_ called layout that returns the
      content.

3. In your main app file:

    - When declaring your app, set use_pages to True: `app = Dash(__name__, use_pages=True)`
    - Add `dash.page_container` in your app layout where you want the page content to be displayed when a user visits
      one of the app's page paths.

The [dash-multipage](../../src/student/dash_multi) folder already contains a `/pages` directory with two pages:

- `charts.py` contains the line and bar charts and their selectors. This has a **variable** called layout.
- `events.py` contains the map and event details card. This has a **function** called layout.

Page layouts must be defined with a variable or function called layout. When creating an app with Pages, only use
`app.layout` in your main `app.py` file.

You need to add a new python file to create and run the app.

1. Create a new main app file e.g. `app.py` or `paralympics.py` (any name except for dash.py)
2. Add code to create the app as for activity 1.2. Modify the line that creates the app to include `use_pages=True`
   e.g. `app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags, use_pages=True)`
3. Define a navbar.
4. Add the `app.layout` and add the nav_bar and a `dash.page_container` to it. You will need to add the import
   `import dash`

    ```python
    # From https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Event Details", href=dash.page_registry['pages.events']['path'])),
            dbc.NavItem(dbc.NavLink("Charts", href=dash.page_registry['pages.charts']['path'])),
        ],
        brand="Paralympics Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
    )

    app.layout = dbc.Container([
        # Nav bar
        navbar,
        # Area where the page content is displayed
        dash.page_container
    ])
    ```
5. Run the app from the main app file you just created. You should have two pages and a clickable menu bar.

