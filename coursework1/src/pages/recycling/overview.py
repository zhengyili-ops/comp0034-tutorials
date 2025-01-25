from dash import register_page, html, dcc, callback, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash
from pathlib import Path
import sys
import pandas as pd
from datetime import date

# 添加父目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils import load_data

# 注册页面
register_page(__name__, path='/recycling', name='Recycling Overview')

# 伦敦区域坐标数据
LONDON_COORDS = {
    'Camden': [-0.1426, 51.5290],
    'City of London': [-0.0923, 51.5155],
    'Hackney': [-0.0575, 51.5450],
    'Hammersmith and Fulham': [-0.2277, 51.4927],
    'Haringey': [-0.1088, 51.5906],
    'Islington': [-0.1069, 51.5416],
    'Kensington and Chelsea': [-0.1919, 51.5017],
    'Lambeth': [-0.1144, 51.4571],
    'Lewisham': [-0.0209, 51.4415],
    'Newham': [0.0333, 51.5255],
    'Southwark': [-0.0932, 51.4733],
    'Tower Hamlets': [-0.0198, 51.5150],
    'Wandsworth': [-0.1927, 51.4571],
    'Westminster': [-0.1357, 51.4975],
    'Barking and Dagenham': [0.1313, 51.5463],
    'Barnet': [-0.2047, 51.6252],
    'Bexley': [0.1386, 51.4549],
    'Brent': [-0.2714, 51.5673],
    'Bromley': [0.0549, 51.4039],
    'Croydon': [-0.0982, 51.3714],
    'Ealing': [-0.3089, 51.5130],
    'Enfield': [-0.0826, 51.6538],
    'Greenwich': [0.0549, 51.4892],
    'Harrow': [-0.3350, 51.5890],
    'Havering': [0.2324, 51.5812],
    'Hillingdon': [-0.4476, 51.5441],
    'Hounslow': [-0.3669, 51.4746],
    'Kingston upon Thames': [-0.3031, 51.3925],
    'Merton': [-0.1977, 51.4095],
    'Redbridge': [0.0738, 51.5590],
    'Richmond upon Thames': [-0.3022, 51.4479],
    'Sutton': [-0.1695, 51.3618],
    'Waltham Forest': [-0.0134, 51.5908]
}

layout = dbc.Container([
    # 标题行
    dbc.Row([
        dbc.Col([
            html.H1("London Recycling Overview", className="text-center mb-4"),
            html.P("Explore recycling trends and patterns across London boroughs", 
                   className="text-center mb-4")
        ])
    ]),
    
    # 年份选择器
    dbc.Row([
        dbc.Col([
            html.Label([
                "Select Year: ",
                html.Small(id="selected-year-display", className="text-muted")
            ], className="mb-2"),
            dcc.RangeSlider(
                id='year-range-slider',
                min=2003,
                max=2022,
                value=[2022, 2022],  # 默认选择最新年份
                marks={
                    year: {
                        'label': str(year),
                        'style': {'color': '#666'}
                    }
                    for year in range(2003, 2023)
                },
                step=None,
                tooltip={"placement": "top", "always_visible": True},
                className="px-2"
            )
        ], width=12),
    ], className="mb-4"),
    
    # 主要统计卡片
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Core London"),
                dbc.CardBody(id="core-london-stats")
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Outer London"),
                dbc.CardBody(id="outer-london-stats")
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Non-London"),
                dbc.CardBody(id="non-london-stats")
            ])
        ], width=4),
    ], className="mb-4"),
    
    # 地图和趋势图
    dbc.Row([
        # 地图
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Recycling Rates Map"),
                dbc.CardBody([
                    dcc.Graph(id="london-map")
                ])
            ])
        ], width=6),
        # 趋势图
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Overall Trends"),
                dbc.CardBody([
                    dcc.Graph(id="trend-chart")
                ])
            ])
        ], width=6),
    ], className="mb-4"),
    
    # 排名表格
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col(html.H5("Top Performing Areas", className="mb-0"), width="auto"),
                                dbc.Col(
                                    html.Small(
                                        id="ranking-period-display",
                                        className="text-muted",
                                    ),
                                    width="auto",
                                    className="d-flex align-items-center"
                                ),
                            ], className="align-items-center"),
                        ], width=12),  # 改为12，占据整行
                    ], className="g-0 align-items-center"),
                ], className="py-2"),
                dbc.CardBody([
                    html.Div(id="rankings-table", className="p-0")
                ])
            ], className="shadow-sm")
        ], width=12)
    ])
], fluid=True)

@callback(
    [Output("core-london-stats", "children"),
     Output("outer-london-stats", "children"),
     Output("non-london-stats", "children"),
     Output("london-map", "figure"),
     Output("trend-chart", "figure")],
    [Input("year-range-slider", "value")]
)
def update_overview(year_range):
    df = load_data()
    
    # 1. 计算统计信息
    def get_stats(status):
        if year_range[0] == year_range[1]:
            # 单年份模式
            data = df[(df['Year'] == year_range[0]) & (df['London_Status'] == status)]
        else:
            # 时间范围模式
            data = df[
                (df['Year'].between(year_range[0], year_range[1])) & 
                (df['London_Status'] == status)
            ]
        return {
            'avg': data['Recycling_Rates'].mean(),
            'max': data['Recycling_Rates'].max(),
            'min': data['Recycling_Rates'].min()
        }
    
    core_stats = get_stats('Core London')
    outer_stats = get_stats('Outer London')
    non_london_stats = get_stats('Non-London')
    
    # 2. 创建地图 - 使用范围的最后一年或单一年份
    map_year = year_range[1] if year_range[0] != year_range[1] else year_range[0]
    map_fig = create_map(df, map_year)
    
    # 3. 创建趋势图
    trend_fig = create_trend_chart(df)
    
    return (
        create_stats_card(core_stats),
        create_stats_card(outer_stats),
        create_stats_card(non_london_stats),
        map_fig,
        trend_fig
    )

