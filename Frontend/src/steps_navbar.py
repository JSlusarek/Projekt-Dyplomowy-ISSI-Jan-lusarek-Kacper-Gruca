from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Dash
from dash import callback, Output, Input
import dash

def step_link(number, label, href, is_current=False, is_done=False, disabled=False):
    # Kolorystyka
    if is_current:
        border_color = "#2f9e44"
        bg_color = "#d3f9d8"
        opacity = "1"
    elif is_done:
        border_color = "#2f9e44"
        bg_color = "#d3f9d8"
        opacity = "0.5"
    else:
        border_color = "#ced4da"
        bg_color = "#f8f9fa"
        opacity = "0.5"

    circle_color = border_color
    text_color = "#000"
    cursor = "pointer" if not disabled else "not-allowed"
    final_href = href if not disabled else None

    return html.A(
        html.Div([
            html.Div(str(number), style={
                "width": "30px",
                "height": "30px",
                "borderRadius": "50%",
                "backgroundColor": circle_color,
                "color": "white",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "fontWeight": "bold",
                "marginRight": "8px"
            }),
            html.Span(label, style={
                "color": text_color,
                "fontWeight": "600" if is_current else "500",
                "fontSize": "15px"
            })
        ],
            style={
                "display": "flex",
                "alignItems": "center",
                "padding": "10px 20px",
                "border": f"2px solid {border_color}",
                "borderRadius": "12px",
                "marginRight": "10px",
                "backgroundColor": bg_color,
                "textDecoration": "none",
                "opacity": opacity,
                "cursor": cursor
            }
        ),
        href=final_href,
        style={"textDecoration": "none"}
    )

def render(current_path, progress):

    if progress is None:
        progress={}

    print(">>> current_path:", current_path)


    steps = [
        {"number": 1, "label": "Formularz", "href": "/formularz"},
        {"number": 2, "label": "Przypisanie profilu", "href": "/profil"},
        {"number": 3, "label": "Zestawienie urządzeń", "href": "/zestawienie"},
    ]

    current_index = next((i for i, step in enumerate(steps) if current_path.startswith(step["href"])), 0)

    return html.Div([
        html.Div([
            step_link(
                number=step["number"],
                label=step["label"],
                href=step["href"],
                is_current=(i == current_index),
                is_done=(i < current_index),
                disabled=(i > current_index and not progress.get(f"step_{i}_done", False))
            )
            for i, step in enumerate(steps)
        ], style={
            "display": "flex",
            "justifyContent": "center",
            "marginTop": "30px",
            "marginBottom": "20px"
        })
    ])
