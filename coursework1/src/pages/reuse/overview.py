from dash import register_page, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import sys
from pathlib import Path

# 添加父目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.recycling_figures import recycling_line_chart
from utils import load_data

register_page(__name__, path='/reuse', name='Reuse Overview')

# 使用相同的伦敦坐标数据
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
    dbc.Row([
        dbc.Col([
            html.H1("London Reuse Overview", className="text-center mb-4")
        ])
    ]),
    
    # 时间范围选择器
    dbc.Row([
        dbc.Col([
            html.Label('Select Time Range:', className='mb-2'),
            dcc.RangeSlider(
                id='reuse-year-selector',
                min=2003,
                max=2022,
                value=[2003, 2022],
                marks={year: str(year) for year in range(2003, 2023, 2)},
                tooltip={'placement': 'bottom', 'always_visible': True}
            )
        ], width=12)
    ], className='mb-4'),
    
    # 主要图表区域
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("London Reuse Map"),
                dbc.CardBody([
                    dcc.Graph(id='reuse-map')
                ])
            ])
        ], width=12)
    ], className='mb-4'),
    
    # 统计卡片
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Core London"),
                dbc.CardBody(id='reuse-core-stats')
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Outer London"),
                dbc.CardBody(id='reuse-outer-stats')
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Non-London"),
                dbc.CardBody(id='reuse-non-stats')
            ])
        ], width=4)
    ])
], fluid=True)

@callback(
    [Output('reuse-core-stats', 'children'),
     Output('reuse-outer-stats', 'children'),
     Output('reuse-non-stats', 'children'),
     Output('reuse-map', 'figure')],
    [Input('reuse-year-selector', 'value')]
)
def update_reuse_overview(year_range):
    df = load_data()
    selected_year = year_range[1]
    df_latest = df[df['Year'] == selected_year]
    
    # 计算各区域统计数据
    def get_stats(status):
        data = df_latest[df_latest['London_Status'] == status]
        return {
            'avg': data['Reuse_Rates'].mean(),
            'max': data['Reuse_Rates'].max(),
            'min': data['Reuse_Rates'].min(),
            'count': len(data)
        }
    
    core_stats = get_stats('Core London')
    outer_stats = get_stats('Outer London')
    non_london_stats = get_stats('Non-London')
    
    # 创建统计卡片内容
    def create_stats_card(stats):
        return html.Div([
            html.H3(f"{stats['avg']:.1f}%", className="text-primary"),
            html.P(f"Highest: {stats['max']:.1f}%"),
            html.P(f"Lowest: {stats['min']:.1f}%"),
            html.P(f"Number of Areas: {stats['count']}")
        ])
    
    # 创建地图
    map_fig = go.Figure()
    
    # 为每个区域添加标记
    for area in df_latest['Area'].unique():
        if area in LONDON_COORDS:  # 只显示有坐标的区域
            area_data = df_latest[df_latest['Area'] == area].iloc[0]
            lon, lat = LONDON_COORDS[area]
            
            map_fig.add_trace(go.Scattergeo(
                lon=[lon],
                lat=[lat],
                text=f"{area}<br>Reuse Rate: {area_data['Reuse_Rates']:.1f}%",
                mode='markers',
                marker=dict(
                    size=10,
                    color=area_data['Reuse_Rates'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar_title="Reuse Rate (%)"
                ),
                name=area
            ))
    
    map_fig.update_layout(
        title=f"London Reuse Rates ({selected_year})",
        geo=dict(
            scope='europe',
            center=dict(lon=-0.1276, lat=51.5072),  # 伦敦中心
            projection_scale=50000,
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showcoastlines=True,
            coastlinecolor='rgb(80, 80, 80)',
            showframe=False
        ),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    return (
        create_stats_card(core_stats),
        create_stats_card(outer_stats),
        create_stats_card(non_london_stats),
        map_fig
    ) 