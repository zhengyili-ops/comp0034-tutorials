# 4. Add Bootstrap CSS styles using Dash Bootstrap Components

You should have installed Dash Bootstrap Components in the set-up activities for the tutorial.

## CSS overview

CSS stands for Cascading Style Sheets. It provides styles for HTML elements.

Web browsers apply CSS rules to a document. A CSS **rule** consist of:

- A **selector**, which selects the element(s) you want to style

- A declaration which is a set of **properties** with values

The following CSS rule selects the paragraph tag `p` and makes the font colour red and the text center-aligned.

```css
p {
    color: red;
    text-align: center;
}
```

A set of these CSS rules are called a **stylesheet**.

CSS can be added to HTML elements in 3 ways:

- **Inline**: using the style attribute in HTML elements
- **Internal**: using a `<style>` element in the `<head>` section
- **External**: using an external CSS file e.g. `my_css.css`.

An **Inline style** affects one element only and is defined in the `style'=""` attribute of that HTML element
e.g. `<h1 style="color: blue; background-color: yellow;">Hello World! </h1>`. Avoid using this method as it is much
harder to maintain!

An **internal stylesheet** places CSS inside a `<style>` element contained inside the HTML `<head>` section.

An **external CSS file** is usually the preferred method and is used in most COMP0034 example code. CSS is
written in a separate file with a `.css` extension.
The stylesheet `.css` file is referenced in the `<head>` section of the html using an HTML `<link>` element.

## Adding CSS in a Dash app

### Inline styles

In Dash you apply an inline style using the style property of an HTML component e.g.:

```python
app.layout = html.Div([
    html.Div(className='row', children='My First App with Data, Graph, and Controls',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
])
```

### External style sheet

In most cases you will use an external stylesheet. This can either be a .css file saved in your project file structure,
or .css hosted elsewhere (usually on a CDN). A CDN (Content Distribution Network) is a
distributed group of servers that caches content and typically has several locations near end users. Its aim is to
improve load times; and for those who use it, to reduce the costs of hosting files themselves.

In Dash you do not have an HTML file, so you define the location of the stylesheet (or stylesheets if you have more than
one) and pass this as a parameter to the Dash app instance. This example uses
the [CDN version of Milligram css](https://milligram.io):

```python
# Import packages
from dash import Dash

# Initialize the app using Milligram css
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.1/milligram.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout etc...
```

To use a local style sheet, place it in the 'assets' folder. This is
explained [here in the Dash documentation](https://dash.plotly.com/external-resources).

### Internal style sheet

There is no straight forward and documented method to do this in Dash.

## Using open source external CSS in Dash

While you can write your own CSS, **for your coursework it is recommended that you use a third party CSS**. Check it has
an open source license, i.e. that you are given permission by its author to use it. Writing your own CSS is not
considered in the mark scheme so writing your own CSS will not improve your marks.

[Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/#quick-start) is a popular CSS library that
has extensive documentation and support and is used in the course materials for
this reason.

Bootstrap is widely used which some say leads to many sites looking similar, others criticisms include the fact that it
is comprehensive, leading to larger file sizes, and yet you may only want to use a small subset of its features. There
are alternatives to Bootstrap you can explore, try searching `alternatives to Bootstrap`, such as:

- [Pure.css](https://purecss.io/start/)
- [Materialize](https://materializecss.com/getting-started.html)
- [ZURB foundation](https://foundation.zurb.com/)

For Dash, there is an additional
library, [dash bootstrap components](https://dash-bootstrap-components.opensource.faculty.ai), that makes Bootstrap
easier to apply to Dash. This is used in the COMP0034 tutorial activities.

Dash bootstrap components has
[themes](https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/) that you can apply to achieve a
particular look and feel.

## Activity: Add Dash Bootstrap Components styling to the paralympics app

This requires the following:

1. Have Dash Bootstrap Components library installed in your Python environment
2. Import the library in your code, usually as `import dash_bootstrap_components as dbc`
3. Add a viewport meta tag. Bootstrap requires this to support the responsive design (explained in activity 3). This is done by
   passing the tag to the 'meta_tags' attribute when the Dash app instance is created.
4. Add the external stylesheet. Pass the Bootstrap stylesheet as an 'external_stylesheets=' attribute when the Dash app
   instance is created. The default theme is `dbc.themes.BOOTSTRAP`, or you can choose
   another [theme](https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/)
5. Encapsulate the layout within a Bootstrap container using the `dbc.Container()` component. This is explained in activity 3.

This is achieved in the code as follows:

```python
from dash import Dash
import dash_bootstrap_components as dbc

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Wrap the layout in a Bootstrap container
app.layout = dbc.Container([
    # Add the HTML layout components in here
])
```

Update your paralympics app to support styling using Dash Bootstrap Components.

[Next activity](1-4-add-bootstrap.md)