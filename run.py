import streamlit as st
import numpy as np
import pandas as pd
from utils.plot import *
from utils.data_source import *
from utils.map import *
from utils.constantes import *
import os
from typing import Dict, Callable


data = load_data()

st.sidebar.title("Covid-19 Visualizer")
page = st.sidebar.selectbox(
    label="Sommaire",
    options=[
        "Graphiques temporels",
        "Distribution géographique ",
    ],
)

page_function_mapping: Dict[str, Callable[[pd.DataFrame], None]] = {
    "Graphiques temporels": line_plots,
    "Distribution géographique ": chloropleth_maps
}

page_function_mapping[page](data)