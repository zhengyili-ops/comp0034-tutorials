from dash import register_page, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import json
import dash

# 添加父目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils import load_data

# 首先定义辅助函数
def get_year_range():
    df = load_data()
    min_year = df['Year'].min()
    max_year = df['Year'].max()
    return min_year, max_year

# 然后定义常量
LONDON_COORDS = {
    # --- Core London ---
    "City of London":         [-0.1221, 51.53562],
    "Westminster":            [-0.16926, 51.52749],
    "Camden":                 [-0.17192, 51.56711],
    "Islington":              [-0.13291, 51.57529],
    "Hackney":                [-0.07576, 51.57505],
    "Tower Hamlets":          [-0.04437, 51.54313],
    "Southwark":             [-0.10046, 51.49390],
    "Lambeth":               [-0.12940, 51.48005],

    # --- Outer London ---
    "Haringey":                [-0.13291, 51.61152],
    "Enfield":                [-0.12489, 51.67152],
    "Barnet":                 [-0.21553, 51.66092],
    "Harrow":                 [-0.36161, 51.59526],
    "Brent":                  [-0.28168, 51.57843],
    "Ealing":                 [-0.33888, 51.53631],
    "Hounslow":               [-0.35603, 51.48485],
    "Richmond upon Thames":   [-0.35603, 51.44764],
    "Kingston upon Thames":   [-0.29641, 51.40070],
    "Merton":                 [-0.20171, 51.43062],
    "Sutton":                 [-0.19692, 51.36332],
    "Croydon":                [-0.09333, 51.37464],
    "Bromley":                [ 0.01518, 51.40574],
    "Bexley":                 [ 0.12118, 51.48156],
    "Greenwich":              [ 0.04000, 51.49097],
    "Lewisham":               [-0.04682, 51.46522],
    "Wandsworth":             [-0.19169, 51.47753],
    "Hammersmith and Fulham": [-0.23862, 51.51681],
    "Kensington and Chelsea": [-0.19637, 51.51484],
    "Waltham Forest":         [-0.04437, 51.61549],
    "Redbridge":              [ 0.05332, 51.61549],
    "Havering":               [ 0.19948, 51.58010],
    "Barking and Dagenham":   [ 0.09108, 51.55648],
    "Newham":                 [ 0.01518, 51.55000],
    "Hillingdon":             [-0.46108, 51.54421],
}

# 添加邮编数据
LONDON_POSTCODES = {
    # Core London
    "City of London": "EC",
    "Westminster": "SW1",
    "Camden": "NW1",
    "Islington": "N1",
    "Hackney": "E8",
    "Tower Hamlets": "E1",
    "Southwark": "SE1",
    "Lambeth": "SE11",
    
    # Outer London
    "Haringey": "N",
    "Enfield": "EN",
    "Barnet": "N",
    "Harrow": "HA",
    "Brent": "NW",
    "Ealing": "W",
    "Hounslow": "TW",
    "Richmond upon Thames": "TW",
    "Kingston upon Thames": "KT",
    "Merton": "SW",
    "Sutton": "SM",
    "Croydon": "CR",
    "Bromley": "BR",
    "Bexley": "DA",
    "Greenwich": "SE",
    "Lewisham": "SE",
    "Wandsworth": "SW",
    "Hammersmith and Fulham": "W",
    "Kensington and Chelsea": "SW",
    "Waltham Forest": "E",
    "Redbridge": "IG",
    "Havering": "RM",
    "Barking and Dagenham": "RM",
    "Newham": "E",
    "Hillingdon": "UB"
}

# 修改教育程度数据生成方式
EDUCATION_DATA = {
    area: {
        'Higher Education': round(30 + (45 - 30) * np.random.random(), 1),  # 30-45%
        'A-Level or Equivalent': round(25 + (35 - 25) * np.random.random(), 1),  # 25-35%
        'GCSE or Equivalent': round(20 + (25 - 20) * np.random.random(), 1),  # 20-25%
        'Other Qualifications': round(5 + (10 - 5) * np.random.random(), 1),  # 5-10%
        'No Qualifications': round(5 + (10 - 5) * np.random.random(), 1)  # 5-10%
    }
    for area in LONDON_COORDS.keys()
}

# 注册页面
register_page(__name__, path='/recycling/area', name='Area Analysis')

# 获取年份范围
min_year, max_year = get_year_range()

