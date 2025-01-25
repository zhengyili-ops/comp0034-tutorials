from dash import register_page, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils import load_data

register_page(__name__, path='/recycling/trends', name='Recycling Trends')

def get_area_options():
    """获取所有区域选项"""
    df = load_data()
    options = [
        {'label': '--- Overview Groups ---', 'value': 'group_header', 'disabled': True},
        {'label': 'All Areas', 'value': 'all'},
        {'label': 'London vs Non-London', 'value': 'london_vs_non'},
        
        {'label': '--- London Groups ---', 'value': 'london_header', 'disabled': True},
        {'label': 'All London Boroughs', 'value': 'london_all'},
        {'label': 'Core London Only', 'value': 'core_london'},
        {'label': 'Outer London Only', 'value': 'outer_london'},
        
        {'label': '--- Performance Groups ---', 'value': 'performance_header', 'disabled': True},
        {'label': 'Top 5 London', 'value': 'top_5_london'},
        {'label': 'Top 5 Non-London', 'value': 'top_5_non_london'},
        {'label': 'Bottom 5 London', 'value': 'bottom_5_london'},
        {'label': 'Bottom 5 Non-London', 'value': 'bottom_5_non_london'},
    ]
    
    # 添加伦敦区域分组
    options.append({'label': '--- London Boroughs ---', 'value': 'london_areas_header', 'disabled': True})
    london_areas = sorted(df[df['London_Status'].isin(['Core London', 'Outer London'])]['Area'].unique())
    for area in london_areas:
        options.append({'label': f"  • {area}", 'value': area})
    
    # 添加非伦敦区域分组
    options.append({'label': '--- Non-London Areas ---', 'value': 'non_london_header', 'disabled': True})
    non_london_areas = sorted(df[df['London_Status'] == 'Non-London']['Area'].unique())
    for area in non_london_areas:
        options.append({'label': f"  • {area}", 'value': area})
    
    return options

def create_comparison_chart(df_grouped, year_range, chart_type):
    """创建伦敦与非伦敦的对比图表"""
    # 合并伦敦数据
    df_final = df_grouped.groupby(['Year', 'Area'])['Recycling_Rates'].mean().reset_index()
    
    # 创建基础图表配置
    fig_config = {
        'x': 'Year',
        'y': 'Recycling_Rates',
        'color': 'Area',
        'title': 'London vs Non-London Recycling Rates Comparison',
        'labels': {'Recycling_Rates': 'Recycling Rate (%)', 'Area': 'Region'},
        'template': 'plotly_white'
    }
    
    # 根据图表类型创建图表
    if chart_type == 'bar':
        fig = px.bar(
            df_final,
            **fig_config,
            barmode='group'
        )
    elif chart_type == 'area':
        fig = px.area(
            df_final,
            **fig_config
        )
    else:  # 默认为折线图
        fig = px.line(
            df_final,
            **fig_config
        )
    
    # 优化图表布局
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Recycling Rate (%)",
        legend_title="Region",
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02
        ),
        height=500
    )
    
    # 优化坐标轴
    fig.update_xaxes(
        dtick=1,
        gridcolor='lightgrey'
    )
    
    fig.update_yaxes(
        gridcolor='lightgrey',
        zeroline=True,
        zerolinecolor='grey',
        zerolinewidth=1
    )
    
    # 创建统计信息
    stats = []
    for area in df_final['Area'].unique():
        area_data = df_final[df_final['Area'] == area]
        
        try:
            # 获取开始和结束年份的数据
            start_rate = area_data[area_data['Year'] == year_range[0]]['Recycling_Rates'].iloc[0]
            end_rate = area_data[area_data['Year'] == year_range[1]]['Recycling_Rates'].iloc[0]
            change = end_rate - start_rate
            
            # 计算平均值和趋势
            avg_rate = area_data['Recycling_Rates'].mean()
            
            stats.append(dbc.Card([
                dbc.CardHeader(area),
                dbc.CardBody([
                    html.P([
                        html.Strong("Average Rate: "), f"{avg_rate:.1f}%"
                    ]),
                    html.P([
                        html.Strong("Start Rate: "), f"{start_rate:.1f}%"
                    ]),
                    html.P([
                        html.Strong("End Rate: "), f"{end_rate:.1f}%"
                    ]),
                    html.P([
                        html.Strong("Overall Change: "), 
                        html.Span(
                            f"{change:+.1f}%",
                            style={'color': 'green' if change > 0 else 'red'}
                        )
                    ])
                ])
            ], className="mb-3"))
            
        except Exception as e:
            print(f"Error calculating stats for {area}: {e}")
            stats.append(dbc.Card([
                dbc.CardHeader(area),
                dbc.CardBody("No data available for selected time range")
            ], className="mb-3"))
    
    # 将统计信息包装在网格布局中
    stats_grid = dbc.Row([
        dbc.Col(stat, width=6) for stat in stats
    ])
    
    return fig, stats_grid

