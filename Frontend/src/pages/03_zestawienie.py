import sys
import os
sys.path.append(os.path.abspath(os.path.join("../../")))

import dash
from dash import html, dcc
import dash_mantine_components as dmc
from components.spider_chart import generate_spider_chart

dash.register_page(__name__, path_template="/zestawienie", name="Zestawienie")

def layout(**kwargs):
    fig = generate_spider_chart("../../Data/GRID/grid_with_profiles.parquet")

    return html.Div([
        dmc.Container([
            dmc.Title("Zestawienie Urządzeń", order=1, ta="center"),
        
        dcc.Graph(figure=fig, style={"marginTop": "40px"})
        ], style={"marginTop": "50px"})
    ])
