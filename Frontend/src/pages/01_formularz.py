import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dash
from dash import html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template="/formularz", name="Formularz")

def layout(**kwargs):
    return html.Div([
        dmc.Container(
            children=[
                dmc.Title("Zmienne", order=1, ta="center"),
                dmc.Text(
                    "Proszę opisać jak bardzo ci zależy na optymalizacji danej cechy.",
                    size="md",
                    ta="center",
                    mt="lg",
                    mb="xs"
                ),
                 dmc.Text(
                    "Wprowadź dane pacjenta, aby zapoznać się z przykładowymi cechami używanymi w predykcji.",
                    ta="center",
                    mb="md"
                ),

                dbc.Row([
                    dbc.Col(dmc.NumberInput(label="Koszt zużycia energii", value=0), width=4),
                    dbc.Col(dmc.NumberInput(label="Zużycie dwutlenku węgla", value=120), width=4),
                    dbc.Col(dmc.NumberInput(label="Komfort użytkowania", value=70), width=4),
                    dbc.Col(dmc.NumberInput(label="Niska awaryjność", value=20), width=4),
                    dbc.Col(dmc.NumberInput(label="Koszt urządzenia", value=80), width=4),
                    dbc.Col(dmc.NumberInput(label="Jakość użytkowania", value=30.0), width=4),
                ], className="mb-4"),
                dmc.Text(
                    "Aplikacja umożliwia eksplorację danych pacjentów, ocenę skuteczności klasyfikatorów oraz predykcję wystąpienia "
                    "cukrzycy typu 2 w oparciu o rzeczywiste cechy kliniczne. Wykorzystuje uczenie maszynowe, m.in. sieci neuronowe "
                    "z tunowaniem hiperparametrów oraz analizą ważności cech.",
                    size="sm",
                    ta="center",
                    mb="md",
                    style={"maxWidth": "700px", "margin": "auto"}
                ),
            ],
            style={"marginTop": "50px"}
        )
    ])
