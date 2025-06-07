import sys
import os
import pickle
import html
import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc

sys.path.append(os.path.abspath(os.path.join("../../")))

from components.spider_chart import generate_spider_chart
from components.plot_all_metrics_for_category_plotly import plot_all_metrics_for_category_plotly

dash.register_page(__name__, path_template="/zestawienie", name="Zestawienie")

# === Wczytaj dane tylko raz ===
with open("../../src/recommendation_engine/pickles/combined_df.pkl", "rb") as f:
    combined_df = pickle.load(f)

with open("../../src/recommendation_engine/pickles/appliance_recommendations_for_profiles.pkl", "rb") as f:
    appliance_recommendations_for_profiles = pickle.load(f)

# === Layout strony ===
def layout(**kwargs):
    return html.Div([
        dmc.Container([
            dcc.Store(id="user-profile-selection", storage_type="session"),

            dmc.Title("Zestawienie Urządzeń", order=1, ta="center"),

            html.Div(id="spider-chart-container", style={"marginTop": "40px"}),

            html.Div(id="zestawienie-wykresy", style={"marginTop": "50px"})
        ])
    ])


@callback(
    Output("spider-chart-container", "children"),
    Input("user-profile-selection", "data")
)
def update_spider_chart(selected_profile):
    if selected_profile is None:
        return dmc.Text("⚠️ Brak wybranego profilu – wykres radarowy niedostępny.", c="red")

    fig = generate_spider_chart("../../Data/GRID/grid_with_profiles.parquet", profile=selected_profile)
    fig.update_layout(
        paper_bgcolor="#f0fdfa",
        plot_bgcolor="#f0fdfa",
        height=500,
        margin=dict(t=60, b=60)
    )

    return html.Div(
        dcc.Graph(figure=fig),
        style={
            "width": "100%",
            "maxWidth": "1200px",
            "margin": "0 auto"
        }
    )

@callback(
    Output("zestawienie-wykresy", "children"),
    Input("user-profile-selection", "data")
)
def update_zestawienie_wykresy(selected_profile):
    print("Wybrany profil:", selected_profile)

    if selected_profile is None:
        return dmc.Text("⚠️ Nie wybrano profilu użytkownika.", c="red")

    figures = plot_all_metrics_for_category_plotly(
        combined_df,
        profile=selected_profile,
        appliance_recommendations_for_profiles=appliance_recommendations_for_profiles,
        show=False
    )

    # Ustawiamy styl zgodny z kolorem tła
    background_color = "#f0fdfa"

    # Dopasuj tło do stylu strony
    return [
        html.Div(
            dcc.Graph(
                figure=fig.update_layout(
                    paper_bgcolor=background_color,
                    plot_bgcolor=background_color,
                    margin=dict(t=60, b=60),
                    height=400
                )
            ),
            style={
                "width": "100%",
                "maxWidth": "1200px",
                "margin": "0 auto 50px auto"
            }
        )
        for fig in figures
    ]

