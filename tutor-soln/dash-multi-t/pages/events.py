# Page with the map and stats card
import dash_bootstrap_components as dbc
from dash import dash, dcc, html

# register the page in the app
dash.register_page(__name__, name='Events', title='Events', path="/", )

# The rows are in a separate Python module called layout_events.py
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Event Details", id="event-h1"),
            html.P(
                "Event details. Select a marker on the map to display the event highlights and summary data.")
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col(children=[
            # Chart replaced the placeholder image
            dcc.Graph(figure=map, id="geo-map"),
        ], width=8),
        dbc.Col(children=[
            card,
        ], width=4),
    ], align="start")

])
