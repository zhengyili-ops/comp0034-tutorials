from dash import Dash, html, dash, page_registry, page_container
import dash_bootstrap_components as dbc

# 设置 meta tags 和样式表
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]
external_stylesheets = [dbc.themes.BOOTSTRAP]

# 创建应用，启用多页面功能
app = Dash(__name__, 
          external_stylesheets=external_stylesheets, 
          meta_tags=meta_tags,
          use_pages=True)

# 创建导航栏
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Event Details", href="/events")),  # 简化路径
        dbc.NavItem(dbc.NavLink("Charts", href="/charts")),  # 简化路径
    ],
    brand="Paralympics Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)

# 定义应用布局
app.layout = dbc.Container([
    navbar,  # 导航栏
    page_container  # 使用导入的 page_container
])

if __name__ == '__main__':
    app.run(debug=True, port=5050)