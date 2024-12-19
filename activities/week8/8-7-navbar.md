# Finishing touches

## Remove unused routes

Remove any routes that are no longer used. For example, the ones with fixed values to create the quiz etc. that were
created in week 7.

## Update the navbar

Add the urls for the new pages to a navbar in `layout.html`.

If you don't have a navbar then move `navbar.html` from the placeholder directory to templates and update `layout.html` 
to include this before the main content area in the body, e.g.

```HTML
<body>
<header>
    {% include 'navbar.html' %}
</header>
```

Use the `url_for()` to generate the URLs.

For example:

```html

<li class="nav-item active">
    <a class="nav-link" href="{{ url_for('main.index')}}">Home</a>
</li>
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('main.display_chart')}}">Chart</a>
</li>
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('main.get_news') }}">News</a>
</li>
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('main.quiz')}}">Quiz</a>
</li>
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('main.predict')}}">Prediction</a>
</li>
```

[Next](8-8-other.md)