layout = dbc.Container([
    # 标题行
    dbc.Row([
        dbc.Col([
            html.H1("Area Analysis", className="text-center mb-4"),
            html.P("Explore recycling patterns across London boroughs", 
                   className="text-center mb-4")
        ])
    ]),
    
    # 控制面板
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Select Time Period:", className="mb-2"),
                    dcc.RangeSlider(
                        id='year-range-selector',
                        min=min_year,
                        max=max_year,
                        value=[max_year, max_year],  # 默认选择最新年份
                        marks={str(year): str(year) for year in range(min_year, max_year + 1)},
                        step=1,
                        className="mb-4",
                        allowCross=True,  # 允许两个滑块交叉，以实现单年份选择
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # 第一行：地图和统计信息
    dbc.Row([
        # 地图部分
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("London Recycling Map"),
                dbc.CardBody([
                    dcc.Graph(
                        id="area-analysis-map",
                        style={
                            'height': '600px',  # 固定高度
                            'width': '100%',    # 宽度适应容器
                            'max-height': '600px',  # 最大高度限制
                            'overflow': 'hidden'  # 超出部分隐藏
                        }
                    )
                ], className="p-0")
            ])
        ], width=9),
        
        # 右侧统计信息保持不变
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Area Statistics"),
                dbc.CardBody([
                    html.Div(id="area-stats")
                ])
            ], className="mb-3"),
            
            dbc.Card([
                dbc.CardHeader("Area Trend"),
                dbc.CardBody([
                    dcc.Graph(
                        id="area-trend-chart",
                        style={'height': '300px'}
                    )
                ])
            ])
        ], width=3)
    ], className="mb-4"),
    
    # 新增第二行：额外分析图表
    dbc.Row([
        # 回收率分布图
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Recycling Rate Distribution"),
                dbc.CardBody([
                    dcc.Graph(id="recycling-distribution")
                ])
            ])
        ], width=6),
        
        # 人口密度与回收率关系图
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Population Density vs Recycling Rate"),
                dbc.CardBody([
                    dcc.Graph(id="density-recycling-correlation")
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # 新增第三行：关键指标
    dbc.Row([
        # 平均回收率
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="avg-recycling-rate", className="text-center"),
                    html.P("Average Recycling Rate", className="text-center text-muted")
                ])
            ])
        ], width=3),
        
        # 最佳表现区域
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="top-performer", className="text-center"),
                    html.P("Top Performing Borough", className="text-center text-muted")
                ])
            ])
        ], width=3),
        
        # 同比变化
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="year-on-year", className="text-center"),
                    html.P("Year-on-Year Change", className="text-center text-muted")
                ])
            ])
        ], width=3),
        
        # 回收率差距
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="recycling-gap", className="text-center"),
                    html.P("Core-Outer Gap", className="text-center text-muted")
                ])
            ])
        ], width=3)
    ]),
    
    # 添加新的行用于教育程度分析
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Education Level Distribution"),
                dbc.CardBody([
                    dcc.Graph(id="education-distribution")
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Education Level vs Recycling Rate"),
                dbc.CardBody([
                    dcc.Graph(id="education-recycling-correlation")
                ])
            ])
        ], width=6)
    ], className="mb-4"),
])

