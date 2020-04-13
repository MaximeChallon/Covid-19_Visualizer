import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *
import os

st.title("Covid-19 vizualizer")

data = load_data()

st.write(get_countries_metadata())

os.remove('data_pret.csv')
os.remove(DATA.replace('https://raw.githubusercontent.com/acorpus/CombinedCovid/master/', ''))
