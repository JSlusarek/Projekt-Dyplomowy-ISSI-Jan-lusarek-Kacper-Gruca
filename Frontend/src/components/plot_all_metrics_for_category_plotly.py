import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_all_metrics_for_category_plotly(df, category, category_assumptions):
    """
    Plot device comparison metrics for a given category as 1x4 Plotly bar charts.

    For the specified device category, generates a row of four bar charts comparing:
    energy usage, cost, CO₂ emissions, and device cost. Highlights the recommended device
    (from the 'is_recommended' column) in a different color. Displays any defined input
    assumptions below the main title.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing device comparison data. Must include the following columns:
        'name', 'category', 'energy_kwh', 'cost_pln', 'co2_emission_kg',
        'device_cost', and 'is_recommended'.

    category : str
        The category of devices to visualize (e.g. 'cooking', 'boiling_water').

    category_assumptions : dict
        Dictionary of input assumptions per category (e.g. {'cooking': 'time_minutes = 30'}).
        Used to display scenario context under the chart title.

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly Figure object containing four subplots (1 row × 4 columns) for the given category.
    """

    metrics = ['energy_kwh', 'cost_pln', 'co2_emission_kg', 'device_cost']
    metric_titles = ['Energy (kWh)', 'Cost (PLN)', 'CO₂ (kg)', 'Device Cost (PLN)']
    assumption = category_assumptions.get(category, '')
    data = df[df['category'] == category]

    fig = make_subplots(rows=1, cols=4, subplot_titles=metric_titles)

    for i, metric in enumerate(metrics):
        for _, row in data.iterrows():
            fig.add_trace(
                go.Bar(
                    x=[row['name']],
                    y=[row[metric]],
                    name=row['name'],
                    marker_color='green' if row['is_recommended'] else 'gray',
                    showlegend=False if row['is_recommended'] else False,
                    hovertemplate=f"{row['name']}<br>{metric}: {row[metric]}<extra></extra>"
                ),
                row=1, col=i+1
            )

    title_text = f"{category}"
    if assumption:
        title_text += f"<br><sup>{assumption}</sup>"

    fig.update_layout(
        height=400,
        width=1200,
        title_text=title_text,
        title_x=0.5,
        margin=dict(t=80),
    )

    fig.update_xaxes(tickangle=30)

    return fig
