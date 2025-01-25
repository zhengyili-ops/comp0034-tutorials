import pandas as pd
import plotly.express as px
from pathlib import Path
import sqlite3

# 使用pathlib构建绝对路径
current_dir = Path(__file__).parent
CSV_PATH = current_dir.parent.parent / "tutor" / "data" / "paralympics.csv"

def line_chart(feature, types=None):
    """
    Create a line chart showing the trend for the selected feature over time.
    
    Args:
        feature: str, the feature to plot (sports, participants, events, countries)
        types: list, the types to include (summer, winter)
    """
    # 验证参数
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    
    # 读取数据
    db_path = current_dir.parent.parent / "tutor" / "data" / "paralympics.db"
    connection = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM paralympics_data", connection)  # 从数据库读取数据
    
    # 如果指定了类型，就过滤数据
    if types and len(types) > 0:
        df = df[df['type'].isin(types)]
    
    # 创建图表
    fig = px.line(
        df,
        x="year",
        y=feature.lower(),
        color="type",  # 区分夏季和冬季
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
    """
    Creates a stacked bar chart showing change in the ratio of male and female competitors.
    
    Parameters:
    event_type: str Winter or Summer
    
    Returns:
    fig: Plotly Express bar chart
    """
    # 读取需要的列
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']
    df_events = pd.read_csv(CSV_PATH, usecols=cols)
    
    # 打印一下数据检查
    print("Unique types in data:", df_events['type'].unique())
    
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
    
    # 打印筛选后的数据检查
    print(f"Number of rows for {event_type}:", len(df_filtered))
    
    if len(df_filtered) == 0:
        print(f"No data found for event type: {event_type}")
        return px.bar(title="No data available")
        
    fig = px.bar(df_filtered,
                 x='xlabel',
                 y=['Male', 'Female'],
                 title=f'How has the ratio of female:male participants changed in {event_type.capitalize()} paralympics?',
                 labels={'xlabel': '', 'value': 'Ratio', 'variable': 'Gender'},
                 template="simple_white",
                 color_discrete_map={'Male': 'blue', 'Female': 'green'}  # 自定义颜色
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
                        # 可选：添加标记样式
                        color_discrete_sequence=['#1f77b4'],  # 标记颜色
                        size_max=15,  # 标记最大尺寸
                        )
    
    # 可选：更新地图样式
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="RebeccaPurple",
        showland=True,
        landcolor="LightGray",
        showocean=True,
        oceancolor="LightBlue"
    )
    
    return fig