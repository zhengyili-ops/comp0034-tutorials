from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Define meta tags and stylesheets
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Create the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Define the layout with Bootstrap grid system
app.layout = dbc.Container([
    # Row 1: App name and intro text
    dbc.Row([
        dbc.Col([
            html.H1("Paralympics Data Analytics"),
            html.P("Explore historical data from the Paralympic Games, including information about events, athletes, sports, and participating countries.")
        ], width=12)
    ]),
    
    # Row 2: Drop down and Check boxes
    dbc.Row([
        # Column 1: Dropdown
        dbc.Col([
            dbc.Select(
                options=[
                    {"label": "Events", "value": "events"},
                    {"label": "Sports", "value": "sports"},
                    {"label": "Countries", "value": "countries"},
                    {"label": "Athletes", "value": "participants"},
                ],
                value="events",
                id="dropdown-input",
            )
        ], width=4),
        # Empty space
        dbc.Col(width=4),
        # Column 2: Checklist
        dbc.Col([
            html.Div([
                dbc.Label("Select the Paralympic Games type"),
                dbc.Checklist(
                    options=[
                        {"label": "Summer", "value": "summer"},
                        {"label": "Winter", "value": "winter"},
                    ],
                    value=["summer"],
                    id="checklist-input",
                )
            ])
        ], width=4)
    ]),
    
    # Row 3: Charts
    dbc.Row([
        # Column 1: Line chart
        dbc.Col([
            html.Img(src=app.get_asset_url('line-chart-placeholder.png'), className="img-fluid")
        ], width=6),
        # Column 2: Bar chart
        dbc.Col([
            html.Img(src=app.get_asset_url('bar-chart-placeholder.png'), className="img-fluid")
        ], width=6)
    ]),
    
    # Row 4: Map and Card
    dbc.Row([
        # Column 1: Map
        dbc.Col([
            html.Img(src=app.get_asset_url('map-placeholder.png'), className="img-fluid")
        ], width=8),
        # Column 2: Event details card
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src=app.get_asset_url("logos/2022_Beijing.jpg"), top=True),
                dbc.CardBody([
                    html.H4("Beijing 2022", className="card-title"),
                    html.P("Number of athletes: XX", className="card-text"),
                    html.P("Number of events: XX", className="card-text"),
                    html.P("Number of countries: XX", className="card-text"),
                    html.P("Number of sports: XX", className="card-text"),
                ])
            ], style={"width": "18rem"})
        ], width=4)
    ])
], fluid=True)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5050)