def calculate_trend_statistics(area_data, year_range):
    """计算区域的趋势统计信息"""
    try:
        # 基础统计
        start_rate = area_data[area_data['Year'] == year_range[0]]['Recycling_Rates'].iloc[0]
        end_rate = area_data[area_data['Year'] == year_range[1]]['Recycling_Rates'].iloc[0]
        change = end_rate - start_rate
        avg_rate = area_data['Recycling_Rates'].mean()
        
        # 计算额外的统计信息
        max_rate = area_data['Recycling_Rates'].max()
        min_rate = area_data['Recycling_Rates'].min()
        max_year = area_data[area_data['Recycling_Rates'] == max_rate]['Year'].iloc[0]
        min_year = area_data[area_data['Recycling_Rates'] == min_rate]['Year'].iloc[0]
        
        # 计算年均增长率
        years_diff = year_range[1] - year_range[0]
        annual_growth = (change / years_diff) if years_diff > 0 else 0
        
        return {
            'start_rate': start_rate,
            'end_rate': end_rate,
            'change': change,
            'avg_rate': avg_rate,
            'max_rate': max_rate,
            'min_rate': min_rate,
            'max_year': max_year,
            'min_year': min_year,
            'annual_growth': annual_growth
        }
    except Exception as e:
        print(f"Error calculating statistics: {e}")
        return None

def create_stat_card(area, stats, year_range):
    """创建统计信息卡片"""
    if not stats:
        return dbc.Card([
            dbc.CardHeader(area),
            dbc.CardBody("No data available for selected time range")
        ], className="mb-3")
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5(area, className="mb-0"),
            html.Small(f"Average Rate: {stats['avg_rate']:.1f}%", 
                      className="text-muted")
        ]),
        dbc.CardBody([
            # 主要指标
            dbc.Row([
                dbc.Col([
                    html.H6("Overall Change", className="text-muted"),
                    html.H4([
                        html.Span(
                            f"{stats['change']:+.1f}%",
                            style={
                                'color': 'green' if stats['change'] > 0 else 'red',
                                'font-weight': 'bold'
                            }
                        )
                    ])
                ], width=6),
                dbc.Col([
                    html.H6("Annual Growth", className="text-muted"),
                    html.H4([
                        html.Span(
                            f"{stats['annual_growth']:+.1f}%",
                            style={
                                'color': 'green' if stats['annual_growth'] > 0 else 'red',
                                'font-weight': 'bold'
                            }
                        )
                    ])
                ], width=6),
            ], className="mb-3"),
            
            # 详细统计
            dbc.Row([
                dbc.Col([
                    html.P([
                        html.Strong(f"Start ({year_range[0]}): "),
                        f"{stats['start_rate']:.1f}%"
                    ]),
                    html.P([
                        html.Strong(f"End ({year_range[1]}): "),
                        f"{stats['end_rate']:.1f}%"
                    ])
                ], width=6),
                dbc.Col([
                    html.P([
                        html.Strong("Peak: "),
                        f"{stats['max_rate']:.1f}% ({stats['max_year']})"
                    ]),
                    html.P([
                        html.Strong("Low: "),
                        f"{stats['min_rate']:.1f}% ({stats['min_year']})"
                    ])
                ], width=6)
            ])
        ])
    ], className="mb-3")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Recycling Trends Analysis", className="text-center mb-4")
        ])
    ]),
    
    # 控制面板
    dbc.Row([
        # 区域选择
        dbc.Col([
            html.Label("Select Areas:", className="mb-2"),
            dcc.Dropdown(
                id='area-selector',
                options=get_area_options(),
                value=['london_all'],
                multi=True,
                placeholder='Search and select areas...',
                searchable=True,  # 启用搜索
                clearable=True,   # 允许清除选择
                className="mb-3"
            ),
            # 时间范围选择
            html.Label("Select Time Range:", className="mb-2"),
            dcc.RangeSlider(
                id='year-range-selector',
                min=2003,
                max=2022,
                value=[2003, 2022],
                marks={year: str(year) for year in range(2003, 2023, 2)},
                tooltip={'placement': 'bottom', 'always_visible': True}
            ),
            # 图表类型选择
            html.Label("Chart Type:", className="mt-3 mb-2"),
            dbc.RadioItems(
                id='chart-type',
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
                dbc.CardHeader("Recycling Rate Trends"),
                dbc.CardBody([
                    dcc.Graph(id='trend-chart')
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # 统计信息
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Trend Statistics"),
                dbc.CardBody(id='trend-stats')
            ])
        ], width=12)
    ])
], fluid=True)

