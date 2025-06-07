import pandas as pd
import plotly.graph_objects as go

def generate_spider_chart(parquet_path: str) -> go.Figure:
    df = pd.read_parquet(parquet_path)
    df[df.select_dtypes(include=['float']).columns] = df.select_dtypes(include=['float']).round(1)
    df = df[df["profile"] != "Balanced"]
    df.drop(columns=["optimal_score", "unique_parameter"], inplace=True)

    quality_cols = ['heating_quality', 'optimal_device', 'cooling_quality', 'cooking_quality', 'computing_quality']
    df['quality'] = df[quality_cols].bfill(axis=1).iloc[:, 0]
    df['quality'] = pd.to_numeric(df['quality'], errors='coerce')

    feature_cols = [
        "cost_pln", "co2_emission_kg", "normalized_comfort",
        "normalized_failure_rate", "device_cost", "quality"
    ]

    profile_means = df.groupby("profile")[feature_cols].mean()

    fig = go.Figure()

    for profile in profile_means.index:
        values = profile_means.loc[profile].tolist()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=feature_cols + [feature_cols[0]],
            fill='toself',
            name=profile
        ))

    fig.update_layout(
        title="Wykres pajęczynowy cech dla różnych profili użytkowników",
        showlegend=True,
        polar=dict(
            radialaxis=dict(
                visible=True,
                autorange=True
            )
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1.02,
                y=1.05,
                showactive=True,
                buttons=[
                    dict(
                        label="🔭",
                        method="relayout",
                        args=[{
                            "polar.radialaxis.range": [0, 1],
                            "polar.radialaxis.autorange": False
                        }]
                    ),
                    dict(
                        label="🔬",
                        method="relayout",
                        args=[{
                            "polar.radialaxis.autorange": True
                        }]
                    )
                ]
            )
        ]
    )

    return fig
