# Page with the map and stats card
import dash
import dash_bootstrap_components as dbc
from dash import html, register_page, dcc, callback
from dash.dependencies import Input, Output
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from figure import scatter_geo, create_card

# register the page in the app, this is the default page
register_page(__name__, path='/events', name='Events', title='Events')

# layout defined as a variable named 'layout'. This is the variable name that is specified in the Dash documentation.
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Paralympic Events"),
            html.P("Explore Paralympic Games locations and event details.")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='geo-map', figure=scatter_geo())
        ], width=8),
        dbc.Col([
            html.Div(id='card-container', children=[
                create_card("Beijing 2022")
            ])
        ], width=4)
    ])
], fluid=True)

@callback(
    Output("card-container", "children"),
    [Input("geo-map", "clickData")]
)
def update_card(click_data):
    if click_data is None:
        return create_card("Beijing 2022")
    else:
        location = click_data['points'][0]['hovertext']
        return create_card(location)
