from dash import register_page, html, dcc, callback, Input, Output, callback_context
import dash_bootstrap_components as dbc
import sys
from pathlib import Path

# 添加父目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent.parent))

# 使用绝对导入
from utils.recycling_figures import (
    recycling_bar_chart,
    recycling_scatter_plot
)
from utils import load_data
import plotly.express as px
import pandas as pd
import dash
import numpy as np

# 添加数据验证
print("\n=== Data Validation ===")
test_df = load_data()
if test_df is not None and not test_df.empty:
    print(f"Data loaded successfully. Shape: {test_df.shape}")
    print("Columns:", test_df.columns.tolist())
    print("Sample data:")
    print(test_df.head())
else:
    print("Error: Failed to load data")

# 注册页面
register_page(
    __name__,
    path='/recycling/comparison',
    name='Regional Comparison',
    title='Regional Comparison',
    location="recycling"
)

# 在布局开始前添加打印
print("Initializing comparison page layout...")

# 在布局之前加载数据
df = load_data()

def get_area_options():
    """获取区域选项"""
    df = load_data()
    return [
        {'label': '--- Overview Groups ---', 'value': 'group_header', 'disabled': True},
        {'label': 'All Areas', 'value': 'all'},
        {'label': 'London vs Non-London', 'value': 'london_vs_non'},
        {'label': '--- London Groups ---', 'value': 'london_header', 'disabled': True},
        {'label': 'All London Boroughs', 'value': 'london_all'},
        {'label': 'Core London Only', 'value': 'core_london'},
        {'label': 'Outer London Only', 'value': 'outer_london'},
        {'label': 'Top 5 London', 'value': 'top_5_london'},
        {'label': 'Bottom 5 London', 'value': 'bottom_5_london'},
        {'label': '--- Performance Groups ---', 'value': 'performance_header', 'disabled': True},
        {'label': 'Top 5 Non-London', 'value': 'top_5_non_london'},
        {'label': 'Bottom 5 Non-London', 'value': 'bottom_5_non_london'},
        {'label': '--- London Boroughs ---', 'value': 'london_boroughs_header', 'disabled': True},
    ] + [
        {'label': area, 'value': area} 
        for area in sorted(df[df['London_Status'].isin(['Core London', 'Outer London'])]['Area'].unique())
    ] + [
        {'label': '--- Non-London Areas ---', 'value': 'non_london_header', 'disabled': True},
    ] + [
        {'label': area, 'value': area}
        for area in sorted(df[df['London_Status'] == 'Non-London']['Area'].unique())
    ]

# 定义布局
layout = dbc.Container([
    # 标题
    dbc.Row([
        dbc.Col(
            html.H1("Regional Comparison", className="text-center mb-4")
        )
    ]),
    
    # 区域选择
    dbc.Row([
        dbc.Col([
            html.Label('Select Areas:', className='mb-2'),
            dcc.Dropdown(
                id='comparison-area-selector',
                options=get_area_options(),
                value=['london_all'],
                multi=True
            )
        ])
    ], className='mb-4'),
    
    # 时间选择
    dbc.Row([
        dbc.Col([
            html.Label('Select Time Range:', className='mb-2'),
            dcc.RangeSlider(
                id='comparison-year-range',
                min=2003,
                max=2022,
                value=[2003, 2022],
                marks={year: str(year) for year in range(2003, 2023, 2)},
                tooltip={'placement': 'bottom', 'always_visible': True}
            )
        ])
    ], className='mb-4'),
    
    # 图表类型选择
    dbc.Row([
        dbc.Col([
            html.Label("Chart Type:", className="mb-2"),
            dbc.RadioItems(
                id='comparison-chart-type',
                options=[
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Area Chart', 'value': 'area'}
                ],
                value='line',
                inline=True,
                className="mb-3"
            )
        ])
    ], className='mb-4'),
    
    # 主要趋势图
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Recycling Rate Trends"),
                dbc.CardBody(
                    dcc.Graph(id='comparison-trend-chart')
                )
            ])
        )
    ], className='mb-4'),
    
    # 下方的统计图表
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Population Trends"),
                dbc.CardBody(
                    dcc.Graph(id='comparison-population-chart')
                )
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Population Density"),
                dbc.CardBody(
                    dcc.Graph(id='comparison-density-chart')
                )
            ]),
            width=6
        )
    ], className='mb-4'),
    
    # 统计信息
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Statistics"),
                dbc.CardBody(id='comparison-trend-stats')
            ])
        )
    ])
], fluid=True)

