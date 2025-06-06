import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join("../../")))

import pickle
import dash
from dash import html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from src.recommendation_engine.predict_profile_for_user import predict_profile_for_user
from src.ai_answer_engine.gemini_model_answer import (
    load_api_key,
    configure_gemini_client,
    interpret_prediction_with_gemini
)


configure_gemini_client(load_api_key())


dash.register_page(__name__, path_template="/profil", name="Profil")

with open("assets/profil_legend.md", "r", encoding="utf-8") as f:
    legend_markdown = f.read()


def layout(**kwargs):
    return html.Div([
        dbc.Container([
            dmc.Title("Profil użytkownika", order=1, ta="center"),
         

            dmc.Center(
                dbc.Button("Uruchom profiler", id="run-interpretation-btn", n_clicks=0)
            ),

            dcc.Store(id="user-profiles-store"),
            dcc.Store(id="profiler-ran-flag", data=False),
            dcc.Store(id="user-profile-selection"),

            dmc.Space(h=20),

            dmc.Center(
                dcc.Loading(
                    children=dmc.Paper([
                        dcc.Markdown(
                            id="interpretation-output",
                            style={
                                "whiteSpace": "pre-wrap",
                                "width": "100%",
                                "maxWidth": "1000px"
                            }
                        ),
                        html.Div(
                            id="profile-choice-buttons",
                            children=[
                                dmc.Center([
                                    dbc.Button("Akceptuj rekomendowany profil", id="accept-main-profile", color="success", className="me-2"),
                                    dbc.Button("Wolę alternatywny profil", id="accept-alternative-profile", color="warning"),
                                ]),
                                dmc.Space(h=20),
                                dmc.Center(
                                    dmc.Text(id="confirmation-output", size="lg", fw="500", c="green")
                                )
                            ],
                            style={"display": "none"}
                        )
                    ], shadow="sm", p="md", radius="md"),
                    type="default"
                )
            ),
           dmc.Paper([
                dcc.Markdown(legend_markdown, style={"whiteSpace": "pre-wrap"})
            ], withBorder=True, shadow="xs", p="md", mt=30),
            dmc.Text(
                "Wkliknij na poniższy przycisk by przypisać swój profil użytkownika.",
                ta="center", mb="md"
            )], style={"marginTop": "30px", "maxWidth": "1200px"})
    ])

@callback(
    Output("interpretation-output", "children"),
    Output("user-profiles-store", "data"),
    Output("profiler-ran-flag", "data"),
    Input("run-interpretation-btn", "n_clicks"),
    prevent_initial_call=True
)
def run_interpretation(n_clicks):
    try:
        with open("../../models/feature_order_user_profile_model.pkl", "rb") as f:
            feature_order = pickle.load(f)
        with open("user_input.json", "r") as f:
            user_input = json.load(f)
        with open("../../models/user_profile_model.pkl", "rb") as f:
            model = pickle.load(f)

        profiles = predict_profile_for_user(
            user_input=user_input,
            model=model,
            feature_order=feature_order,
        )
        
        interpretation = interpret_prediction_with_gemini(user_input, predicted_profiles=profiles)

        return interpretation, {
            "user_input": user_input,
            "profile_first": profiles[0],
            "profile_second": profiles[1]
        }, True

    except Exception as e:
        return f"Błąd podczas generowania interpretacji: {str(e)}", dash.no_update, False

@callback(
    Output("profile-choice-buttons", "style"),
    Input("profiler-ran-flag", "data")
)
def toggle_profile_buttons_visible(ran):
    return {"display": "block"} if ran else {"display": "none"}


@callback(
    Output("user-profile-selection", "data"),
    Output("confirmation-output", "children"),
    Input("accept-main-profile", "n_clicks"),
    Input("accept-alternative-profile", "n_clicks"),
    State("user-profiles-store", "data"),
    prevent_initial_call=True
)
def handle_user_selection(n_main, n_alt, profiles_data):
    triggered = ctx.triggered_id

    if not profiles_data:
        return dash.no_update, "Najpierw uruchom profiler."

    if triggered == "accept-main-profile":
        with open("profil.json", "w", encoding="utf-8") as f:
            json.dump(profiles_data["profile_first"], f)
        return profiles_data["profile_first"], f"Wybrałeś profil: **{profiles_data['profile_first']}**"

    elif triggered == "accept-alternative-profile":
        with open("profil.json", "w", encoding="utf-8") as f:
            json.dump(profiles_data["profile_second"], f)
        return profiles_data["profile_second"], f" Wybrałeś alternatywny profil: **{profiles_data['profile_second']}**"

    return dash.no_update, ""
