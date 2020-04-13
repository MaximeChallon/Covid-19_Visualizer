import streamlit as st
import numpy as np
import os
import csv
import pandas as pd
from .constantes import *
import datetime
import scipy

def load_data():
    data = pd.read_csv(DATA)
    del data['Lat']
    del data['Long']
    
    return data