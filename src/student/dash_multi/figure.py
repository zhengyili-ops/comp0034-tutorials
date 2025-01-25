import pandas as pd
import plotly.express as px
from pathlib import Path
import sqlite3
import dash
import dash_bootstrap_components as dbc
from dash import html

current_dir = Path(__file__).parent
CSV_PATH = current_dir.parent.parent / "tutor" / "data" / "paralympics.csv"

def line_chart(feature, types=None):
    """
    Create a line chart showing the trend for the selected feature over time.
    
    Args:
        feature: str, the feature to plot
        types: list, the types to include (summer, winter)
    """
    # 验证参数
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    
    # 读取数据
    df = pd.read_csv(CSV_PATH)
    
    # 如果指定了类型，就过滤数据
    if types and len(types) > 0:
        df = df[df['type'].isin(types)]
    
    # 创建图表
    fig = px.line(
        df,
        x="year",
        y=feature.lower(),
        color="type",
        title=f"How has the number of {feature} changed over time?",
        labels={
            feature.lower(): feature.capitalize(),
            "year": "Year",
            "type": "Games Type"
        },
        template="simple_white"
    )
    
    return fig

def bar_gender(event_type):
    """Creates a stacked bar chart showing change in the ratio of male and female competitors."""
    # 读取需要的列
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']
    df_events = pd.read_csv(CSV_PATH, usecols=cols)
    
    # 数据清理和准备
    df_events = df_events.dropna(subset=['participants_m', 'participants_f'])
    df_events.reset_index(drop=True, inplace=True)
    
    # 计算男女比例
    df_events['Male'] = df_events['participants_m'] / df_events['participants']
    df_events['Female'] = df_events['participants_f'] / df_events['participants']
    
    # 排序并创建x轴标签
    df_events.sort_values(['type', 'year'], ascending=(True, True), inplace=True)
    df_events['xlabel'] = df_events['host'] + ' ' + df_events['year'].astype(str)
    
    # 使用小写来匹配数据
    event_type = event_type.lower()
    
    # 筛选数据并创建图表
    df_filtered = df_events.loc[df_events['type'] == event_type]
    
    if len(df_filtered) == 0:
        return px.bar(title="No data available")
        
    fig = px.bar(df_filtered,
                 x='xlabel',
                 y=['Male', 'Female'],
                 title=f'How has the ratio of female:male participants changed in {event_type.capitalize()} paralympics?',
                 labels={'xlabel': '', 'value': 'Ratio', 'variable': 'Gender'},
                 template="simple_white",
                 color_discrete_map={'Male': 'blue', 'Female': 'green'}
                 )
    
    # 更新坐标轴
    fig.update_xaxes(ticklen=0)
    fig.update_yaxes(tickformat=".0%")
    
    return fig

def scatter_geo():
    """Creates a world map showing the locations of Paralympic games."""
    # 构建数据库文件路径
    db_path = current_dir.parent.parent / "tutor" / "data" / "paralympics.db"
    
    # 创建数据库连接
    connection = sqlite3.connect(db_path)

    # 定义SQL查询
    sql = '''
    SELECT event.year, host.host, host.latitude, host.longitude FROM event
    JOIN host_event ON event.event_id = host_event.event_id
    JOIN host on host_event.host_id = host.host_id
    '''
    
    # 使用pandas读取SQL查询结果
    df_locs = pd.read_sql(sql=sql, con=connection, index_col=None)
    
    # 将经纬度转换为浮点数
    df_locs['longitude'] = df_locs['longitude'].astype(float)
    df_locs['latitude'] = df_locs['latitude'].astype(float)
    
    # 添加地点和年份的组合列
    df_locs['name'] = df_locs['host'] + ' ' + df_locs['year'].astype(str)
    
    # 创建地图
    fig = px.scatter_geo(df_locs,
                        lat=df_locs.latitude,
                        lon=df_locs.longitude,
                        hover_name=df_locs.name,
                        title="Where have the Paralympics been held?",
                        color_discrete_sequence=['#1f77b4'],
                        size_max=15
                        )
    
    # 更新地图样式
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="RebeccaPurple",
        showland=True,
        landcolor="LightGray",
        showocean=True,
        oceancolor="LightBlue"
    )
    
    return fig 

def get_event_details(host, year):
    """Get the details for a specific Paralympic event."""
    # 读取数据
    df = pd.read_csv(CSV_PATH)
    
    # 查找特定事件的数据
    event_data = df[(df['host'] == host) & (df['year'] == year)].iloc[0]
    
    return {
        'participants': event_data['participants'],
        'events': event_data['events'],
        'countries': event_data['countries'],
        'sports': event_data['sports']
    } 

def create_card(host_year):
    """
    Generate a card for the event specified by host city name and year.

    Parameters:
        host_year: str  String with the host city name followed by a space then the year

    Returns:
        card: dash bootstrap components card for the event
    """
    # 分割主办城市和年份
    host, year = host_year.rsplit(' ', 1)
    year = int(year)
    
    # 读取数据
    df = pd.read_csv(CSV_PATH)
    
    # 获取特定事件的数据
    event_data = df[(df['host'] == host) & (df['year'] == year)].iloc[0]
    
    # 准备卡片内容
    logo_path = f'logos/{year}_{host}.jpg'
    participants = f"Number of athletes: {event_data['participants']}"
    events = f"Number of events: {event_data['events']}"
    countries = f"Number of countries: {event_data['countries']}"
    sports = f"Number of sports: {event_data['sports']}"
    
    card = dbc.Card([
        dbc.CardImg(
            src=dash.get_asset_url(logo_path),
            style={'max-width': '200px'},
            top=True
        ),
        dbc.CardBody([
            html.H4(host_year, className="card-title"),
            html.P(participants, className="card-text"),
            html.P(events, className="card-text"),
            html.P(countries, className="card-text"),
            html.P(sports, className="card-text"),
        ]),
    ],
        style={"width": "18rem"},
    )
    return card 

def create_bubble_chart():
    """Creates a bubble chart showing participants vs events, with bubble size representing countries."""
    # 读取数据
    df = pd.read_csv(CSV_PATH)
    
    # 创建气泡图
    fig = px.scatter(df, 
                    x="events", 
                    y="participants",
                    size="countries",  # 气泡大小代表参赛国家数
                    color="type",      # 颜色区分夏季和冬季
                    hover_name="host", # 悬停显示主办城市
                    text="year",       # 显示年份
                    title="Paralympics Growth: Events vs Participants",
                    labels={
                        "events": "Number of Events",
                        "participants": "Number of Participants",
                        "type": "Games Type"
                    })
    
    # 更新布局
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=True)
    
    return fig

def create_data_table():
    """Creates a table showing key statistics for each Paralympic Games."""
    # 读取数据
    df = pd.read_csv(CSV_PATH)
    
    # 选择要显示的列并重命名
    table_df = df[[
        'year', 'host', 'type', 
        'participants', 'events', 
        'countries', 'sports'
    ]].rename(columns={
        'year': 'Year',
        'host': 'Host City',
        'type': 'Type',
        'participants': 'Athletes',
        'events': 'Events',
        'countries': 'Countries',
        'sports': 'Sports'
    })
    
    # 按年份排序
    table_df = table_df.sort_values('Year', ascending=False)
    
    # 创建表格
    table = dash.dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in table_df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'minWidth': '100px'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        page_size=10,  # 每页显示10行
        sort_action='native',  # 启用排序
        filter_action='native'  # 启用筛选
    )
    
    return table 