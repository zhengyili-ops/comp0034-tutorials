# Page with the line chart
import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

# register the page in the app
register_page(__name__, name="Charts", title="Charts")


# This uses the option to create the layout as a function
# see https://dash.plotly.com/urls#layout
def layout(**kwargs):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Charts"),
                html.P("Try to answer the questions using the charts below.")
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col(children=[
                dbc.Select(
                    id="type-dropdown",  # id uniquely identifies the element, will be needed later
                    options=[
                        {"label": "Events", "value": "events"},
                        # The value is in the format of the column heading in the data
                        {"label": "Sports", "value": "sports"},
                        {"label": "Countries", "value": "countries"},
                        {"label": "Athletes", "value": "participants"},
                    ],
                    value="events"  # The default selection
                )], width=2),
            dbc.Col(children=[
                # Placeholder image to represent the chart
                dcc.Graph(figure=line, id="line-chart"),
            ], width=4),
            dbc.Col(children=[
                type_checklist,
            ], width=2),
            dbc.Col(children=[
                # Chart replaced the placeholder image
                dcc.Graph(figure=bar, id="bar-chart"),
            ], width=4),
        ],
            align="start")
    ])
