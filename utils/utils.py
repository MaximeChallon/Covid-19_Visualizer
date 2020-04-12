import streamlit as st
import numpy as np
import os
import csv
import pandas as pd
from .constantes import *

def load_data():
    # gestion des données globales (hors US)
    def unzip_data_global(path, header):
        os.system('wget ' + path)

        country_list = []
        province_list = []
        dates_list = []
        deaths_list = []

        with open(path.replace('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/', ''), 'r') as f:
            f_o = csv.reader(f)
            i = 0
            liste_dates_dispo = []
            for line in f_o:
                if i == 0:
                    liste_dates_dispo = line[4:]
                    i += 1
                else:
                    j = 0
                    for col in line[4:]:
                        province_list.append(line[0])
                        country_list.append(line[1].replace('*', ''))
                        dates_list.append(liste_dates_dispo[j])
                        deaths_list.append(int(col))
                        j += 1
                    i += 1

        os.remove(path.replace('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/', ''))
        all_data = {'Country': country_list,
                'Province': province_list,
                'Date': dates_list,
                header : deaths_list
                }

        data = pd.DataFrame(all_data)
        return data

    # gestion des données des United States
    def unzip_data_US(path, header):
        os.system('wget ' + path)

        country_list = []
        province_list = []
        dates_list = []
        deaths_list = []

        with open(path.replace('https://raw.githubusercontent.com/jeffcore/covid-19-usa-by-state/master/',''), 'r') as f:
            f_o = csv.reader(f)
            i = 0
            liste_dates_dispo = []
            for line in f_o:
                if i == 0:
                    liste_dates_dispo = line[1:]
                    i += 1
                else:
                    j = 0
                    for col in line[1:]:
                        province_list.append(line[0])
                        country_list.append('United States')
                        dates_list.append(liste_dates_dispo[j])
                        deaths_list.append(int(col))
                        j += 1
                    i += 1

        os.remove(path.replace('https://raw.githubusercontent.com/jeffcore/covid-19-usa-by-state/master/',''))
        all_data = {'Country': country_list,
                    'Province': province_list,
                    'Date': dates_list,
                    header: deaths_list
                    }

        data = pd.DataFrame(all_data)
        return data

    # DataFrame pandas pour chaque indicateur
    data_deaths_global = unzip_data_global(DATA_DEATHS_GLOBAL, 'Deaths')
    data_confirmed_global = unzip_data_global(DATA_CONFIRMED_GLOBAL, 'Confirmed')
    data_recovered_global = unzip_data_global(DATA_RECOVERED_GLOBAL, 'Recovered')
    data_deaths_US = unzip_data_US(DATA_DEATHS_US, 'Deaths')
    data_confirmed_US = unzip_data_US(DATA_CONFIRMED_US, 'Confirmed')

    # jointures entre les différentes sets de données
    data_merge_g1 = pd.merge(data_deaths_global, data_confirmed_global, on=['Country','Province', 'Date'], how='inner')
    data_merge_g = pd.merge(data_merge_g1, data_recovered_global, on=['Country','Province', 'Date'], how='inner')
    data_merge_us = pd.merge(data_deaths_US, data_confirmed_US, on=['Country', 'Province', 'Date'], how='inner')
    data_merge = pd.merge(data_merge_g, data_merge_us, on=['Country', 'Province', 'Date', 'Deaths', 'Confirmed'], how='outer')

    return data_merge