# 验证布局组件
print("\n=== Layout Validation ===")
if layout is not None:
    components = []
    for row in layout.children:
        if hasattr(row, 'children'):
            for col in row.children:
                if hasattr(col, 'children'):
                    for component in col.children:
                        if hasattr(component, 'id'):
                            components.append(component.id)
    print(f"Layout components: {components}")
else:
    print("Error: Layout is None")

# 回调部分修改
@callback(
    Output('comparison-trend-chart', 'figure'),
    [Input('comparison-area-selector', 'value'),
     Input('comparison-year-range', 'value'),
     Input('comparison-chart-type', 'value')]
)
def update_trend_chart(selected_areas, year_range, chart_type):
    """更新趋势图"""
    print("\n=== Callback Triggered ===")
    print(f"Selected areas: {selected_areas}")
    print(f"Year range: {year_range}")
    print(f"Chart type: {chart_type}")

    if not selected_areas or not year_range or not chart_type:
        print("Missing required inputs")
        return {}

    df_filtered = get_filtered_data(selected_areas, year_range)
    
    if df_filtered.empty:
        print("No data returned from get_filtered_data")
        return {
            'data': [],
            'layout': {
                'title': 'No data available for the selected criteria',
                'xaxis': {'visible': False},
                'yaxis': {'visible': False},
                'annotations': [{
                    'text': 'Please select different areas or time range',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 20}
                }]
            }
        }

    print(f"Data filtered successfully. Shape: {df_filtered.shape}")
    print("Areas in filtered data:", df_filtered['Area'].unique())
    print("Sample of filtered data:")
    print(df_filtered.head())

    fig = create_trend_chart(df_filtered, chart_type)
    return fig

@callback(
    Output('comparison-population-chart', 'figure'),  # 移除 allow_duplicate=True
    [Input('comparison-area-selector', 'value'),
     Input('comparison-year-range', 'value')]
)
def update_population_chart(selected_areas, year_range):
    """更新人口趋势图"""
    if not selected_areas or not year_range:  # 添加输入验证
        return {}
        
    df_filtered = get_filtered_data(selected_areas, year_range)
    return create_population_chart(df_filtered)

@callback(
    Output('comparison-density-chart', 'figure'),  # 移除 allow_duplicate=True
    [Input('comparison-area-selector', 'value'),
     Input('comparison-year-range', 'value')]
)
def update_density_chart(selected_areas, year_range):
    """更新密度趋势图"""
    if not selected_areas or not year_range:  # 添加输入验证
        return {}
        
    df_filtered = get_filtered_data(selected_areas, year_range)
    return create_density_chart(df_filtered)

@callback(
    Output('comparison-trend-stats', 'children'),  # 移除 allow_duplicate=True
    [Input('comparison-area-selector', 'value'),
     Input('comparison-year-range', 'value')]
)
def update_stats(selected_areas, year_range):
    """更新统计信息"""
    if not selected_areas or not year_range:  # 添加输入验证
        return html.Div("Please select areas and time range")
        
    df_filtered = get_filtered_data(selected_areas, year_range)
    return create_stats_cards(df_filtered)

