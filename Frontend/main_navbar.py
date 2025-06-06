import dash_bootstrap_components as dbc
from dash import Dash, html

App_logo = "assets/Logo_aplikacji.png"

def render(app: Dash) -> dbc.NavbarSimple:
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Start", href="/")),
        ],
        color="#e0f4f1",#f0fdfa
        dark=False,
        expand=True,
        brand=html.Div([
            html.Img(src=App_logo, height="120px", style={"marginRight": "10px"}),
            html.Span("Home Appliance Profiling System", style={
                "fontSize": "22px",
                "fontWeight": "bold",
                "color": "#003f5c",
                "fontFamily": "Inter, Roboto, sans-serif"
            }),
        ], style={"display": "flex", "alignItems": "center"}),
        brand_style={"marginLeft": "10px"},
    )
