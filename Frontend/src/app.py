from dash import Dash, html, dcc, Output, Input
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import dash
import steps_navbar
import main_navbar  

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP,'assets/custom.css']
)

app.layout = dmc.MantineProvider(
    html.Div([
        main_navbar.render(app),
        dcc.Store(id="wizard-progress", data={"step_1_done": False, "step_2_done": False}),             
        dcc.Location(id="url"),
        html.Div(id="steps-navbar"),          
        dash.page_container
    ])
)

@app.callback(
    Output("steps-navbar", "children"),
    Input("url", "pathname"),
    Input("wizard-progress", "data")
)
def update_navbar(pathname, progress):
    if pathname == "/":
        return None  
    return steps_navbar.render(pathname, progress)

@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("wizard-progress", "data"),
    prevent_initial_call=True
)
def redirect_after_progress(progress):
    if progress is None:
        raise dash.exceptions.PreventUpdate
    
    if progress.get("step_1_done") and not progress.get("step_2_done"):
        return "/profil"
    elif progress.get("step_2_done"):
        return "/zestawienie"
    raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run(debug=True, port=8050)
