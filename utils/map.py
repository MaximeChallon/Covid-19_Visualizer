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
    log_scale: bool = True,
    is_region: bool = True,
) -> alt.Chart:
    if is_region:
        shape = alt.topo_feature("https://raw.githubusercontent.com/MaximeChallon/Coviz-19/master/utilitaires/data/data_country.topo.json", "countries")
    else:
        shape = alt.topo_feature("https://raw.githubusercontent.com/MaximeChallon/Coviz-19/master/utilitaires/data/data_country.topo.json", "countries")

    area_name = "Country" if is_region else "Country"
    lookup_in_shape = "Country" if is_region else "Country"
    lookup_in_df = "Country" if is_region else "Country"

    chart_data = data[data[feature] > 0][[feature, lookup_in_df]]

    base_chart = (
        alt.Chart(shape)
        .mark_geoshape(stroke="black", strokeWidth=0.5, color="white")
        .encode(tooltip=[alt.Tooltip(f"properties.{area_name}:N", title=title)])
    )
    scale = (
        alt.Scale(type="log", scheme="yelloworangered")
        if log_scale
        else alt.Scale(type="linear", scheme="teals")
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


def choropleth_maps(data):
    st.title("COVID-19 in Italy - Geographical distribution")

    map_scale = st.radio(
        label="What resolution would you like to visualise?",
        options=["Province", "Region"])
    is_region = map_scale == "Region"

    if is_region:
        st.markdown("What indicator would you like to visualise?")
        features = get_features_country(data)
        feature = st.selectbox(label="Choose...", options=features)

        is_growth_factor = st.checkbox(label="Growth factor of feature")
        min_day = 0
        log_scale = True
    else:
        #data = get_province_data()
        data.columns = [
            "Cases" if feature == "Cases" else feature
            for feature in data.columns
        ]
        feature = "Cases"

        st.markdown("Only total cases and their growth factor are available at the province resolution.")
        feature_str = st.selectbox(
            label="What feature would you like to visualise?",
            options=["Cases"],
        )
        min_day = 0
        log_scale = True

    # Date selection
    data["days_passed"] = data["Date"].apply(lambda x: (x - datetime.date(2020, 1, 22)).days)
    # data["days_passed"] = data['Date'].sub(data['First_Date'], axis=0)
    n_days = data["days_passed"].unique().shape[0] - 1
    st.markdown("Choose what date to visualise as the number of days elapsed since the first data collection, on 24th February:")
    chosen_n_days = st.slider(
        "Days:", min_value=min_day, max_value=n_days, value=n_days,
    )
    st.markdown(
        ("Chosen date: "
            + f"{datetime.date(2020, 1, 22) + datetime.timedelta(days=chosen_n_days)}"
        )
    )
    day_data = data[data["days_passed"] == chosen_n_days]

    if day_data.empty:
        st.warning("No information is available for the selected date")
    else:
        choropleth = generate_regions_choropleth(
            day_data, feature, "Country", log_scale=log_scale, is_region=is_region
        )
        st.altair_chart(choropleth)