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
        dcc.Location(id="url"),
        html.Div(id="steps-navbar"),          
        dash.page_container
    ])
)

@app.callback(
    Output("steps-navbar", "children"),
    Input("url", "pathname")
)
def update_navbar(pathname):
    if pathname == "/":
        return None  
    return steps_navbar.render(pathname)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
