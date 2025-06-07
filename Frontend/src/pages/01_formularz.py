import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dash
from dash import html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, State, ctx, dcc, no_update
from dash.exceptions import PreventUpdate


dash.register_page(__name__, path_template="/formularz", name="Formularz")

def layout(**kwargs):
    return html.Div([

        #dcc.Location(id="url", refresh=False),
        dcc.Location(id="redirect", refresh=True),
        dcc.Store(id="user-input-store", storage_type="session"),
        dmc.Container([
            dmc.Title("Zmienne", order=1, ta="center"),

            dmc.Text(
                "Wybierz jak bardzo zależy Ci na wymienionych cechach",
                size="md",
                ta="center",
                mt="lg",
                mb="xl"
            ),

            # ------------------ Obowiązkowe cechy ------------------
            dbc.Row([
                dbc.Col(dmc.Text("Koszt zużycia energii"), width=3),
                dbc.Col(html.Div(), width=1),
                dbc.Col(dmc.Slider(
                    id="cost_pln",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dbc.Row([
                dbc.Col(dmc.Text("Zużycie dwutlenku węgla"), width=3),
                dbc.Col(html.Div(), width=1),
                dbc.Col(dmc.Slider(
                    id="co2_emission_kg",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dbc.Row([
                dbc.Col(dmc.Text("Komfort użytkowania"), width=3),
                dbc.Col(html.Div(), width=1),
                dbc.Col(dmc.Slider(
                    id="normalized_comfort",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dbc.Row([
                dbc.Col(dmc.Text("Niska awaryjność"), width=3),
                dbc.Col(html.Div(), width=1),
                dbc.Col(dmc.Slider(
                    id="normalized_failure_rate",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dbc.Row([
                dbc.Col(dmc.Text("Koszt urządzenia"), width=3),
                dbc.Col(html.Div(), width=1),
                dbc.Col(dmc.Slider(
                    id="device_cost",
                    min=-10,
                    max=10,
                    step=1,
                    value=0,
                    marks=[{"value": i, "label": str(i)} for i in range(-10, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dmc.Divider(label="(Opcjonalne cechy)", labelPosition="center", my="lg"),

            # ------------------ Opcjonalne cechy ------------------

            dbc.Row([
                dbc.Col(dmc.Text("Jakość grzania"), width=3),
                dbc.Col(dmc.Center(dmc.Switch(id="heating_quality_enabled", checked=False, size="sm")), width=1),
                dbc.Col(dmc.Slider(
                    id="heating_quality",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    disabled=True,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dbc.Row([
                dbc.Col(dmc.Text("Jakość gotowania"), width=3),
                dbc.Col(dmc.Center(dmc.Switch(id="cooking_quality_enabled", checked=False, size="sm")), width=1),
                dbc.Col(dmc.Slider(
                    id="cooking_quality",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    disabled=True,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dbc.Row([
                dbc.Col(dmc.Text("Jakość obliczeń komputera"), width=3),
                dbc.Col(dmc.Center(dmc.Switch(id="computing_quality_enabled", checked=False, size="sm")), width=1),
                dbc.Col(dmc.Slider(
                    id="computing_quality",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    disabled=True,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dbc.Row([
                dbc.Col(dmc.Text("Jakość chłodzenia"), width=3),
                dbc.Col(dmc.Center(dmc.Switch(id="cooling_quality_enabled", checked=False, size="sm")), width=1),
                dbc.Col(dmc.Slider(
                    id="cooling_quality",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    disabled=True,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 11, 2)],
                    color="indigo",
                    radius="xl",
                    size="sm"
                ), width=6)
            ], align="center", className="mb-3"),

            dmc.Center(
                dmc.Button("OK", id="submit-button", color="teal", mt="xl")
            ),
            #html.Div(id="output-id")  # debug output

        ], style={
            "maxWidth": "800px", 
            "margin": "auto", 
            "marginTop": "50px",
            "overflowY": "auto",
            "paddingBottom": "250px"
            })
    ])

# włączanie/wyłączanie suwaków
@callback(Output("heating_quality", "disabled"), Input("heating_quality_enabled", "checked"))
def toggle_hq(e): return not e

@callback(Output("cooking_quality", "disabled"), Input("cooking_quality_enabled", "checked"))
def toggle_cq(e): return not e

@callback(Output("computing_quality", "disabled"), Input("computing_quality_enabled", "checked"))
def toggle_comp(e): return not e

@callback(Output("cooling_quality", "disabled"), Input("cooling_quality_enabled", "checked"))
def toggle_cool(e): return not e


# # move to the next step and update progress
@callback(
    Output("wizard-progress", "data", allow_duplicate=True),
    Output("steps-navbar", "children", allow_duplicate=True),  # wymuszamy refresh navbaru
    Input("submit-button", "n_clicks"),
    State("wizard-progress", "data"),
    prevent_initial_call=True
)
def go_to_step2(n_clicks, progress):
    if not n_clicks:
        raise PreventUpdate

    progress["step_1_done"] = True
    return progress, no_update

# # wysyłanie na BE

# @callback(
#     Output("output-id", "children"),        # ???
#     Input("submit-button", "n_clicks"),     # ???
#     State("cost_pln", "value"),
#     State("co2_emission_kg", "value"),
#     State("normalized_comfort", "value"),
#     State("normalized_failure_rate", "value"),
#     State("device_cost", "value"),

#     State("heating_quality_enabled", "checked"),
#     State("heating_quality", "value"),

#     State("cooking_quality_enabled", "checked"),
#     State("cooking_quality", "value"),

#     State("computing_quality_enabled", "checked"),
#     State("computing_quality", "value"),

#     State("cooling_quality_enabled", "checked"),
#     State("cooling_quality", "value"),
# )

# def collect_user_input(_, cost, co2, comfort, failure, device,
#                        heating_enabled, heating,
#                        cooking_enabled, cooking,
#                        computing_enabled, computing,
#                        cooling_enabled, cooling):

#     user_input = {
#         "cost_pln": cost,
#         "co2_emission_kg": co2,
#         "normalized_comfort": comfort,
#         "normalized_failure_rate": failure,
#         "device_cost": device,
#     }

#     if heating_enabled:
#         user_input["heating_quality"] = heating
#     if cooking_enabled:
#         user_input["cooking_quality"] = cooking
#     if computing_enabled:
#         user_input["computing_quality"] = computing
#     if cooling_enabled:
#         user_input["cooling_quality"] = cooling

#     return str(user_input)  # debug; tu można np. wysłać do API, itp.

@callback(
    Output("user-input-store", "data"),
    Output("redirect", "pathname"),
    Input("submit-button", "n_clicks"),
    State("cost_pln", "value"),
    State("co2_emission_kg", "value"),
    State("normalized_comfort", "value"),
    State("normalized_failure_rate", "value"),
    State("device_cost", "value"),
    State("heating_quality_enabled", "checked"),
    State("heating_quality", "value"),
    State("cooking_quality_enabled", "checked"),
    State("cooking_quality", "value"),
    State("computing_quality_enabled", "checked"),
    State("computing_quality", "value"),
    State("cooling_quality_enabled", "checked"),
    State("cooling_quality", "value"),
    prevent_initial_call=True
)
def collect_user_input(_, cost, co2, comfort, failure, device,
                       heating_enabled, heating,
                       cooking_enabled, cooking,
                       computing_enabled, computing,
                       cooling_enabled, cooling):
    user_input = {
        "cost_pln": cost,
        "co2_emission_kg": co2,
        "normalized_comfort": comfort,
        "normalized_failure_rate": failure,
        "device_cost": device,
        "heating_quality": heating if heating_enabled else 0,
        "cooking_quality": cooking if cooking_enabled else 0,
        "computing_quality": computing if computing_enabled else 0,
        "cooling_quality": cooling if cooling_enabled else 0,
    }

    print("Zbierane dane od użytkownika:", user_input)
    return user_input, "/profil"