@callback(
    [Output("rankings-table", "children"),
     Output("ranking-period-display", "children")],
    [Input("year-range-slider", "value")]
)
def update_rankings(year_range):
    df = load_data()
    
    if year_range[0] == year_range[1]:
        # 单年份模式
        table = create_rankings_table(df, year_range[0], 'year')
        period_display = f"({year_range[0]})"
    else:
        # 时间范围模式
        table = create_rankings_table(df, year_range, 'range')
        period_display = f"(Average {year_range[0]}-{year_range[1]})"
    
    return table, period_display

@callback(
    Output("selected-year-display", "children"),
    [Input("year-range-slider", "value")]
)
def update_year_display(value):
    return f"({value[0]}-{value[1]})"

def create_map(df, year):
    # 创建地图可视化
    map_data = df[df['Year'] == year]
    
    fig = go.Figure()
    
    for area in map_data['Area'].unique():
        if area in LONDON_COORDS:
            area_data = map_data[map_data['Area'] == area].iloc[0]
            lon, lat = LONDON_COORDS[area]
            
            fig.add_trace(go.Scattergeo(
                lon=[lon],
                lat=[lat],
                text=f"{area}<br>Recycling Rate: {area_data['Recycling_Rates']:.1f}%",
                mode='markers',
                marker=dict(
                    size=10,
                    color=area_data['Recycling_Rates'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar_title="Recycling Rate (%)"
                ),
                name=area
            ))
    
    fig.update_layout(
        title=f"London Recycling Rates ({year})",
        geo=dict(
            scope='europe',
            center=dict(lon=-0.1276, lat=51.5072),
            projection_scale=50000,
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showcoastlines=True,
            coastlinecolor='rgb(80, 80, 80)',
            showframe=False
        ),
        height=400
    )
    
    return fig

def create_trend_chart(df):
    # 创建趋势图
    trend_data = df.groupby(['Year', 'London_Status'])['Recycling_Rates'].mean().reset_index()
    
    fig = px.line(
        trend_data,
        x='Year',
        y='Recycling_Rates',
        color='London_Status',
        title='Recycling Rates Trends by Region Type',
        labels={'Recycling_Rates': 'Average Recycling Rate (%)',
                'Year': 'Year',
                'London_Status': 'Region Type'}
    )
    
    fig.update_layout(height=400)
    return fig

def create_rankings_table(df, year, ranking_type='year'):
    """创建排名表格，支持单年或时间范围"""
    if ranking_type == 'year':
        rankings_data = (df[df['Year'] == year]
                        .sort_values('Recycling_Rates', ascending=False)
                        .reset_index(drop=True))
    else:
        # 时间范围模式
        year_range = year
        rankings_data = (df[df['Year'].between(year_range[0], year_range[1])]
                        .groupby(['Area', 'London_Status', 'Postcode'])['Recycling_Rates']
                        .mean()
                        .reset_index()
                        .sort_values('Recycling_Rates', ascending=False)
                        .reset_index(drop=True))
    
    # 创建表格
    table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Rank", style={'width': '60px'}),
                html.Th("Area", style={'width': '25%'}),
                html.Th("Postcode", style={'width': '15%'}),
                html.Th("Region Type", style={'width': '25%'}),
                html.Th("Recycling Rate", style={'width': '20%', 'text-align': 'right'})
            ], className="table-light")
        ]),
        html.Tbody([
            html.Tr([
                html.Td(
                    html.Span(f"#{i+1}", 
                             className="badge bg-primary rounded-pill",
                             style={'min-width': '35px'}),
                    className="align-middle"
                ),
                html.Td(row['Area'], className="align-middle"),
                html.Td(
                    html.Span(
                        row['Postcode'] if pd.notna(row['Postcode']) else 'Non',
                        className="badge bg-light text-dark"
                    ),
                    className="align-middle"
                ),
                html.Td(
                    html.Span(
                        row['London_Status'],
                        className=f"badge {'bg-success' if 'London' in row['London_Status'] else 'bg-secondary'}"
                    ),
                    className="align-middle"
                ),
                html.Td(
                    html.Strong(f"{row['Recycling_Rates']:.1f}%"),
                    className="align-middle text-end"
                )
            ], className="align-middle") 
            for i, row in rankings_data.head(10).iterrows()
        ])
    ], bordered=False, hover=True, responsive=True,
       className="table align-middle mb-0")

    return table

def create_stats_card(stats):
    return html.Div([
        html.H3(f"{stats['avg']:.1f}%", className="text-primary"),
        html.P([
            html.Span("Highest: ", className="fw-bold"),
            f"{stats['max']:.1f}%"
        ]),
        html.P([
            html.Span("Lowest: ", className="fw-bold"),
            f"{stats['min']:.1f}%"
        ])
    ])


