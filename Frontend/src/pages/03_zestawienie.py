import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__, path_template="/zestawienie", name="Zestawienie")

def layout(**kwargs):
    return html.Div([
        dmc.Container([
            dmc.Title("Wpływ zmiennych na model", order=1, ta="center"),
            dmc.Text(
                "Na podstawie wytrenowanego modelu można analizować, które cechy wejściowe mają największy wpływ na końcową predykcję.",
                size="md",
                ta="center",
                mt="lg",
                mb="xs",
                style={"maxWidth": "800px", "margin": "auto"}
            ),
            dmc.Text(
                "W praktyce wykorzystuje się takie metody jak analiza gradientów, SHAP, LIME czy permutacje losowe, "
                "aby określić znaczenie poszczególnych zmiennych. W niniejszej aplikacji (w pełnej wersji) prezentowany jest wykres, "
                "który pokazuje względny wpływ zmiennych klinicznych, takich jak poziom glukozy, ciśnienie krwi, wiek i inne.",
                size="sm",
                ta="center",
                style={"maxWidth": "800px", "margin": "auto"}
            ),
        ], style={"marginTop": "50px"})
    ])
