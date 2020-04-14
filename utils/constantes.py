from datetime import date
import datetime
import os
import requests
import re


x = requests.get('https://github.com/acorpus/CombinedCovid')
url = x.text
with open('html.html', "w") as f:
    f.write(url)
with open('html.html', 'r') as f:
    for ligne in f:
        if "time_series_covid19_combined_global" in ligne:
            FILE_NAME = re.sub(r'.*>([^<]+)<.*$',r'\1',ligne)
            FILE_NAME = FILE_NAME.replace('\n', '')
os.remove('html.html')
DATA = "https://raw.githubusercontent.com/acorpus/CombinedCovid/master/" + FILE_NAME