# 辅助函数
def get_filtered_data(selected_areas, year_range):
    """获取过滤后的数据"""
    df = load_data()
    print("\n" + "="*50)
    print("DEBUG OUTPUT START")
    print("="*50)
    print(f"Selected areas: {selected_areas}")
    print(f"Year range: {year_range}")
    print(f"Original data shape: {df.shape}")
    
    # 检查数据
    print("\nUnique London statuses:", df['London_Status'].unique())
    print("\nSample of Recycling Rates:")
    print(df[['Area', 'London_Status', 'Year', 'Recycling_Rates']].head(10))

    # 如果没有选择任何区域，返回空数据框
    if not selected_areas:
        print("No areas selected")
        return pd.DataFrame()

    # 创建基础年份过滤
    df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    print(f"Data after year filtering: {df.shape}")

    # 存储所有过滤后的数据
    filtered_dfs = []

    for area in selected_areas:
        print(f"\nProcessing area: {area}")
        
        if area == 'bottom_5_london':
            try:
                # 获取最新年份的伦敦数据
                latest_year = df['Year'].max()
                print(f"Processing bottom 5 London for year {latest_year}")
                
                # 获取最新年份的伦敦数据
                latest_london_data = df[
                    (df['Year'] == latest_year) & 
                    df['London_Status'].isin(['Core London', 'Outer London'])
                ]
                
                # 确保数据已排序
                latest_london_data = latest_london_data.sort_values('Recycling_Rates')
                print("\nRecycling rates for all London areas:")
                print(latest_london_data[['Area', 'Recycling_Rates']].to_string())
                
                # 获取底部5个区域
                bottom_areas = latest_london_data['Area'].head(5).tolist()
                print(f"\nSelected bottom 5 areas: {bottom_areas}")
                
                # 获取这些区域的所有年份数据
                bottom_data = df[df['Area'].isin(bottom_areas)]
                print(f"Found {len(bottom_data)} records for these areas")
                
                if not bottom_data.empty:
                    filtered_dfs.append(bottom_data)
                    print("Data added successfully")
                
            except Exception as e:
                print(f"Error in bottom_5_london: {str(e)}")
                import traceback
                print(traceback.format_exc())

        elif area == 'bottom_5_non_london':
            try:
                # 获取最新年份的非伦敦数据
                latest_year = df['Year'].max()
                print(f"Latest year: {latest_year}")
                
                # 获取非伦敦数据
                non_london_mask = df['London_Status'] == 'Non-London'
                non_london_data = df[non_london_mask]
                print(f"Total Non-London data records: {len(non_london_data)}")
                
                # 获取最新年份的数据
                latest_non_london_data = non_london_data[non_london_data['Year'] == latest_year]
                print(f"Latest year Non-London data records: {len(latest_non_london_data)}")
                print("Available areas:", latest_non_london_data['Area'].unique())
                print("Recycling rates:", latest_non_london_data[['Area', 'Recycling_Rates']].to_string())
                
                # 获取后5名区域
                bottom_areas = latest_non_london_data.sort_values('Recycling_Rates')['Area'].head(5).unique()
                print(f"Bottom 5 Non-London areas: {bottom_areas}")
                
                # 获取这些区域的所有年份数据
                bottom_data = df[df['Area'].isin(bottom_areas)]
                print(f"Found {len(bottom_data)} records for bottom 5 areas")
                
                if not bottom_data.empty:
                    filtered_dfs.append(bottom_data)
                    print("Successfully added bottom 5 Non-London data")
                else:
                    print("Warning: No data found for bottom 5 Non-London areas")
                    
            except Exception as e:
                print(f"Error processing bottom 5 Non-London: {str(e)}")
        
        elif area == 'all':
            filtered_dfs.append(df.copy())
            print("Added all data")
            
        elif area == 'london_vs_non':
            # 计算伦敦平均值
            london_data = df[df['London_Status'].isin(['Core London', 'Outer London'])]
            london_avg = london_data.groupby('Year')['Recycling_Rates'].mean().reset_index()
            london_avg['Area'] = 'London Average'
            
            # 计算非伦敦平均值
            non_london_data = df[df['London_Status'] == 'Non-London']
            non_london_avg = non_london_data.groupby('Year')['Recycling_Rates'].mean().reset_index()
            non_london_avg['Area'] = 'Non-London Average'
            
            filtered_dfs.extend([london_avg, non_london_avg])
            print("Added London vs Non-London averages")
            
        elif area == 'london_all':
            london_data = df[df['London_Status'].isin(['Core London', 'Outer London'])]
            filtered_dfs.append(london_data)
            print(f"Added all London data: {len(london_data)} records")
            
        elif area == 'core_london':
            core_data = df[df['London_Status'] == 'Core London']
            filtered_dfs.append(core_data)
            print(f"Added Core London data: {len(core_data)} records")
            
        elif area == 'outer_london':
            outer_data = df[df['London_Status'] == 'Outer London']
            filtered_dfs.append(outer_data)
            print(f"Added Outer London data: {len(outer_data)} records")
            
        elif area == 'top_5_london':
            # 获取最新年份的伦敦数据
            latest_year = df['Year'].max()
            print(f"Latest year for Top 5: {latest_year}")
            
            london_data = df[df['London_Status'].isin(['Core London', 'Outer London'])]
            latest_london_data = london_data[london_data['Year'] == latest_year]
            print(f"Latest London data shape: {latest_london_data.shape}")
            
            # 获取前5名区域
            top_areas = latest_london_data.nlargest(5, 'Recycling_Rates')['Area'].unique()
            print(f"Top 5 London areas identified: {top_areas}")
            
            # 获取这些区域的所有年份数据
            top_data = df[df['Area'].isin(top_areas)]
            print(f"Found {len(top_data)} records for top 5 areas")
            if not top_data.empty:
                filtered_dfs.append(top_data)
            
        else:
            # 处理单个区域选择
            print(f"Looking for area: {area}")
            area_data = df[df['Area'] == area]
            print(f"Found {len(area_data)} records")
            if not area_data.empty:
                filtered_dfs.append(area_data)
                print(f"Added data for area: {area}")
            else:
                print(f"Warning: No data found for area: {area}")
                print(f"Available areas: {df['Area'].unique()}")
    
    # 合并所有过滤后的数据
    if filtered_dfs:
        result = pd.concat(filtered_dfs, ignore_index=True)
        print("\n=== Final Results ===")
        print(f"Shape: {result.shape}")
        print("Areas included:", result['Area'].unique())
        print("Sample data:")
        print(result.head())
        return result
    else:
        print("\nNo data to return")
        return pd.DataFrame()

