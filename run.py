import streamlit as st
import numpy as np
import pandas as pd
from utils.plot import *
from utils.data_source import *
from utils.map import *
from utils.constantes import *
from utils.tendance import trajectory_cases
import os
from typing import Dict, Callable


data = load_data()

st.sidebar.title("Covid-19 Visualizer")
page = st.sidebar.selectbox(
    label="Sommaire",
    options=[
        "Données",
        "Graphiques temporels",
        "Graphiques de tendance",
        "Distribution géographique ",
    ],
)

page_function_mapping: Dict[str, Callable[[pd.DataFrame], None]] = {
    "Données": show_data,
    "Graphiques temporels": line_plots,
    "Graphiques de tendance": trajectory_cases,
    "Distribution géographique ": chloropleth_maps
}

page_function_mapping[page](data)