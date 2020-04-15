from utils.data_source import *
import altair as alt
import streamlit as st


##############################################################################################
############################# general plots ################################################
##############################################################################################


def get_features_general(data):
    """
    Récupère les colonnes utilisées pour faire le graphique des données mondiales
    :param data: DataFrame Pandas
    :return: list
    """
    feature_data = data.drop(columns=[
            "Date",
            "Country",
            "Population",
            "Percent_Change_Cases",
            "Percent_Change_Deaths",
            "New_Cases_per_10000",
            "New_Deaths_per_10000",
            "Cases_per_10000",
            "Deaths_per_10000",
            "First_Date"])
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


def line_plots_general(data):
    """
    Créé un graphique pour les données mondiales
    :param data: DataFrame Pandas
    :return: None
    """
    st.markdown("## Données mondiales")
    features = get_features_general(data)
    feature = st.selectbox(label="Choisir...", options=features)

    # Group data by date
    general = data.groupby("Date", as_index=False).sum()

    # Choose log scale or linear, defines what feature to use
    general_choice = st.radio(label="Echelle", options=["Linéaire", "Logarithmique"])
    if general_choice == "Logarithmique":
        general = general[general[feature] > 0]
        general_scale = alt.Scale(type="log")
    else:
        general_scale = alt.Scale(type="linear")

    general_chart = generate_global_chart(general, feature, general_scale, "Mois et jour")
    st.altair_chart(general_chart)

##############################################################################################
############################# countries plots ################################################
##############################################################################################


def get_features_country(data):
    """
    Récupère les colonnes nécessaires pour le graphique des pays
    :param data:  DataFrame Pandas
    :return:  list
    """
    feature_data = data.drop(columns=[
            "Date",
            "Country",
            "Population",
            "First_Date"])
    return feature_data.columns.tolist()


def calculate_growth_factor(data, features):
    for feature in features:
        data[f"{feature}_y"] = data[feature].shift()
        data[f"{feature}_i"] = data[feature] / data[f"{feature}_y"]
    return data


def regional_growth_factor(data, features):
    regions_raw = []
    for region_name, region in data.groupby("Country"):
        region = region.sort_values("Date")
        region = calculate_growth_factor(region, features)
        regions_raw.append(region)
    data = pd.concat(regions_raw).reset_index(drop=True)
    return data


def generate_regional_chart(
    data: pd.DataFrame,
    feature: str,
    scale: alt.Scale,
    x_title: str,
    color_title: str,
    padding: int = 5,
    width: int = 700,
    height: int = 500,
    legend_position: str = "top-left",
):
    return (
        alt.Chart(data)
        .mark_line(point={"size": 70})
        .encode(
            x=alt.X("Date", title=x_title),
            y=alt.Y(f"{feature}", title=feature, scale=scale),
            color=alt.Color("Country", title=color_title),
            tooltip=[
                alt.Tooltip("Country", title=color_title),
                alt.Tooltip(f"{feature}", title=feature),
                alt.Tooltip("Date", title=x_title, type="temporal"),
            ],
        )
        .configure_legend(
            fillColor="white",
            strokeWidth=3,
            strokeColor="#f63366",
            cornerRadius=5,
            padding=10,
            orient=legend_position,
        )
        .configure_scale(continuousPadding=padding)
        .properties(width=width, height=height)
        .interactive()
    )


def line_plots_countries(data):
    st.markdown("## Données des pays")
    features = get_features_country(data)
    feature = st.selectbox(label="Choisir...", options=features)
    # Get list of regions and select the ones of interest
    region_options = data["Country"].sort_values().unique().tolist()
    regions = st.multiselect(
        label="Pays",
        options=region_options,
        default=["France", "Italy", "United States"],
    )
    # Filter regions in selection
    selected_regions = data[data["Country"].isin(regions)]

    if selected_regions.empty:
        st.warning("Aucun pays sélectionné!")
    else:
        selected_regions = regional_growth_factor(selected_regions, features)
        regional_choice = st.radio(
            label="Echelle pour les pays", options=["Linéaire", "Logarithmique"]
        )
        if regional_choice == "Logarithmique":
            selected_regions = selected_regions[selected_regions[feature] > 0]
            regional_scale = alt.Scale(type="log")
        else:
            regional_scale = alt.Scale(type="linear")

        regional_chart = generate_regional_chart(
            selected_regions,
            feature,
            regional_scale,
            x_title="Mois et jour",
            color_title="Pays",
        )
        st.altair_chart(regional_chart)


def line_plots(data):
    line_plots_general(data)
    line_plots_countries(data)