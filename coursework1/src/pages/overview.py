from dash import register_page, html
import dash_bootstrap_components as dbc

register_page(__name__, path='/', name='Overview')

layout = dbc.Container([
    # 主标题和副标题
    html.H1("London Waste Management Analysis", 
            className="text-center my-4"),
    html.P("Explore recycling and waste management data across London boroughs and surrounding areas.",
           className="text-center mb-5"),
    
    # 两个主要分析模块的卡片
    dbc.Row([
        # 回收分析卡片
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2("Recycling Analysis", className="card-title h3"),
                    html.P("Analyze recycling rates and trends across different regions.",
                          className="card-text"),
                    dbc.Button("Explore Recycling", 
                             href="/recycling/overview",
                             color="primary",
                             className="mt-3")
                ])
            ], className="h-100")
        ], width=12, lg=6, className="mb-4"),
        
        # 废物管理卡片
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2("Waste Management", className="card-title h3"),
                    html.P("Investigate waste collection and disposal patterns.",
                          className="card-text"),
                    dbc.Button("Explore Waste",
                             href="/waste/overview",
                             color="primary",
                             className="mt-3")
                ])
            ], className="h-100")
        ], width=12, lg=6, className="mb-4")
    ]),
    
    # 关键统计部分
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Key Statistics"),
                dbc.CardBody([
                    # 这里可以添加一些关键统计数据
                    html.Div(id="key-stats")
                ])
            ])
        ])
    ])
], fluid=True, className="px-4") 