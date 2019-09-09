# UTC_to_EST.py
# Converts UTC times to EST
# KAC 09/09/2019

import pandas as pd
from datetime import datetime, timezone

path = '/Users/Koby/PycharmProjects/MLBData/Input/'

df_boxScores = pd.read_csv(path + '2016-boxScores-Date.csv')

def utc_to_est(utc_date):
    hour = int(utc_date[11:13])
    if hour - 12 > 0:
        est_date = utc_date[:10]
        est_date = datetime.strptime(est_date, '%Y-%m-%d')
    else:
        day = int(utc_date[8:10]) - 1
        month = int(utc_date[5:7])
        if day == 0 and (month == 6 or month == 8 or month == 9):
            month = month - 1
            day = 31
        if day == 0 and (month == 5 or month == 7 or month == 10):
            month = month - 1
            day = 30
        est_date = utc_date[:5] + str(month).zfill(2) + '-' + str(day).zfill(2)
        est_date = datetime.strptime(est_date, '%Y-%m-%d')
    return est_date


df_boxScores.Date = df_boxScores.Date.apply(utc_to_est)
df_boxScores.drop(labels=['gameId'], inplace=True, axis=1)

df_boxScores.to_csv('boxScores_Date.csv', index=False)
