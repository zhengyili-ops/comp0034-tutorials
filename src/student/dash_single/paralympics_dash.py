from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from figure import line_chart, bar_gender, scatter_geo  # Import from figure.py instead of figures
from dash.dependencies import Input, Output

# Define meta tags and stylesheets
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Create the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Create the line chart
line_fig = line_chart("sports")
bar_fig = bar_gender("Summer")  # 确保是 "Summer" 而不是 "summer"
map_fig = scatter_geo()  # 创建地图

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
            dcc.Graph(id="line-chart", figure=line_fig)
        ], width=12)
    ]),
    
    # Row 4: Bar chart
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="bar-chart", figure=bar_fig)
        ], width=12)
    ]),
    
    # Row 5: Map and Card
    dbc.Row([
        # Column 1: Map - 替换原来的静态图片
        dbc.Col([
            dcc.Graph(id="geo-map", figure=map_fig)  # 使用交互式地图
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

# 在layout定义后添加回调
@app.callback(
    Output("line-chart", "figure"),
    [Input("dropdown-input", "value"),
     Input("checklist-input", "value")]
)
def update_charts(selected_feature, selected_types):
    """Update the line chart based on user selection"""
    return line_chart(selected_feature, selected_types)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5050)