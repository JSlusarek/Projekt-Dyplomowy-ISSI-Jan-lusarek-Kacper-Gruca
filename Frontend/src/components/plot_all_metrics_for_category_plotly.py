import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_all_metrics_for_category_plotly(df, profile, appliance_recommendations_for_profiles, show=True):
    """
    Tworzy i opcjonalnie wyświetla wykresy 1x4 dla każdej kategorii urządzeń z profilu użytkownika.

    Parameters
    ----------
    df : pandas.DataFrame
        Dane porównawcze urządzeń.
    profile : str
        Nazwa profilu użytkownika, np. 'Saver', 'EcoFriendly'.
    appliance_recommendations_for_profiles : dict
        Słownik rekomendacji {profile: {category: recommended_device_name}}.
    show : bool
        Czy od razu wyświetlać wykresy (True), czy tylko zwrócić jako listę obiektów Figure (False).

    Returns
    -------
    List[go.Figure]
        Lista wykresów Plotly (po jednej figurze na kategorię).
    """

    category_assumptions = {
        'boiling_water': 'liters = 1.5',
        'cooking': 'time_minutes = 30',
        'heating_food': 'time_minutes = 30',
        'making_coffee': 'cups = 1',
        'multicookers': 'recipe_complexity = 1.5',
        'water_heating': 'liters = 50',
        'bathing': '',
        'bathroom_heating': '',
        'workstation': '',
        'cooling': 'duration_min = 60'
    }

    recommended = appliance_recommendations_for_profiles[profile]
    category_order = list(recommended.keys())

    df = df[df['category'].isin(category_order)].copy()

    # Oznaczamy urządzenia rekomendowane
    df['is_recommended'] = df.apply(
        lambda row: row['name'] == recommended.get(row['category']), axis=1
    )

    figures = []

    for category in category_order:
        data = df[df['category'] == category]
        assumption = category_assumptions.get(category, '')

        metrics = ['energy_kwh', 'cost_pln', 'co2_emission_kg', 'device_cost']
        metric_titles = ['Energy (kWh)', 'Cost (PLN)', 'CO₂ (kg)', 'Device Cost (PLN)']

        fig = make_subplots(rows=1, cols=4, subplot_titles=metric_titles)

        for i, metric in enumerate(metrics):
            for _, row in data.iterrows():
                fig.add_trace(
                    go.Bar(
                        x=[row['name']],
                        y=[row[metric]],
                        marker_color='#00695c' if row['is_recommended'] else '#e0e0e0',
                        showlegend=False,
                        hovertemplate=f"{row['name']}<br>{metric}: {row[metric]}<extra></extra>"
                    ),
                    row=1, col=i + 1
                )

        title_text = f"{category}"
        if assumption:
            title_text += f"<br><sup>{assumption}</sup>"

        fig.update_layout(
            height=400,
            width=1200,
            title_text=title_text,
            title_x=0.5,
            margin=dict(t=80)
        )
        fig.update_xaxes(tickangle=30)

        if show:
            fig.show()

        figures.append(fig)

    return figures