def create_trend_chart(df_filtered, chart_type):
    """创建趋势图"""
    print("\n=== Creating Trend Chart ===")
    print(f"Chart type: {chart_type}")
    print(f"Data shape: {df_filtered.shape}")
    print("Unique areas:", df_filtered['Area'].unique())
    
    if df_filtered.empty:
        return {}
    
    # 确保数据类型正确
    df_filtered['Year'] = pd.to_numeric(df_filtered['Year'])
    df_filtered['Recycling_Rates'] = pd.to_numeric(df_filtered['Recycling_Rates'])
    
    # 创建图表
    if chart_type == 'bar':
        fig = px.bar(
            df_filtered,
            x='Year',
            y='Recycling_Rates',
            color='Area',
            title='Recycling Rate Trends',
            labels={'Recycling_Rates': 'Recycling Rate (%)', 'Area': 'Region'},
            barmode='group'
        )
    elif chart_type == 'area':
        fig = px.area(
            df_filtered,
            x='Year',
            y='Recycling_Rates',
            color='Area',
            title='Recycling Rate Trends',
            labels={'Recycling_Rates': 'Recycling Rate (%)', 'Area': 'Region'}
        )
    else:  # 默认为折线图
        fig = px.line(
            df_filtered,
            x='Year',
            y='Recycling_Rates',
            color='Area',
            title='Recycling Rate Trends',
            labels={'Recycling_Rates': 'Recycling Rate (%)', 'Area': 'Region'}
        )
    
    # 更新布局
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="LightGrey",
            borderwidth=1
        ),
        margin=dict(l=40, r=20, t=60, b=40)
    )
    
    return fig

def create_population_chart(df_filtered):
    """创建人口趋势图"""
    population_fig = px.line(
        df_filtered,
        x='Year',
        y='Population',
        color='Area',
        title='Population Trends'
    )
    
    # 统一图表样式
    population_fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return population_fig

def create_density_chart(df_filtered):
    """创建密度趋势图"""
    density_fig = px.line(
        df_filtered,
        x='Year',
        y='Population_Density',
        color='Area',
        title='Population Density Trends'
    )
    
    # 统一图表样式
    density_fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return density_fig

def create_stats_cards(df_filtered):
    """创建统计信息卡片"""
    stats = []
    for area in df_filtered['Area'].unique():
        area_data = df_filtered[df_filtered['Area'] == area]
        if not area_data.empty:
            stats.append(
                dbc.Card([
                    dbc.CardHeader(area),
                    dbc.CardBody([
                        html.P(f"Average Recycling Rate: {area_data['Recycling_Rates'].mean():.1f}%"),
                        html.P(f"Latest Population: {area_data['Population'].iloc[-1]:,.0f}" if 'Population' in area_data.columns else ""),
                        html.P(f"Latest Density: {area_data['Population_Density'].iloc[-1]:,.1f} per km²" if 'Population_Density' in area_data.columns else "")
                    ])
                ], className="mb-3")
            )
    
    return stats 