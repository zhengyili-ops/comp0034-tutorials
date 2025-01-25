# Page with the line chart and bar chart and their selectors
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, register_page, dash_table
from dash.dependencies import Input, Output
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from figure import line_chart, bar_gender, create_bubble_chart, create_data_table

# register the page in the app
register_page(__name__, path='/charts', name='Charts', title='Charts')

layout = dbc.Container([
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
    
    # Row 3: Line chart
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="line-chart")
        ], width=12)
    ]),
    
    # Row 4: Bar chart
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="bar-chart")
        ], width=12)
    ]),
    
    # Row 5: Bubble Chart
    dbc.Row([
        dbc.Col([
            html.H2("Paralympics Growth Analysis", className="mt-4"),
            dcc.Graph(figure=create_bubble_chart())
        ], width=12)
    ]),
    
    # Row 6: Data Table
    dbc.Row([
        dbc.Col([
            html.H2("Paralympic Games Historical Data", className="mt-4"),
            create_data_table()
        ], width=12)
    ])
], fluid=True)

@callback(
    Output("line-chart", "figure"),
    [Input("dropdown-input", "value"),
     Input("checklist-input", "value")]
)
def update_line_chart(selected_feature, selected_types):
    return line_chart(selected_feature, selected_types)

@callback(
    Output("bar-chart", "figure"),
    [Input("checklist-input", "value")]
)
def update_bar_chart(selected_type):
    return bar_gender(selected_type[0] if selected_type else "summer")
