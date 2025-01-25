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
            html.H1("Recycling Overview", className="text-center mb-4"),
            html.P("Explore London's recycling trends and patterns", 
                   className="text-center mb-4")
        ])
    ]),
    
    # 年份选择器
    dbc.Row([
        dbc.Col([
            html.Label([
                "Select Year: ",
                html.Small(id="year-display", className="text-muted")
            ], className="mb-2"),
            dcc.RangeSlider(
                id='year-slider',
                min=2003,
                max=2022,
                value=[2022, 2022],
                marks={str(year): str(year) for year in range(2003, 2023)},
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
    
    # 趋势图
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Overall Recycling Trend"),
                dbc.CardBody([
                    dcc.Graph(id="trend-chart")
                ])
            ])
        ])
    ], className="mb-4"),
    
    # 热力图
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Recycling Rates by Area and Year"),
                dbc.CardBody([
                    dcc.Graph(id="heatmap")
                ])
            ])
        ])
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
                        ], width=12),
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
     Output("trend-chart", "figure"),
     Output("heatmap", "figure"),
     Output("year-display", "children"),
     Output("rankings-table", "children"),
     Output("ranking-period-display", "children")],
    [Input("year-slider", "value")]
)
def update_overview(year_range):
    if year_range is None:
        year_range = [2022, 2022]  # 提供默认值
        
    df = load_data()
    
    # 1. 计算统计信息
    def get_stats(status):
        if year_range[0] == year_range[1]:
            data = df[(df['Year'] == year_range[0]) & (df['London_Status'] == status)]
        else:
            data = df[
                (df['Year'].between(year_range[0], year_range[1])) & 
                (df['London_Status'] == status)
            ]
        return {
            'avg': data['Recycling_Rates'].mean() if not data.empty else 0,
            'max': data['Recycling_Rates'].max() if not data.empty else 0,
            'min': data['Recycling_Rates'].min() if not data.empty else 0
        }
    
    try:
        core_stats = get_stats('Core London')
        outer_stats = get_stats('Outer London')
        non_london_stats = get_stats('Non-London')
        
        # 2. 创建趋势图
        trend_fig = update_trend(year_range)
        
        # 3. 创建热力图
        heatmap_fig = create_heatmap(df, year_range)
        
        # 4. 创建排名表格
        if year_range[0] == year_range[1]:
            table = create_rankings_table(df, year_range[0], 'year')
            period_display = f"({year_range[0]})"
        else:
            table = create_rankings_table(df, year_range, 'range')
            period_display = f"(Average {year_range[0]}-{year_range[1]})"
        
        return (
            create_stats_card(core_stats),
            create_stats_card(outer_stats),
            create_stats_card(non_london_stats),
            trend_fig,
            heatmap_fig,
            f"({year_range[0]}-{year_range[1]})",
            table,
            period_display
        )
    except Exception as e:
        print(f"Error in update_overview: {e}")
        # 返回空值或默认值
        return ["N/A"] * 7

def update_trend(year_range):
    if year_range is None:
        year_range = [2022, 2022]
        
    df = load_data()
    
    # 创建趋势数据
    trend_data = df.groupby(['Year', 'London_Status'])['Recycling_Rates'].mean().reset_index()
    
    # 添加伦敦整体平均值
    london_overall = df[df['London_Status'].isin(['Core London', 'Outer London'])].groupby('Year')['Recycling_Rates'].mean().reset_index()
    london_overall['London_Status'] = 'London Overall'
    
    # 合并数据
    trend_data = pd.concat([trend_data, london_overall])
    
    # 根据选择的年份范围筛选数据
    trend_data = trend_data[
        (trend_data['Year'] >= year_range[0]) & 
        (trend_data['Year'] <= year_range[1])
    ]
    
    # 设置颜色映射
    color_map = {
        'Core London': '#4e79a7',
        'Outer London': '#f28e2b',
        'Non-London': '#59a14f',
        'London Overall': '#e15759'
    }
    
    # 根据是否是单一年份选择图表类型
    if year_range[0] == year_range[1]:
        # 单一年份显示柱状图
        fig = px.bar(
            trend_data,
            x='London_Status',
            y='Recycling_Rates',
            color='London_Status',
            title=f'Recycling Rates by Region Type ({year_range[0]})',
            labels={'Recycling_Rates': 'Average Recycling Rate (%)',
                   'London_Status': 'Region Type'},
            color_discrete_map=color_map,
            text='Recycling_Rates'
        )
        
        # 更新柱状图样式
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='auto',
            hovertemplate="%{y:.1f}%<br>" +
                         "<extra></extra>"
        )
        
        # 柱状图特定布局
        fig.update_layout(
            showlegend=False,  # 不需要图例因为颜色已经表示了区域类型
            yaxis=dict(
                range=[0, max(trend_data['Recycling_Rates']) * 1.1],
                tickformat='.1f'
            )
        )
    else:
        # 时间范围显示折线图
        fig = px.line(
            trend_data,
            x='Year',
            y='Recycling_Rates',
            color='London_Status',
            title='Recycling Rates Trends by Region Type',
            labels={'Recycling_Rates': 'Average Recycling Rate (%)',
                   'Year': 'Year',
                   'London_Status': 'Region Type'},
            color_discrete_map=color_map
        )
        
        # 折线图特定布局
        fig.update_layout(
            xaxis=dict(
                range=[year_range[0]-0.5, year_range[1]+0.5],
                tickmode='linear',
                dtick=1
            )
        )
    
    # 通用布局设置
    fig.update_layout(
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(240,240,240,0.3)',
        xaxis_gridcolor='rgba(255,255,255,0.8)',
        yaxis_gridcolor='rgba(255,255,255,0.8)'
    )
    
    return fig

def create_heatmap(df, year_range):
    # 筛选数据
    df_filtered = df[
        (df['Year'] >= year_range[0]) & 
        (df['Year'] <= year_range[1])
    ]
    
    # 创建热力图数据
    heatmap_data = df_filtered.pivot_table(
        values='Recycling_Rates',
        index='Area',
        columns='Year',
        aggfunc='mean'
    ).round(1)
    
    # 按平均回收率排序区域
    area_means = heatmap_data.mean(axis=1).sort_values(ascending=False)
    heatmap_data = heatmap_data.reindex(area_means.index)
    
    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale=[
            [0, 'rgb(255,255,255)'],      # 最低值为白色
            [0.2, 'rgb(220,230,242)'],    # 浅蓝色
            [0.4, 'rgb(164,194,244)'],    # 中浅蓝色
            [0.6, 'rgb(109,158,235)'],    # 中蓝色
            [0.8, 'rgb(54,122,227)'],     # 深蓝色
            [1, 'rgb(39,73,142)']         # 最深蓝色
        ],
        text=heatmap_data.values.round(1),
        texttemplate='%{text}%',
        textfont={"size": 10, "color": "black"},
        hoverongaps=False,
        hovertemplate='Area: %{y}<br>Year: %{x}<br>Rate: %{z:.1f}%<extra></extra>'
    ))
    
    title_text = ('Recycling Rates by Area and Year ' +
                 f"({year_range[0]}-{year_range[1]})" if year_range[0] != year_range[1]
                 else f"({year_range[0]})")
    
    fig.update_layout(
        title=title_text,
        height=800,
        yaxis=dict(
            title='Area',
            tickfont=dict(size=10)
        ),
        xaxis=dict(
            title='Year',
            tickmode='linear',
            dtick=1
        ),
        margin=dict(l=150, r=20, t=30, b=50)
    )
    
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


