import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))  # 添加项目根目录到路径

from dash import Dash, html, dcc, page_container
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# 创建应用实例
app = Dash(__name__, 
           use_pages=True,  # 启用多页面功能
           external_stylesheets=[dbc.themes.BOOTSTRAP])

# 创建导航栏
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Charts", href="/charts")),
        dbc.NavItem(dbc.NavLink("Events", href="/events")),
    ],
    brand="Paralympics Analysis",
    brand_href="/",
    color="primary",
    dark=True,
)

# 定义应用布局
app.layout = html.Div([
    navbar,
    dash.page_container  # 页面内容容器
])

if __name__ == '__main__':
    app.run(debug=True, port=5050)