from dash import register_page, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils import load_data

register_page(__name__, path='/reuse/trends', name='Reuse Trends')

def get_area_options():
    """获取所有区域选项"""
    df = load_data()
    options = [
        {'label': '--- Region Groups ---', 'value': 'group_header', 'disabled': True},
        {'label': 'All Areas', 'value': 'all'},
        {'label': 'London (All)', 'value': 'london_all'},
        {'label': 'Non-London', 'value': 'non_london'},
        {'label': '--- London Boroughs ---', 'value': 'london_header', 'disabled': True}
    ]
    
    london_areas = sorted(df[df['London_Status'].isin(['Core London', 'Outer London'])]['Area'].unique())
    for area in london_areas:
        options.append({'label': f"  • {area}", 'value': area})
    
    return options

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Reuse Trends Analysis", className="text-center mb-4")
        ])
    ]),
    
    # 控制面板
    dbc.Row([
        dbc.Col([
            html.Label("Select Areas:", className="mb-2"),
            dcc.Dropdown(
                id='reuse-area-selector',  # 修改ID
                options=get_area_options(),
                value=['london_all'],
                multi=True,
                className="mb-3"
            ),
            html.Label("Select Time Range:", className="mb-2"),
            dcc.RangeSlider(
                id='reuse-year-selector',  # 修改ID
                min=2003,
                max=2022,
                value=[2003, 2022],
                marks={year: str(year) for year in range(2003, 2023, 2)},
                tooltip={'placement': 'bottom', 'always_visible': True}
            ),
            html.Label("Chart Type:", className="mt-3 mb-2"),
            dbc.RadioItems(
                id='reuse-chart-type',  # 修改ID
                options=[
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Area Chart', 'value': 'area'}
                ],
                value='line',
                inline=True,
                className="mb-3"
            )
        ], width=12)
    ], className="mb-4"),
    
    # 趋势图
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Reuse Rate Trends"),
                dbc.CardBody([
                    dcc.Graph(id='reuse-trend-chart')  # 修改ID
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # 统计信息
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Trend Statistics"),
                dbc.CardBody(id='reuse-trend-stats')  # 修改ID
            ])
        ], width=12)
    ])
], fluid=True)

@callback(
    [Output('reuse-trend-chart', 'figure'),
     Output('reuse-trend-stats', 'children')],
    [Input('reuse-area-selector', 'value'),
     Input('reuse-year-selector', 'value'),
     Input('reuse-chart-type', 'value')]
)
def update_reuse_trend_analysis(selected_areas, year_range, chart_type):
    df = load_data()
    
    # 过滤时间范围
    df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    
    # 处理区域选择
    if 'all' in selected_areas:
        filtered_df = df
    else:
        mask = pd.Series(False, index=df.index)
        for area in selected_areas:
            if area == 'london_all':
                mask |= df['London_Status'].isin(['Core London', 'Outer London'])
            elif area == 'non_london':
                mask |= df['London_Status'] == 'Non-London'
            else:
                mask |= df['Area'] == area
        filtered_df = df[mask]
    
    # 创建图表
    if chart_type == 'line':
        fig = px.line(filtered_df, 
                     x='Year', 
                     y='Reuse_Rates',  # 修改为Reuse数据
                     color='Area',
                     title='Reuse Rate Trends')
    elif chart_type == 'bar':
        fig = px.bar(filtered_df,
                    x='Year',
                    y='Reuse_Rates',  # 修改为Reuse数据
                    color='Area',
                    title='Reuse Rate Trends',
                    barmode='group')
    else:  # area chart
        fig = px.area(filtered_df,
                     x='Year',
                     y='Reuse_Rates',  # 修改为Reuse数据
                     color='Area',
                     title='Reuse Rate Trends')
    
    # 优化图表布局
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Reuse Rate (%)",
        legend_title="Area",
        hovermode='x unified',
        template='plotly_white'
    )
    
    # 计算统计信息
    stats = []
    for area in filtered_df['Area'].unique():
        area_data = filtered_df[filtered_df['Area'] == area]
        start_rate = area_data[area_data['Year'] == year_range[0]]['Reuse_Rates'].iloc[0]
        end_rate = area_data[area_data['Year'] == year_range[1]]['Reuse_Rates'].iloc[0]
        change = end_rate - start_rate
        
        stats.append(html.Div([
            html.H5(area),
            html.P([
                f"Start Rate: {start_rate:.1f}%",
                html.Br(),
                f"End Rate: {end_rate:.1f}%",
                html.Br(),
                f"Change: {change:+.1f}%",
            ])
        ], className="mb-3"))
    
    return fig, html.Div(stats) 