import streamlit as st
import numpy as np
import os
import csv
import pandas as pd
from .constantes import *
import datetime
import scipy


def list_countries(data_path):
    """
    Récupère tous les pays disponibles dans le jeu de données
    :param data_path: Pandas DataFrame
    :return: list
    """
    with open(data_path, 'r') as f:
        f_o = csv.reader(f)
        next(f_o)
        liste_pays = []
        noms_normalises = {
            "Republic of Korea": "South Korea",
            "Holy See": "Vatican City",
            "Iran (Islamic Republic of)": "Iran",
            "Viet Nam": "Vietnam",
            "Taipei and environs": "Taiwan",
            "Republic of Moldova": "Moldova",
            "Russian Federaration": "Russia",
            "Taiwan*": "Taiwan",
            "occupied Palestinian territory": "Palestine",
            "West Bank and Gaza": "Palestine",
            "Bahamas, The": "Bahamas",
            "Cote d'Ivoire": "Ivory Coast",
            "Gambia, The": "Gambia",
            "US": "United States",
            "Cabo Verde": "Cape Verde",
            "Timor Leste": "East Timor",
            "Vatican": "Vatican City",
            "Democratic Republic of the Congo": "Congo (Kinshasa)",
            "Republic of the Congo": "Congo (Brazzaville)"
        }
        for line in f_o:
            if line[1] not in liste_pays:
                if line[1] in noms_normalises:
                    if noms_normalises[line[1]] not in liste_pays:
                        liste_pays.append((noms_normalises[line[1]]))
                else:
                    liste_pays.append(line[1])

    return liste_pays


def get_countries_metadata():
    """
    Récupère des données auxiliaires des pays
    :return: retourne un dataframe prêt à subir une left join avec le dataframe de load_data
    """
    # pour mettre les gps dans le dataframe, décommenter les deux lignes suivantes. Attention, ça mange de la RAM
    #gps = pd.read_csv('data/data_pays_gps.csv')
    metadata = pd.read_csv('data/data_population.csv')
    #metadata = pd.merge(gps, pop, on="Country", how="inner")

    return metadata


def load_data():
    """
    Charge les données depuis le dépôt de acorpus et effectue un premier traitement des données avant de faire les jointures
    :return: Pandas DataFrame pr à être utilisé dans l'application
    """
    data = pd.read_csv(DATA)
    # suppression de deux colonnes inutiles (les GPS seront mis plus tard et plus précisément)
    del data['Lat']
    del data['Long']
    # conversion de la chaîne date en datetime
    data['Date'] = pd.to_datetime(data['Date']).apply(lambda x: x.date())
    data['First_Date'] = pd.to_datetime("2020-01-22")
    # remplissage des valeurs vides de la colonne des régions avec les valeurs de la colonne pays
    data.loc[(pd.isnull(data.Province_State)), 'Province_State'] = data.Country_Region
    # remplissage des autres valeurs vides
    data.loc[(pd.isnull(data.daily_confirmed)), 'daily_confirmed'] = 0
    data.loc[(pd.isnull(data.daily_deaths)), 'daily_deaths'] = 0
    data.loc[(pd.isnull(data.change_confirmed)), 'change_confirmed'] = 0
    data.loc[(pd.isnull(data.change_deaths)), 'change_deaths'] = 0
    # suppression de la colonne country_region, dont les valeurs sont maintenant dans la colonne des provinces
    del data['Country_Region']
    # renommage des colonnes
    data.rename(columns={'Province_State': 'Country',
                         'Confirmed': "Cases",
                         'daily_confirmed': 'New_Cases',
                         'daily_deaths': 'New_Deaths',
                         'change_confirmed' : 'Percent_Change_Cases',
                         'change_deaths' : 'Percent_Change_Deaths'},
                inplace=True)

    # remplacement des noms de pays incorrects
    noms_normalises = {
        "Republic of Korea": "South Korea",
        "Korea. South": "South Korea",
        "Holy See": "Vatican City",
        "Iran (Islamic Republic of)": "Iran",
        "Viet Nam": "Vietnam",
        "Taipei and environs": "Taiwan",
        "Republic of Moldova": "Moldova",
        "Russian Federaration": "Russia",
        "Taiwan*": "Taiwan",
        "occupied Palestinian territory": "Palestine",
        "West Bank and Gaza": "Palestine",
        "Bahamas, The": "Bahamas",
        "Cote d'Ivoire": "Ivory Coast",
        "Gambia, The": "Gambia",
        "US": "United States",
        "Cabo Verde": "Cape Verde",
        "Timor Leste": "East Timor",
        "Vatican": "Vatican City",
        "Democratic Republic of the Congo": "Congo (Kinshasa)",
        "Republic of the Congo": "Congo (Brazzaville)"
    }
    for nom in noms_normalises:
        data.replace(nom, noms_normalises[nom], inplace=True)

    # jointures avec les métadonnées
    data = pd.merge(data, get_countries_metadata(), on="Country",how="left")
    # calculs par rapport aux populations
    data['New_Cases_per_10000'] = data['New_Cases'] * 10000 / data['Population']
    data['Cases_per_10000'] = data['Cases'] * 10000 / data['Population']
    data['New_Deaths_per_10000'] = data['New_Deaths'] * 10000 / data['Population']
    data['Deaths_per_10000'] = data['Deaths'] * 10000 / data['Population']

    return data


def show_data(data):
    st.markdown("## Données utilisées dans cette application")

    feature_data = data.drop(columns=[
        "Date",
        "Country",
        "Population",
        "First_Date"])
    features = feature_data.columns.tolist()
    feature = st.multiselect(
        label="Données à afficher",
        options=features,
        default=["Cases", "Deaths"]
    )

    pays_options = data["Country"].sort_values().unique().tolist()
    pays = st.multiselect(
        label="Pays à sélectionner",
        options=pays_options,
        default=["France", "Italy"]
    )

    toutes_colonnes  = data.columns.to_list()
    colonnes_selectionnees = []
    for feature in feature:
        colonnes_selectionnees.append(feature)
    colonnes_selectionnees.append('Country')
    colonnes_selectionnees.append('Date')
    for colonne in toutes_colonnes:
        if colonne not in colonnes_selectionnees:
            del data[colonne]


    data = data[data['Country'].isin(pays)]

    st.dataframe(data.reset_index(drop=True))