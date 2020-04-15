import streamlit as st
import numpy as np
import pandas as pd
from utils.plot import *
from utils.data_source import *
from utils.map import *
from utils.constantes import *
import os

st.title("Covid-19 vizualizer")

data = load_data()
st.write(data)

line_plots_general(data)

line_plots_countries(data)

choropleth_maps(data)