@callback(
    [Output('trend-chart', 'figure', allow_duplicate=True),
     Output('trend-stats', 'children', allow_duplicate=True)],
    [Input('area-selector', 'value'),
     Input('year-range-selector', 'value'),
     Input('chart-type', 'value')],
    prevent_initial_call=True
)
def update_trend_analysis(selected_areas, year_range, chart_type):
    df = load_data()
    df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    
    # 初始化变量
    filtered_df = pd.DataFrame()
    mask = pd.Series(False, index=df.index)
    fig = None  # 初始化图表变量
    
    # 创建基础图表配置
    fig_config = {
        'x': 'Year',
        'y': 'Recycling_Rates',
        'color': 'Area',
        'title': 'Recycling Rate Trends',
        'labels': {'Recycling_Rates': 'Recycling Rate (%)', 'Area': 'Region'},
        'template': 'plotly_white'
    }
    
    # 处理区域选择
    for area in selected_areas:
        if area == 'london_all':
            # 计算每个伦敦区域的数据
            london_df = df[df['London_Status'].isin(['Core London', 'Outer London'])]
            
            # 计算Core London和Outer London的平均值
            core_avg = df[df['London_Status'] == 'Core London'].groupby('Year')['Recycling_Rates'].mean().reset_index()
            core_avg['Area'] = 'Core London'
            
            outer_avg = df[df['London_Status'] == 'Outer London'].groupby('Year')['Recycling_Rates'].mean().reset_index()
            outer_avg['Area'] = 'Outer London'
            
            # 计算所有伦敦区域的总平均值
            london_avg = london_df.groupby('Year')['Recycling_Rates'].mean().reset_index()
            london_avg['Area'] = 'London Overall Average'
            
            # 合并数据
            if filtered_df.empty:
                filtered_df = pd.concat([core_avg, outer_avg, london_avg])
            else:
                filtered_df = pd.concat([filtered_df, core_avg, outer_avg, london_avg])
            
            # 为折线图设置特殊样式
            if chart_type == 'line':
                fig = px.line(filtered_df, **fig_config)
                
                # 设置线条样式
                for trace in fig.data:
                    if trace.name == 'London Overall Average':
                        trace.line.width = 3
                        trace.line.color = 'black'
                        trace.line.dash = 'solid'
                    elif trace.name == 'Core London':
                        trace.line.width = 2
                        trace.line.dash = 'dash'
                    elif trace.name == 'Outer London':
                        trace.line.width = 2
                        trace.line.dash = 'dot'
                
                # 更新图表布局，移除重复的说明
                fig.update_layout(
                    title="London Boroughs Recycling Trends",
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=1.02,
                        bgcolor="rgba(255, 255, 255, 0.8)",
                        bordercolor="LightGrey",
                        borderwidth=1
                    )
                )
        
        elif area == 'london_vs_non':
            # 添加London和Non-London的平均值
            london_mask = df['London_Status'].isin(['Core London', 'Outer London'])
            non_london_mask = df['London_Status'] == 'Non-London'
            
            # 计算平均值
            london_avg = df[london_mask].groupby('Year')['Recycling_Rates'].mean().reset_index()
            london_avg['Area'] = 'London Average'
            non_london_avg = df[non_london_mask].groupby('Year')['Recycling_Rates'].mean().reset_index()
            non_london_avg['Area'] = 'Non-London Average'
            
            # 合并平均值数据
            if filtered_df.empty:
                filtered_df = pd.concat([london_avg, non_london_avg])
            else:
                filtered_df = pd.concat([filtered_df, london_avg, non_london_avg])
        elif area == 'core_london':
            mask |= df['London_Status'] == 'Core London'
        elif area == 'outer_london':
            mask |= df['London_Status'] == 'Outer London'
        elif area == 'top_5_london':
            latest_year = df['Year'].max()
            london_df = df[(df['Year'] == latest_year) & 
                         (df['London_Status'].isin(['Core London', 'Outer London']))]
            top_areas = london_df.nlargest(5, 'Recycling_Rates')['Area']
            mask |= df['Area'].isin(top_areas)
        elif area == 'top_5_non_london':
            latest_year = df['Year'].max()
            non_london_df = df[(df['Year'] == latest_year) & 
                             (df['London_Status'] == 'Non-London')]
            top_areas = non_london_df.nlargest(5, 'Recycling_Rates')['Area']
            mask |= df['Area'].isin(top_areas)
        elif area == 'bottom_5_london':
            latest_year = df['Year'].max()
            london_df = df[(df['Year'] == latest_year) & 
                         (df['London_Status'].isin(['Core London', 'Outer London']))]
            bottom_areas = london_df.nsmallest(5, 'Recycling_Rates')['Area']
            mask |= df['Area'].isin(bottom_areas)
        elif area == 'bottom_5_non_london':
            latest_year = df['Year'].max()
            non_london_df = df[(df['Year'] == latest_year) & 
                             (df['London_Status'] == 'Non-London')]
            bottom_areas = non_london_df.nsmallest(5, 'Recycling_Rates')['Area']
            mask |= df['Area'].isin(bottom_areas)
        elif not area.endswith('_header'):
            mask |= df['Area'] == area
    
    # 如果没有选择任何区域，返回空图表
    if filtered_df.empty:
        return {}, "Please select at least one area to display"
    
    # 如果图表还没有创建，根据图表类型创建
    if fig is None:
        if chart_type == 'bar':
            fig = px.bar(filtered_df, **fig_config, barmode='group')
            fig.update_layout(
                bargap=0.2,
                bargroupgap=0.1
            )
        elif chart_type == 'area':
            fig = px.area(filtered_df, **fig_config)
        else:  # 默认为折线图
            fig = px.line(filtered_df, **fig_config)
    
    # 统一的图表布局设置
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Recycling Rate (%)",
        legend_title="Region",
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="LightGrey",
            borderwidth=1
        ),
        height=500
    )
    
    # 计算统计信息
    stats = []
    for area in filtered_df['Area'].unique():
        area_data = filtered_df[filtered_df['Area'] == area]
        area_stats = calculate_trend_statistics(area_data, year_range)
        stats.append(create_stat_card(area, area_stats, year_range))
    
    # 将统计信息包装在网格布局中
    stats_grid = dbc.Row([
        dbc.Col(stat, width=4) for stat in stats
    ], className="g-3")
    
    return fig, stats_grid 