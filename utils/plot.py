from utils.data_source import *
from utils.constantes import *
import altair as alt
import streamlit as st
import numpy as np


def get_features_general(data) :
    feature_data = data.drop(columns=[
            "Date",
            "Country",
            "Population",
            "Percent_Change_Cases",
            "Percent_Change_Deaths",
            "New_Cases_per_10000",
            "New_Deaths_per_10000"])
    return feature_data.columns.tolist()


def generate_global_chart(
    data: pd.DataFrame,
    feature: str,
    scale: alt.Scale,
    x_title: str,
    padding: int = 5,
    width: int = 700,
    height: int = 500,
):
    return (
        alt.Chart(data)
        .mark_line(point={"size": 70})
        .encode(
            x=alt.X("Date", title=x_title),
            y=alt.Y(f"{feature}", title=feature, scale=scale),
            tooltip=[
                alt.Tooltip(f"{feature}", title=feature),
                alt.Tooltip("Date", title=x_title, type="temporal"),
            ],
        )
        .configure_scale(continuousPadding=padding)
        .properties(width=width, height=height)
        .interactive()
    )


def line_plots(data):
    features = get_features_general(data)
    feature = st.selectbox(label=("Choose..."), options=features)

    # Group data by date
    general = data.groupby("Date", as_index=False).sum()

    # Choose log scale or linear, defines what feature to use
    general_choice = st.radio(label=("Scale"), options=[("Linéaire"), ("Logarithmique")])
    if general_choice == ("Logarithmique"):
        general = general[general[feature] > 0]
        general_scale = alt.Scale(type="log")
    else:
        general_scale = alt.Scale(type="linear")

    st.markdown(("## " + ("General data")))
    general_chart = generate_global_chart(general, feature, general_scale, ("Month and day"))
    st.altair_chart(general_chart)