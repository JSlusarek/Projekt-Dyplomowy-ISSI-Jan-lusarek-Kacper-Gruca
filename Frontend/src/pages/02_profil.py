import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

dash.register_page(__name__, path_template="/profil", name="Profil")

def layout(**kwargs):
    return html.Div([
        dbc.Container(
            children=[
                dmc.Title("Model predykcyjny", order=1, ta="center"),
                dmc.Text(
                    "Wprowadź dane pacjenta, aby zapoznać się z przykładowymi cechami używanymi w predykcji.",
                    ta="center",
                    mb="md"
                ),

            
                dmc.Center(
                    dmc.Text(
                        "W tej wersji strony predykcja została wyłączona. Dane służą tylko do prezentacji formularza.",
                        size="sm",
                        c="gray"
                    )
                )
            ],
            style={"marginTop": "30px", "maxWidth": "800px"}
        )
    ])