# 合并回调函数
@callback(
    [Output("area-analysis-map", "figure"),
     Output("area-stats", "children"),
     Output("area-trend-chart", "figure"),
     Output("recycling-distribution", "figure"),
     Output("density-recycling-correlation", "figure"),
     Output("avg-recycling-rate", "children"),
     Output("top-performer", "children"),
     Output("year-on-year", "children"),
     Output("recycling-gap", "children"),
     Output("education-distribution", "figure"),
     Output("education-recycling-correlation", "figure")],
    [Input("year-range-selector", "value"),
     Input("area-analysis-map", "clickData")]
)
def update_all_components(year_range, click_data):
    df = load_data()
    
    # 检查是否是单一年份
    is_single_year = year_range[0] == year_range[1]
    selected_year = year_range[0]  # 如果是单一年份，使用任一值都可以
    
    if is_single_year:
        # 单年份数据处理
        year_data = df[df['Year'] == selected_year]
        title_text = f"London Recycling Rates in {selected_year}"
    else:
        # 时间范围数据处理
        year_data = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
        title_text = f"London Recycling Rates ({year_range[0]}-{year_range[1]})"
    
    # 1. 创建地图
    map_fig = go.Figure()

    # 添加背景地图图片
    map_fig.add_layout_image(
        dict(
            source="/assets/london_map.png",
            xref="x",
            yref="y",
            x=-0.52,
            y=51.72,
            sizex=0.82,
            sizey=0.42,
            sizing="contain",
            opacity=1,
            layer="below"
        )
    )
    
    # 为每个区域添加标记点
    for area in LONDON_COORDS:
        area_data = year_data[year_data['Area'] == area]
        if not area_data.empty:
            recycling_rate = area_data.iloc[0]['Recycling_Rates']
            london_status = area_data.iloc[0]['London_Status']
            
            # 根据区域类型设置颜色
            color = '#4e79a7' if london_status == 'Core London' else '#f28e2b'
            
            map_fig.add_trace(go.Scatter(
                x=[LONDON_COORDS[area][0]],
                y=[LONDON_COORDS[area][1]],
                mode='markers',
                marker=dict(
                    size=15,
                    color=color,
                    line=dict(
                        color='white',
                        width=1.5
                    )
                ),
                name=london_status,
                text=f"<b>{area}</b><br>Recycling Rate: {recycling_rate:.1f}%<br>{london_status}",
                customdata=[area],  # 添加区域名称作为自定义数据
                hoverinfo='text',
                hovertemplate="%{text}<extra></extra>",
                showlegend=london_status not in [t.name for t in map_fig.data]
            ))
    
    # 更新地图布局
    map_fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.98,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        xaxis=dict(
            range=[-0.52, 0.30],
            showgrid=False,
            zeroline=False,
            visible=False,
            fixedrange=True,  # 锁定X轴
            constrain='domain'  # 确保比例固定
        ),
        yaxis=dict(
            range=[51.30, 51.72],
            showgrid=False,
            zeroline=False,
            visible=False,
            fixedrange=True,  # 锁定Y轴
            scaleanchor="x",
            scaleratio=1.2,
            constrain='domain'  # 确保比例固定
        ),
        height=600,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        dragmode=False,  # 禁用拖动
        hovermode='closest',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1,
            itemsizing='constant'
        ),
        modebar=dict(
            remove=[
                "zoom",
                "pan",
                "select",
                "lasso",
                "zoomIn",
                "zoomOut",
                "autoScale",
                "resetScale",
                "toImage",
                "resetViews",
                "toggleSpikelines"
            ],
            orientation='v'
        ),
        clickmode='event'  # 只允许点击事件
    )
    
    # 2. 创建区域统计信息
    stats_content = html.Div("Click an area to see details")
    if click_data:
        try:
            point_data = click_data['points'][0]
            area_name = point_data['customdata'] if 'customdata' in point_data else point_data['text'].split('<br>')[0].replace('<b>', '').replace('</b>', '')
            
            area_data = df[df['Area'] == area_name]
            
            if not area_data.empty:
                # 获取选定时间范围内的数据
                period_data = area_data[
                    (area_data['Year'] >= year_range[0]) & 
                    (area_data['Year'] <= year_range[1])
                ]
                
                # 计算变化
                if len(period_data) > 1:  # 如果有多个年份的数据
                    start_rate = period_data[period_data['Year'] == year_range[0]]['Recycling_Rates'].values[0]
                    end_rate = period_data[period_data['Year'] == year_range[1]]['Recycling_Rates'].values[0]
                    change = end_rate - start_rate
                    # 根据变化值设置颜色
                    change_color = "red" if change > 0 else "green" if change < 0 else "black"
                    change_text = html.Span(
                        f"{change:+.1f}%",
                        style={'color': change_color, 'font-weight': 'bold'}
                    )
                else:
                    change_text = "N/A"
                
                # 获取最新年份的数据用于显示当前回收率
                current_data = period_data[period_data['Year'] == year_range[1]].iloc[0]
                
                stats_content = html.Div([
                    html.H4(area_name, className="mb-3"),
                    html.Div([
                        html.P([
                            html.Strong("Postcode: "),
                            LONDON_POSTCODES.get(area_name, "N/A")
                        ]),
                        html.P([
                            html.Strong("Region Type: "),
                            current_data['London_Status']
                        ]),
                        html.P([
                            html.Strong("Recycling Rate: "),
                            f"{current_data['Recycling_Rates']:.1f}%"
                        ]),
                        html.P([
                            html.Strong("Change over period: "),
                            change_text
                        ])
                    ], className="area-stats")
                ])
        except Exception as e:
            print(f"Error processing click data: {e}")
            stats_content = html.Div("Error loading area details")

    # 3. 创建趋势图表，添加选定时间范围的高亮
    trend_fig = go.Figure()
    if click_data:
        try:
            point_data = click_data['points'][0]
            area_name = point_data['customdata'] if 'customdata' in point_data else point_data['text'].split('<br>')[0].replace('<b>', '').replace('</b>', '')
            area_trend = df[df['Area'] == area_name]
            
            if not area_trend.empty:
                # 添加灰色背景来显示选定的时间范围
                trend_fig.add_vrect(
                    x0=year_range[0],
                    x1=year_range[1],
                    fillcolor="rgba(128, 128, 128, 0.2)",
                    layer="below",
                    line_width=0,
                    annotation_text="Selected Period" if year_range[0] != year_range[1] else "Selected Year",
                    annotation_position="top left"
                )

                # 添加趋势线
                trend_fig.add_trace(go.Scatter(
                    x=area_trend['Year'],
                    y=area_trend['Recycling_Rates'],
                    mode='lines+markers',
                    name=area_name,
                    line=dict(color='#4e79a7' if area_trend.iloc[0]['London_Status'] == 'Core London' else '#f28e2b')
                ))
                
                trend_fig.update_layout(
                    title=f"Recycling Rate Trend for {area_name}",
                    xaxis_title="Year",
                    yaxis_title="Recycling Rate (%)",
                    height=300,
                    margin=dict(l=40, r=20, t=40, b=30),
                    hovermode='x unified',
                    yaxis=dict(range=[0, max(area_trend['Recycling_Rates']) * 1.1]),
                    showlegend=False
                )
        except Exception as e:
            print(f"Error creating trend chart: {e}")
            trend_fig.update_layout(
                title="Error loading trend data",
                height=300,
                margin=dict(l=40, r=20, t=40, b=30)
            )
    
    # 创建额外的图表和指标
    # 1. 创建回收率分布箱线图
    dist_fig = go.Figure()
    
    # 为Core London和Outer London分别创建箱线图
    for status, color in [('Core London', '#4e79a7'), ('Outer London', '#f28e2b')]:
        status_data = year_data[year_data['London_Status'] == status]
        dist_fig.add_trace(go.Box(
            y=status_data['Recycling_Rates'],
            name=status,
            boxpoints='all',  # 显示所有数据点
            jitter=0.3,  # 数据点的随机偏移量
            pointpos=-1.8,  # 数据点的位置
            marker_color=color,  # 设置颜色
            line=dict(color=color),  # 箱线的颜色
            marker=dict(
                size=8,
                opacity=0.7
            ),
            hovertemplate="<b>%{text}</b><br>" +
                         "Recycling Rate: %{y:.1f}%<br>" +
                         "<extra></extra>",
            text=status_data['Area'],  # 添加区域名称用于悬停显示
            width=0.4  # 减小箱线图的宽度
        ))

    dist_fig.update_layout(
        title=f"Recycling Rate Distribution by Region Type ({selected_year})",
        yaxis_title="Recycling Rate (%)",
        showlegend=True,
        height=400,
        plot_bgcolor='rgba(240,240,240,0.3)',
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.8)',
            zeroline=False
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor='rgba(255,255,255,0.8)'
        ),
        boxmode='group',
        boxgap=0,       # 将间距设为0
        boxgroupgap=0,  # 将组间距设为0
        bargap=0.15     # 控制整体分组的间距
    )
    
    # 2. 创建人口密度与回收率散点图
    corr_fig = go.Figure()
    for status in ['Core London', 'Outer London']:
        status_data = year_data[year_data['London_Status'] == status]
        corr_fig.add_trace(go.Scatter(
            x=status_data['Population_Density'],
            y=status_data['Recycling_Rates'],
            mode='markers',
            name=status,
            text=status_data['Area'],
            marker=dict(size=10),
            hovertemplate="<b>%{text}</b><br>" +
                        "Population Density: %{x:.0f}<br>" +
                        "Recycling Rate: %{y:.1f}%<br>" +
                        "<extra></extra>"
        ))
    corr_fig.update_layout(
        title=f"Population Density vs Recycling Rate ({selected_year})",
        xaxis_title="Population Density (per km²)",
        yaxis_title="Recycling Rate (%)",
        height=400
    )
    
    # 3. 计算关键指标
    avg_rate = f"{year_data['Recycling_Rates'].mean():.1f}%"
    top_area = year_data.loc[year_data['Recycling_Rates'].idxmax()]
    top_performer = f"{top_area['Area']} ({top_area['Recycling_Rates']:.1f}%)"
    
    # 计算同比变化
    prev_year = df[df['Year'] == (selected_year - 1)]
    if not prev_year.empty:
        yoy_change = year_data['Recycling_Rates'].mean() - prev_year['Recycling_Rates'].mean()
        yoy_text = f"{yoy_change:+.1f}%"
    else:
        yoy_text = "N/A"
    
    # 计算Core和Outer London的回收率差距
    core_rate = year_data[year_data['London_Status'] == 'Core London']['Recycling_Rates'].mean()
    outer_rate = year_data[year_data['London_Status'] == 'Outer London']['Recycling_Rates'].mean()
    gap = core_rate - outer_rate
    gap_text = f"{gap:+.1f}%"

    # 创建教育程度分布柱状图
    edu_dist_fig = go.Figure()
    if click_data:
        point_data = click_data['points'][0]
        area_name = point_data['customdata'] if 'customdata' in point_data else point_data['text'].split('<br>')[0].replace('<b>', '').replace('</b>', '')
        
        if area_name in EDUCATION_DATA:
            edu_data = EDUCATION_DATA[area_name]
            education_levels = ['Higher Education', 'A-Level or Equivalent', 'GCSE or Equivalent', 
                              'Other Qualifications', 'No Qualifications']
            colors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f']
            
            # 生成年度数据
            years = list(range(year_range[0], year_range[1] + 1))
            
            # 为每个教育水平创建柱状图
            for level, color in zip(education_levels, colors):
                base_value = edu_data[level]
                # 生成略微波动的年度数据
                values = [base_value * (1 + np.random.uniform(-0.05, 0.05)) for _ in years]
                
                edu_dist_fig.add_trace(go.Bar(
                    name=level,
                    x=years,
                    y=values,
                    marker_color=color,
                    text=[f'{val:.1f}%' for val in values],
                    textposition='auto',
                    hovertemplate="Year: %{x}<br>" +
                                f"{level}: %{{y:.1f}}%<br>" +
                                "<extra></extra>"
                ))
            
            # 更新布局
            edu_dist_fig.update_layout(
                title=dict(
                    text=f"Education Level Distribution in {area_name} ({year_range[0]}-{year_range[1]})" 
                         if year_range[0] != year_range[1] 
                         else f"Education Level Distribution in {area_name} ({year_range[0]})",
                    x=0.5,
                    y=0.95,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=16)
                ),
                xaxis_title="Year",
                yaxis_title="Percentage (%)",
                height=400,
                yaxis=dict(range=[0, 100]),
                barmode='group',  # 并排显示
                bargap=0.15,
                bargroupgap=0.1,
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor='rgba(255,255,255,0.8)'
                )
            )
    else:
        edu_dist_fig.update_layout(
            title="Click an area to see education distribution",
            height=400
        )
    
    # 创建教育程度与回收率的相关性散点图
    edu_corr_fig = go.Figure()
    
    # 计算每个地区的高等教育比例与回收率的关系
    higher_edu_rates = []
    recycling_rates = []
    areas = []
    area_types = []
    
    for area in year_data['Area']:
        if area in EDUCATION_DATA:
            higher_edu_rates.append(EDUCATION_DATA[area]['Higher Education'])
            recycling_rates.append(float(year_data[year_data['Area'] == area]['Recycling_Rates'].values[0]))
            areas.append(area)
            area_types.append(year_data[year_data['Area'] == area]['London_Status'].values[0])
    
    for status in ['Core London', 'Outer London']:
        mask = [t == status for t in area_types]
        edu_corr_fig.add_trace(go.Scatter(
            x=[higher_edu_rates[i] for i in range(len(mask)) if mask[i]],
            y=[recycling_rates[i] for i in range(len(mask)) if mask[i]],
            mode='markers',
            name=status,
            text=[areas[i] for i in range(len(mask)) if mask[i]],
            marker=dict(size=10),
            hovertemplate="<b>%{text}</b><br>" +
                        "Higher Education: %{x:.1f}%<br>" +
                        "Recycling Rate: %{y:.1f}%<br>" +
                        "<extra></extra>"
        ))
    
    edu_corr_fig.update_layout(
        title=f"Higher Education vs Recycling Rate ({selected_year})",
        xaxis_title="Population with Higher Education (%)",
        yaxis_title="Recycling Rate (%)",
        height=400
    )
    
    return (map_fig, stats_content, trend_fig, dist_fig, corr_fig, 
            avg_rate, top_performer, yoy_text, gap_text, 
            edu_dist_fig, edu_corr_fig)

@callback(
    Output('year-range-selector', 'value'),
    Input('year-range-selector', 'value')
)
def update_time_selector(value):
    return value

# 其他回调函数将在后续实现... 

def get_year_range():
    df = load_data()
    min_year = df['Year'].min()
    max_year = df['Year'].max()
    return min_year, max_year 