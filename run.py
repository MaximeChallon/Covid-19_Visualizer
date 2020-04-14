import streamlit as st
import numpy as np
import pandas as pd
from utils.plot import *
from utils.data_source import *
from utils.constantes import *
import os

st.title("Covid-19 vizualizer")

data = load_data()
st.write(data)

st.write(line_plots(data))