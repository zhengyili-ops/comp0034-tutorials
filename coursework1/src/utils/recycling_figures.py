import pandas as pd
import plotly.express as px
from pathlib import Path
from dash import dash_table, html, dcc
import plotly.graph_objects as go
import os
import dash_bootstrap_components as dbc
import sqlite3

# 更新数据路径
current_dir = Path(__file__).parent.parent.parent  # 返回到 coursework1 目录
data_path = current_dir / "data" / "newdata.csv"

def get_areas_by_type(area_type):
    """根据区域类型获取对应的区域列表"""
    df = pd.read_csv(data_path)
    if area_type == 'london_all':
        return df[df['London_Status'].isin(['Core London', 'Outer London'])]['Area'].unique().tolist()
    elif area_type == 'non_london':
        return df[df['London_Status'] == 'Non-London']['Area'].unique().tolist()
    elif area_type == 'core_london':
        return df[df['London_Status'] == 'Core London']['Area'].unique().tolist()
    elif area_type == 'outer_london':
        return df[df['London_Status'] == 'Outer London']['Area'].unique().tolist()
    else:
        return [area_type]  # 单个区域

def load_data():
    """加载和预处理数据"""
    try:
        current_dir = Path(__file__).parent.parent.parent
        db_path = current_dir / "data" / "paralympics.db"  # 数据库路径
        connection = sqlite3.connect(db_path)

        # 从数据库中读取数据
        query = "SELECT * FROM paralympics_data"  # 假设你的表名为 paralympics_data
        df = pd.read_sql(query, connection)

        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def recycling_line_chart(df):
    """创建回收率趋势线图"""
    try:
        # 按年份和区域类型计算平均回收率
        trend_data = df.groupby(['Year', 'London_Status'])['Recycling_Rates'].mean().reset_index()
        
        # 创建基础图形
        fig = go.Figure()
        
        # 定义颜色映射
        colors = {
            'Core London': '#2E86C1',    # 深蓝色
            'Outer London': '#F39C12',   # 橙色
            'Non-London': '#27AE60',     # 绿色
            'London Overall': '#3498DB'  # 浅蓝色
        }
        
        # 为每个区域类型添加折线
        for status in trend_data['London_Status'].unique():
            status_data = trend_data[trend_data['London_Status'] == status]
            
            fig.add_trace(go.Scatter(
                x=status_data['Year'],
                y=status_data['Recycling_Rates'],
                name=status,
                mode='lines+markers',
                line=dict(
                    color=colors.get(status, '#666666'),
                    width=2
                ),
                marker=dict(
                    size=8,
                    symbol='circle'
                ),
                hovertemplate=(
                    "<b>%{x}</b><br>" +
                    "Recycling Rate: %{y:.1f}%<br>" +
                    f"Region: {status}<extra></extra>"
                )
            ))
        
        # 更新布局
        fig.update_layout(
            title={
                'text': 'Recycling Rate Trends by Region Type',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24)
            },
            xaxis=dict(
                title='Year',
                gridcolor='rgba(0,0,0,0.1)',
                gridwidth=1,
                tickmode='linear',
                dtick=1,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title='Recycling Rate (%)',
                gridcolor='rgba(0,0,0,0.1)',
                gridwidth=1,
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='rgba(0,0,0,0.2)',
                tickfont=dict(size=12)
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=50, r=20, t=60, b=50)
        )
        
        return fig
    except Exception as e:
        print(f"Error in recycling_line_chart: {e}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        return {}

def recycling_scatter_plot(df):
    """创建人口密度与回收率的散点图"""
    try:
        fig = px.scatter(
            df,
            x='Population_Density',
            y='Recycling_Rates',
            color='London_Status',
            size='Population',
            hover_data=['Area'],
            title=f"Population Density vs Recycling Rate ({df['Year'].iloc[0]})",
            labels={
                'Population_Density': 'Population Density (per km²)',
                'Recycling_Rates': 'Recycling Rate (%)',
                'London_Status': 'Region Type',
                'Population': 'Population',
                'Area': 'Borough'
            }
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig
    except Exception as e:
        print(f"Error in recycling_scatter_plot: {e}")
        return {}

def recycling_bar_chart(df):
    """创建区域类型回收率柱状图"""
    try:
        # 计算各区域类型的平均回收率
        avg_rates = df.groupby('London_Status')['Recycling_Rates'].mean().reset_index()
        
        fig = go.Figure()
        
        colors = {
            'Core London': '#2E86C1',
            'Outer London': '#F39C12',
            'Non-London': '#27AE60'
        }
        
        for status in ['Core London', 'Outer London', 'Non-London']:
            rate = avg_rates[avg_rates['London_Status'] == status]['Recycling_Rates'].iloc[0]
            
            fig.add_trace(go.Bar(
                name=status,
                x=[status],
                y=[rate],
                text=[f'{rate:.1f}%'],
                textposition='auto',
                marker_color=colors[status]
            ))
        
        fig.update_layout(
            title=f'Average Recycling Rates by Region Type ({df["Year"].iloc[0]})',
            yaxis_title='Recycling Rate (%)',
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False
        )
        
        return fig
    except Exception as e:
        print(f"Error in recycling_bar_chart: {e}")
        return {}

def recycling_bar_chart_range(df, comparison_type):
    """创建区域范围对比柱状图"""
    try:
        if comparison_type == 'london_vs_non':
            # 伦敦与非伦敦对比
            london_data = df[df['London_Status'].isin(['Core London', 'Outer London'])]
            non_london_data = df[df['London_Status'] == 'Non-London']
            
            london_avg = london_data['Recycling_Rates'].mean()
            non_london_avg = non_london_data['Recycling_Rates'].mean()
            
            data = pd.DataFrame({
                'Region': ['London', 'Non-London'],
                'Rate': [london_avg, non_london_avg]
            })
            
        else:  # core_vs_outer
            # 核心伦敦与外伦敦对比
            data = df[df['London_Status'].isin(['Core London', 'Outer London'])].groupby('London_Status')['Recycling_Rates'].mean().reset_index()
            data.columns = ['Region', 'Rate']
        
        fig = px.bar(
            data,
            x='Region',
            y='Rate',
            text=data['Rate'].round(1).astype(str) + '%',
            title=f'Recycling Rate Comparison ({df["Year"].iloc[0]})'
        )
        
        fig.update_layout(
            yaxis_title='Recycling Rate (%)',
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False
        )
        
        return fig
    except Exception as e:
        print(f"Error in recycling_bar_chart_range: {e}")
        return {}

def recycling_borough_chart(df):
    """创建区域详细对比图"""
    try:
        # 只选择伦敦区域并按回收率排序
        london_data = df[df['London_Status'].isin(['Core London', 'Outer London'])].sort_values('Recycling_Rates', ascending=True)
        
        fig = go.Figure()
        
        colors = {
            'Core London': '#2E86C1',
            'Outer London': '#F39C12'
        }
        
        for status in ['Core London', 'Outer London']:
            status_data = london_data[london_data['London_Status'] == status]
            
            fig.add_trace(go.Bar(
                x=status_data['Recycling_Rates'],
                y=status_data['Area'],
                orientation='h',
                name=status,
                text=[f'{rate:.1f}%' for rate in status_data['Recycling_Rates']],
                textposition='auto',
                marker_color=colors[status]
            ))
        
        fig.update_layout(
            title=f'Recycling Rates by Borough in London ({df["Year"].iloc[0]})',
            xaxis_title='Recycling Rate (%)',
            yaxis_title='Borough',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    except Exception as e:
        print(f"Error in recycling_borough_chart: {e}")
        return {}

def recycling_data_table(df):
    """创建数据表格"""
    try:
        # 获取最新年份的数据
        latest_year = df['Year'].max()
        df_latest = df[df['Year'] == latest_year].copy()
        
        # 选择要显示的列并重命名
        columns_to_show = {
            'Area': 'Borough',
            'Year': 'Year',
            'Recycling_Rates': 'Recycling Rate (%)',
            'Population': 'Population',
            'Population_Density': 'Population Density',
            'London_Status': 'Region'
        }
        
        # 选择并重命名列
        df_display = df_latest[list(columns_to_show.keys())].rename(columns=columns_to_show)
        
        # 格式化数值
        df_display['Recycling Rate (%)'] = df_display['Recycling Rate (%)'].round(1)
        df_display['Population'] = df_display['Population'].apply(lambda x: f"{int(x):,}")
        df_display['Population Density'] = df_display['Population Density'].round(1)
        
        return dash_table.DataTable(
            id='analysis-data-table',
            columns=[{'name': col, 'id': col} for col in df_display.columns],
            data=df_display.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'fontSize': '14px'
            },
            style_header={
                'backgroundColor': '#f8f9fa',
                'fontWeight': 'bold'
            },
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            }],
            page_size=10,
            sort_action='native',
            filter_action='native'
        )
    except Exception as e:
        print(f"Error in recycling_data_table: {e}")
        return html.Div("Error creating data table", className="text-danger")

