# Content from 3rd party REST APIs

An API is an application programming interface; it allows programmers to connect one software to another.
APIs have methods that developers can access to do something.

A REST API is one that conforms to the REST architecture or pattern. These use the HTTP request/response method and
return data in a structured format, often in JSON format. You can then use the data received in HTTP response in your
own app.https://www.contextualwebsearch.com/

There are many published REST APIs, and while many are free they often require you to register and obtain an API key.
To find one try:

- [apipheny](https://apipheny.io/free-api/)
- [GitHub repos of APIs grouped by topic](https://github.com/public-apis/public-apis?tab=readme-ov-file)
- [Any API](https://any-api.com/)

## API format

This activity uses [HackerNews](https://github.com/HackerNews/API) which is a free API that doesn't require a key and so
making it easier for tutorial purposes.
Unfortunately I could not find a more relevant API that did not require a key.

The URL that the activity uses is
the [news stories](https://github.com/HackerNews/API?tab=readme-ov-file#new-top-and-best-stories):
`https://hacker-news.firebaseio.com/v0/topstories.json`

This returns a list of item ids.

A subsequent call to the item id using `https://hacker-news.firebaseio.com/v0/item/<itemid>.json` returns JSON in the
following structure for each news article:

```JSON
{
  "by": "dhouston",
  "descendants": 71,
  "id": 8863,
  "kids": [
    8952,
    9224
  ],
  "score": 111,
  "time": 1175714200,
  "title": "My YC app: Dropbox - Throw away your USB drive",
  "type": "story",
  "url": "http://www.getdropbox.com/u/2/screencast.html"
}
```

## Flask route to get data from a REST API

The general steps for a Flask route that gets data from a REST API and uses it in an HTML page are:

- Submit an HTTP request to the API. A popular Python package for this is `requests` which is part of the core Python
  library so you don't need to install it. The format of the query URL will depend on API and should be explained in
  their documentation.
- The result of the request will be a HTTP response that has data attached. The data is typically in JSON format. The
  format depends on the API and again should be explained in their documentation.
- Get the JSON content from the HTTP response.
- Pass the JSON to the Jinja template. You may need to manipulate the JSON in some way if it is not exactly what you
  want.
- Access the JSON in the template.

## Create a route for the paralympics app

Add a route to the paralympics app to get the top stories:

```python
import requests
from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/news')
def get_news():
    """Get the top stories from Hacker News.
    NB: The page will be slow to load due to the number of requests made to the Hacker News API so limited to 3 stories.
    """
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    item_ids = response.json()
    stories = []
    # Get 3 stories
    for i in range(3):
        url = f"https://hacker-news.firebaseio.com/v0/item/{item_ids[i]}.json"
        response = requests.get(url)
        stories.append(response.json())
    return render_template('news.html', stories=stories)
```

## Create a news page template

Create a template, `news.html`.

Access the JSON values for the url and the title and display as hyperlinks on the page.

```jinja
{% extends "layout.html" %}
{% block title %}News{% endblock %}
{% block content %}
    <h2>Latest news</h2>
    {% for story in stories %}
        <a href="{{ story.url }}">{{ story.title }}</a>
        <br>
    {% endfor %}
{% endblock %}
```

## Try it yourself

Find an API from one of the links above and try to add a page with content received from the API.

[Next activity](8-4-page-form.md)