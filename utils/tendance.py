import streamlit as st
import numpy as np
import pandas as pd
from utils.constantes import *
import altair as alt
import os

def average_over_days(data, categorical_columns, avg_days=5):
    """Returns an average over the latest avg_days days of all values in data"""
    data = data.sort_values(by="Date", ascending=False, axis=0).reset_index(drop=True)
    grouped_categorical = (
        data[categorical_columns].groupby(data.index // avg_days).first()
    )
    grouped_numerical = data.groupby(data.index // avg_days).mean()
    return pd.concat([grouped_categorical, grouped_numerical], axis=1)


def generate_trajectory_chart(
    data: pd.DataFrame,
    scale: alt.Scale,
    feature_x: str,
    feature_y: str,
    colour_code_column: str = None,
    padding: int = 5,
    width: int = 700,
    height: int = 500
):

    scale = scale
    chart = (
        alt.Chart(data)
        .mark_line(point={"size": 70})
        .encode(
            x=alt.X(f"{feature_x}:Q", title=feature_x, scale=scale),
            y=alt.Y(f"{feature_y}:Q", title=feature_y, scale=scale),
            tooltip=[
                alt.Tooltip(f"{feature_x}", title=feature_x, format=".2~f"),
                alt.Tooltip(f"{feature_y}", title=feature_y, format=".2~f"),
                alt.Tooltip("Date", type="temporal"),
            ],
        )
    )

    if colour_code_column:
        chart = chart.encode(color=colour_code_column)

    return (
        chart.configure_scale(continuousPadding=padding)
        .properties(width=width, height=height)
        .interactive()
    )


def trajectory_cases(data):

    st.markdown("## Graphique de la tendance mondiale")
    st.markdown('Ce graphique permet d\'observer la baisse du nombre de cas quotidiens par rapport au nombre de cas total.\
                Faire bouger le curseur permet de linéariser plus ou moins la courbe. Pour effacer cet effet, mettre sur 1,\
                 c\'est à dire qu\'un point apparaît pour chaque jour; mettre sur 10 signifie qu\'un point apparaît tous les 10 jours. ')
    data = data[
        ["Date", "Cases", "New_Cases", "Country"]
    ]
    data = data.sort_values(by="Date", axis=0)

    n_days = data["Date"].unique().shape[0]
    avg_days = st.slider(label="Intervalles entre les jours", min_value=1, max_value=n_days // 4, value=5)

    scale_choice = st.radio(
        label="Echelle...", options=["Linéaire", "Logarithmique"]
    )
    if scale_choice == "Logarithmique":
        scale_choice = alt.Scale(type="log")
    else:
        scale_choice = alt.Scale(type="linear")

    mondial = (data.drop(columns="Country").groupby("Date", as_index=False).sum())
    mondial = average_over_days(mondial, "Date", avg_days)

    chart = generate_trajectory_chart(mondial, scale_choice, "Cases", "New_Cases")
    st.altair_chart(chart)

    st.markdown("## Graphique de la tendance pour chaque pays")
    st.markdown("C'est le même principe que le graphe du dessous. \
                Bouger la barre du haut permet également de changer ce graphique. \
                Ces graphes permettent d'observer le moment où la présence du vrus semble baisser.")

    pays_options = data["Country"].sort_values().unique().tolist()
    pays = st.multiselect(
        label="Pays à utiliser",
        options=pays_options,
        default=["France", "Italy", "United States"],
    )

    selected_regions = data[data["Country"].isin(pays)]

    if selected_regions.empty:
        st.warning("Aucun pays sélectionné")
    else:
        averaged_regions = (selected_regions.groupby(["Country"], as_index=False)
            .apply(lambda group: average_over_days(group, ["Date", "Country"], avg_days))
            .reset_index(level=0, drop=True)
            .reset_index(drop=True))

        final_data = averaged_regions[(averaged_regions["Cases"] > 0)& (averaged_regions["New_Cases"] > 0)]

        st.altair_chart(generate_trajectory_chart(final_data,scale_choice,"Cases","New_Cases",colour_code_column="Country"))