import streamlit as st
import numpy as np
import pandas as pd
import datetime
from utils.plot import *
from utils.data_source import *
from utils.constantes import *
import os


def generate_regions_choropleth(
    data: pd.DataFrame,
    feature: str,
    title: str,
    width: int = 1000,
    height: int = 600,
    log_scale: bool = True
) -> alt.Chart:
    shape = alt.topo_feature("https://raw.githubusercontent.com/MaximeChallon/Coviz-19/master/utilitaires/data/data_country.topo.json", "countries")

    area_name = "Country"
    lookup_in_shape = "Country"
    lookup_in_df = "Country"

    chart_data = data[data[feature] > 0][[feature, lookup_in_df]]

    base_chart = (
        alt.Chart(shape)
        .mark_geoshape(stroke="black", strokeWidth=0.5, color="white")
        .encode(tooltip=[alt.Tooltip(f"properties.{area_name}:N", title=title)])
    )
    scale = (
        alt.Scale(type="log", scheme="yelloworangered")
        if log_scale
        else alt.Scale(type="linear", scheme="yelloworangered")
    )
    color_chart = (
        alt.Chart(shape)
        .mark_geoshape(stroke="black", strokeWidth=0.5)
        .encode(
            color=alt.Color(
                f"{feature}:Q",
                title=feature,
                scale=scale,
                legend=alt.Legend(labelLimit=50),
            ),
            tooltip=[
                alt.Tooltip(f"properties.{area_name}:N", title=title),
                alt.Tooltip(f"{feature}:Q", title=feature, format=".4~f"),
            ],
        )
        .transform_lookup(
            f"properties.{lookup_in_shape}",
            from_=alt.LookupData(data=chart_data, key=lookup_in_df, fields=[feature])
        )
    )

    final_chart = (
        (base_chart + color_chart)
        .configure_view(strokeWidth=0)
        .properties(width=width, height=height)
    )

    return final_chart


def chloropleth_maps(data):
    st.title("Distribution géographique du Covid-19 dans le monde")

    st.markdown("Quel indicateur utiliser?")
    features = get_features_country(data)
    feature = st.selectbox(label="Choisir", options=features)

    regional_choice = st.radio(
        label=("Echelle pour le monde"), options=[("Linéaire"), ("Logarithmique")]
    )
    min_day = 0

    if regional_choice == "Linéaire":
        log_scale = False
    else:
        log_scale = True

    # Date selection
    data["days_passed"] = data["Date"].apply(lambda x: (x - datetime.date(2020, 1, 22)).days)
    # data["days_passed"] = data['Date'].sub(data['First_Date'], axis=0)
    n_days = data["days_passed"].unique().shape[0] - 1
    st.markdown("Choisir le jour à visualiser depuis le 22 janvier 2020.")
    chosen_n_days = st.slider(
        "Jours:", min_value=min_day, max_value=n_days, value=n_days,
    )
    st.markdown(
        ("Date choisie: "
            + f"{datetime.date(2020, 1, 22) + datetime.timedelta(days=chosen_n_days)}"
        )
    )
    day_data = data[data["days_passed"] == chosen_n_days]

    if day_data.empty:
        st.warning("Aucune information disponible pour la date sélectionnée.")
    else:
        choropleth = generate_regions_choropleth(
            day_data, feature, "Country", log_scale=log_scale
        )
        st.altair_chart(choropleth)