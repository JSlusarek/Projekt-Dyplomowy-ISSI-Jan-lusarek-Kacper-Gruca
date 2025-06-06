from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Dash
from dash import callback, Output, Input
import dash


#dash.register_page(__name__, path="/")  

def step_link(number, label, href, active=False):
    color = "#c92a2a" if active else "#ced4da"
    bg = "#fff" if active else "#f8f9fa"
    text_color = "#000" if active else "#495057"

    return html.A(
        html.Div([
            html.Div(str(number), style={
                "width": "30px",
                "height": "30px",
                "borderRadius": "50%",
                "backgroundColor": color,
                "color": "white",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "fontWeight": "bold",
                "marginRight": "8px"
            }),
            html.Span(label, style={"color": text_color, "fontWeight": "500"})
        ],
            style={
                "display": "flex",
                "alignItems": "center",
                "padding": "10px 20px",
                "border": f"2px solid {color}",
                "borderRadius": "12px",
                "marginRight": "10px",
                "backgroundColor": bg,
                "textDecoration": "none"
            }
        ),
        href=href,
        style={"textDecoration": "none"}
    )


def render(current_path):
    return html.Div([
        html.Div([
            step_link(1, "Formularz", "/formularz", active=(current_path == "/formularz")),
            step_link(2, "Przypisanie profilu", "/profil", active=(current_path == "/profil")),
            step_link(3, "Zestawienie urządzeń", "/zestawienie", active=(current_path == "/zestawienie")),
        ], style={
            "display": "flex",
            "justifyContent": "center",
            "marginTop": "30px",
            "marginBottom": "20px"
        })
    ])
