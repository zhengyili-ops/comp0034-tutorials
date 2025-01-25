import dash
from dash import html
import dash_bootstrap_components as dbc
from pathlib import Path
import os

print("\n=== Initializing Dash App ===")

# 设置页面文件夹路径
PAGES_FOLDER = os.path.join(os.path.dirname(__file__), "pages")

app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder=PAGES_FOLDER,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v5.8.1/css/all.css'
    ],
    assets_folder=Path(__file__).parent / 'assets',
    suppress_callback_exceptions=True
)

# 验证页面注册
print("\n=== Registered Pages ===")
for page in dash.page_registry.values():
    print(f"Page: {page['name']}, Path: {page['path']}")

# 创建导航栏
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Overview", href="/recycling"),
                dbc.DropdownMenuItem("Area Analysis", href="/recycling/area"),
                dbc.DropdownMenuItem("Time Analysis", href="/recycling/time"),
                dbc.DropdownMenuItem("Population Impact", href="/recycling/population"),
            ],
            nav=True,
            label="Recycling Analysis",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Overview", href="/reuse"),
                dbc.DropdownMenuItem("Facility Analysis", href="/reuse/facility"),
                dbc.DropdownMenuItem("Organization Impact", href="/reuse/organization"),
                dbc.DropdownMenuItem("Charity Shops", href="/reuse/charity"),
            ],
            nav=True,
            label="Reuse Analysis",
        ),
    ],
    brand="London Recycling & Reuse Analytics",
    color="primary",
    dark=True,
)

# 应用布局
app.layout = html.Div([
    navbar,
    html.Div(dash.page_container, id='page-content')
])

print("\n=== App Layout Created ===")

if __name__ == "__main__":
    print("\n=== Starting Server ===")
    app.run(debug=True) 