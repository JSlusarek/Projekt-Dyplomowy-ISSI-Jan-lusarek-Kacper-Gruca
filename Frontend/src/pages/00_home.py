import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__, path="/", name="Start")

def layout(**kwargs):
    return dmc.Container([
        dmc.Title("Cześć!", order=1, ta="center", mt="xl"),

        dmc.Text(
            "Witaj w Home Appliance Profiling System",
            ta="center",
            size="md",
            style={"maxWidth": "800px", "margin": "auto", "marginTop": "20px"}
        ),

        dmc.Text(
            "Nasza aplikacja wspiera Cię w analizie Twoich preferencji domowych i "
            "dopasowaniu najlepszego sprzętu AGD przy wykorzystaniu sztucznej inteligencji.",
            ta="center",
            size="sm",
            style={"maxWidth": "800px", "margin": "auto", "marginTop": "10px", "marginBottom": "30px"}
        ),

        dmc.Title("Jak korzystać z aplikacji?", order=3, ta="center", mt="xl"),

        dmc.List(
            spacing="md",
            size="sm",
            center=True,
            icon=html.Div("✓", style={"color": "teal", "fontWeight": "bold", "fontSize": "18px"}),
            children=[
                dmc.ListItem("Krok 1: Wypełnij formularz i zatwierdź przypisany profil użytkownika."),
                dmc.ListItem("Krok 2: Poznaj swój profil – zobacz jego szczegółowy opis, oparty na algorytmach AI."),
                dmc.ListItem("Krok 3: Przejrzyj zestawienie urządzeń najlepiej dopasowanych do Twojego profilu."),
            ],
            style={"maxWidth": "800px", "margin": "auto", "marginTop": "20px"}
        ),

        dmc.Center(
            html.A(
                dmc.Button("Rozpocznij", size="md", mt=40, color="teal", radius="md"),
                href="/formularz",
                style={"textDecoration": "none"}
            )
        )
    ], style={"marginTop": "60px"})
