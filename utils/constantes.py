from datetime import date
import datetime
import os

# dataset
try:
    yesterday = date.today() - datetime.timedelta(1)
    Date = yesterday.strftime("%m_%d_%y")
    DATA = 'https://raw.githubusercontent.com/acorpus/CombinedCovid/master/time_series_covid19_combined_global_' + Date + '.csv'
    os.system('wget ' + DATA)
    DATA = 'https://raw.githubusercontent.com/acorpus/CombinedCovid/master/time_series_covid19_combined_global_' + Date + '.csv'
except:
    Today = date.today()
    Date = Today.strftime("%m_%d_%y")
    DATA = 'https://raw.githubusercontent.com/acorpus/CombinedCovid/master/time_series_covid19_combined_global_' + Date + '.csv'
    os.system('wget ' + DATA)
    DATA = 'https://raw.githubusercontent.com/acorpus/CombinedCovid/master/time_series_covid19_combined_global_' + Date + '.csv'