def create_uk_map():
    # 英国区域数据
    regions = [
        'NORTH WEST', 'YORKSHIRE', 'EAST MIDLANDS', 'WEST MIDLANDS',
        'EASTERN', 'LONDON', 'SOUTH EAST', 'SOUTH WEST', 'SOUTHERN'
    ]
    
    # 创建示例数据（你可以替换成实际数据）
    df = pd.DataFrame({
        'region': regions,
        'recycling_rate': [45, 42, 44, 43, 46, 48, 47, 41, 45]  # 示例回收率
    })
    
    # 创建地图
    fig = go.Figure()
    
    # 添加英国地图
    fig.add_trace(go.Choropleth(
        locations=df['region'],
        z=df['recycling_rate'],
        locationmode='country names',
        colorscale='Viridis',
        colorbar_title="Recycling Rate (%)",
        text=df['region'],
        hovertemplate="<b>%{text}</b><br>" +
                      "Recycling Rate: %{z}%<br>" +
                      "<extra></extra>",
    ))
    
    # 更新布局
    fig.update_layout(
        title_text='England Recycling Rates by Region',
        geo_scope='europe',  # 限制地图范围在欧洲
        geo=dict(
            center=dict(lon=-2, lat=54),  # 英国中心位置
            projection_scale=4.5,  # 缩放级别
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showcoastlines=True,
            coastlinecolor='rgb(80, 80, 80)',
            showframe=False,
            showcountries=True,
            countrycolor='rgb(80, 80, 80)',
            resolution=50
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=700
    )
    
    # 添加区域边界
    # 这里需要添加英国各区域的边界坐标
    # 可以使用 GeoJSON 数据或者手动添加边界线
    
    return fig

def add_region_boundaries(fig):
    """添加区域边界线"""
    # 这里可以添加区域边界线的坐标
    # 使用 fig.add_trace(go.Scattergeo()) 来画边界线
    pass

def create_borough_layout(borough_name=None, region=None, postcode=None):
    """创建区域数据展示布局"""
    return dbc.Container([
        # 顶部信息卡片
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"Borough: {borough_name or 'Select a Borough'}"),
                        dbc.Row([
                            dbc.Col(html.P(f"Region: {region or 'N/A'}"), width=6),
                            dbc.Col(html.P(f"PostCode: {postcode or 'N/A'}"), width=6),
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 主要回收率趋势图
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recycling Rate Trends"),
                    dbc.CardBody([
                        dcc.Graph(
                            id='recycling-trend',
                            config={'displayModeBar': True}
                        )
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 下方四个关键指标图表
        dbc.Row([
            # 人口变化
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Population Trends"),
                    dbc.CardBody(dcc.Graph(id='population-trend'))
                ])
            ], width=6),
            
            # 教育水平
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Educational Level"),
                    dbc.CardBody(dcc.Graph(id='education-trend'))
                ])
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            # 人口密度
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Population Density"),
                    dbc.CardBody(dcc.Graph(id='density-trend'))
                ])
            ], width=6),
            
            # 人均回收率
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Per Capita Recycling"),
                    dbc.CardBody(dcc.Graph(id='per-capita-trend'))
                ])
            ], width=6)
        ])
    ], fluid=True)