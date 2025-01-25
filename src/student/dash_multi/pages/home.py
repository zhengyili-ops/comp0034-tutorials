from dash import register_page, html, dcc
import dash_bootstrap_components as dbc

register_page(__name__, path='/', name='Home', title='Home')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Paralympics Data Analytics"),
            html.P("Welcome to the Paralympics Data Analysis Dashboard. Explore historical data from the Paralympic Games.")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Charts", className="card-title"),
                    html.P("Explore trends and patterns in Paralympic data through interactive visualizations."),
                    dbc.Button("Go to Charts", href="/charts", color="primary")
                ])
            ], className="mb-4")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Events", className="card-title"),
                    html.P("View detailed information about Paralympic events and host cities."),
                    dbc.Button("Go to Events", href="/events", color="primary")
                ])
            ], className="mb-4")
        ], width=6)
    ])
], fluid=True) 