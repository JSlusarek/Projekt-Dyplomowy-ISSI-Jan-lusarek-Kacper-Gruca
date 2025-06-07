import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join("../../")))

import pickle
import dash
from dash import html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate


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

        dcc.Location(id="redirect-check", refresh=True),
        dcc.Store(id="wizard-progress"),
        html.Div(id="redirect-dummy"),                  # redirect if necessary

        dbc.Container([
            dmc.Title("Profil użytkownika", order=1, ta="center"),
            dcc.Location(id="redirect", refresh=True),
            dcc.Store(id="user-input-store", storage_type="session"),

         

            #dmc.Center(
            #    dbc.Button("Uruchom profiler", id="run-interpretation-btn", n_clicks=0)
            #),

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
                                    #dbc.Button("Akceptuj rekomendowany profil", id="accept-main-profile", color="teal" ,className="me-2",style={"borderRadius": "12px"}),

                                    #dbc.Button("Wolę alternatywny profil", id="accept-alternative-profile", color="warning"),
                                    dbc.Button(
                                        "Wolę alternatywny profil",
                                        id="accept-alternative-profile",
                                        color="warning",  # zachowana funkcjonalność Dash
                                        className="me-2",
                                        style={
                                            "background": "linear-gradient(90deg, #f9d423, #ff4e00)",  # złoto → pomarańcz
                                            "border": "none",
                                            "color": "white",
                                            "fontWeight": "bold",
                                            "padding": "10px 24px",
                                            "borderRadius": "12px",
                                            "fontSize": "16px",
                                            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                            "textAlign": "center",
                                            "whiteSpace": "nowrap",
                                            "transition": "0.3s",
                                        }
                                    ),
                                    
                                    dbc.Button(
                                        "Wybierz rekomendowany profil",
                                        id="accept-main-profile",
                                        color="teal",  # wymagany, ale i tak go nadpisujemy stylem
                                        className="me-2",
                                        style={
                                            "background": "linear-gradient(90deg, #00c96b, #007bff)",  # gradient z zieleni do niebieskiego
                                            "border": "none",               # bez ramki
                                            "color": "white",               # biały tekst
                                            "fontWeight": "bold",           # pogrubienie
                                            "padding": "10px 24px",         # wewnętrzne marginesy
                                            "borderRadius": "12px",         # zaokrąglenie rogów
                                            "fontSize": "16px",             # rozmiar czcionki
                                            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",  # lekki cień
                                            "textAlign": "center",          # wyśrodkowanie tekstu
                                            "whiteSpace": "nowrap",         # zapobiega łamaniu się tekstu
                                            "transition": "0.3s",           # płynne efekty hovera
                                        }
                                    )
                                ]),
                                dmc.Space(h=20),
                                dmc.Center(
                                    dmc.Text(id="confirmation-output", size="lg", fw="500", c="green")
                                ),
                                dmc.Center(
                                    dmc.Text(id="profile-warning", size="md", c="red"),
                                    style={"marginBottom": "10px"}
                                ),
                                dmc.Center(
                                    dbc.Button("Przejdź dalej", id="go-to-summary", color="teal",n_clicks=0,disabled=True,
                                    style={
                                    "backgroundColor": "#00c96b",         # ten sam odcień zieleni
                                    "border": "none",
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "padding": "10px 24px",
                                    "borderRadius": "8px",               # lekko zaokrąglone rogi
                                    "fontSize": "16px",
                                    "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                                    "textAlign": "center",
                                    "whiteSpace": "nowrap",
                                    "transition": "0.3s",
                                })
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
            ], withBorder=True, shadow="xs", p="md", mt=30)], style={"marginTop": "30px", "maxWidth": "1200px"})
    ])
@callback(
    Output("interpretation-output", "children"),
    Output("user-profiles-store", "data"),
    Output("profiler-ran-flag", "data"),
    Input("user-input-store", "data"),
    prevent_initial_call=True
)
def run_interpretation(user_input):
    if not user_input:
        raise PreventUpdate

    try:
        with open("../../models/feature_order_user_profile_model.pkl", "rb") as f:
            feature_order = pickle.load(f)

        with open("../../models/user_profile_model.pkl", "rb") as f:
            model = pickle.load(f)

        profiles = predict_profile_for_user(
            user_input=user_input,
            model=model,
            feature_order=feature_order,
        )

        recommendation = (
            f"**Rekomendowany profil:** `{profiles[0]}`  \n"
            f"**Alternatywny profil:** `{profiles[1]}`  \n\n"
        )

        interpretation = recommendation + interpret_prediction_with_gemini(
            user_input,
            predicted_profiles=profiles
        )

        return interpretation, {
            "user_input": user_input,
            "profile_first": profiles[0],
            "profile_second": profiles[1]
        }, True

    except Exception as e:
        # fallback: same profile, bez AI
        interpretation = (
            f"**Rekomendowany profil:** `Brak danych`  \n"
            f"**Alternatywny profil:** `Brak danych`  \n\n"
            f"Upss, nie mogliśmy się połączyć z AI"
        )
        return interpretation, dash.no_update, False


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

@callback(
    Output("redirect-check", "pathname"),
    Input("wizard-progress", "data"),
    prevent_initial_call=True
)

def check_access(progress):
    if not progress.get("step_1_done"):
        return "/formularz"
    raise dash.exceptions.PreventUpdate


@callback(
    Output("wizard-progress", "data", allow_duplicate=True),
    Output("redirect-check", "pathname", allow_duplicate=True),
    Output("profile-warning", "children"),  # nowy output!
    Input("go-to-summary", "n_clicks"),
    State("wizard-progress", "data"),
    State("user-profile-selection", "data"),
    prevent_initial_call=True
)
def go_to_summary(n, progress, profile_selected):
    if not n:
        raise dash.exceptions.PreventUpdate

    if not profile_selected:
        return dash.no_update, dash.no_update, "⚠️ Proszę wybrać profil przed kontynuacją."

    if progress is None:
        progress = {}

    progress["step_2_done"] = True
    return progress, "/zestawienie", ""




@callback(
    Output("go-to-summary", "disabled"),
    Input("user-profile-selection", "data")
)
def enable_summary_button(profile):
    return not bool(profile)  # przycisk aktywny tylko jeśli coś wybrano
