from dash import register_page, html, dcc
import dash_bootstrap_components as dbc

register_page(__name__, path='/', name='Overview', title='Overview')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("London Waste Management Analysis", className="text-center mb-4"),
            html.P("Explore recycling and waste management data across London boroughs and surrounding areas.", 
                   className="lead text-center")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Recycling Analysis", className="card-title"),
                    html.P("Analyze recycling rates and trends across different regions."),
                    dbc.Button("Explore Recycling", href="/recycling", color="primary")
                ])
            ], className="mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Waste Management", className="card-title"),
                    html.P("Investigate waste collection and disposal patterns."),
                    dbc.Button("Explore Waste", href="/waste", color="primary")
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Key Statistics"),
                dbc.CardBody([
                    html.Div(id="overview-stats")
                ])
            ])
        ])
    ])
], fluid=True) 