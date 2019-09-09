# Team Records at each Date in the Season
# TeamRecords_byDate.py
# KAC - 09/08/2019

import pandas as pd
import numpy as np
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


df_temp = pd.DataFrame(df_boxScores.loc[df_boxScores['Home_Runs']>df_boxScores['Away_Runs']])
df_homeWins = pd.DataFrame(df_temp.groupby(['Date', 'Home_Team']).size().reset_index())
df_homeWins = df_homeWins.rename(columns={'Home_Team':'Team', df_homeWins.columns[2]:'Home_Win'})
df_awayLosses = pd.DataFrame(df_temp.groupby(['Date', 'Away_Team']).size().reset_index())
df_awayLosses = df_awayLosses.rename(columns={'Away_Team':'Team', df_awayLosses.columns[2]:'Away_Loss'})
df_temp2 = pd.DataFrame(df_boxScores.loc[df_boxScores['Home_Runs']<df_boxScores['Away_Runs']])
df_homeLosses = pd.DataFrame(df_temp2.groupby(['Date', 'Home_Team']).size().reset_index())
df_homeLosses = df_homeLosses.rename(columns={'Home_Team':'Team', df_homeLosses.columns[2]:'Home_Loss'})
df_awayWins = pd.DataFrame(df_temp2.groupby(['Date', 'Away_Team']).size().reset_index())
df_awayWins = df_awayWins.rename(columns={'Away_Team':'Team', df_awayWins.columns[2]:'Away_Win'})


df_dates = pd.DataFrame()
dates= df_awayWins.Date.unique()
teams = df_awayWins.Team.unique()
teams = sorted(teams)

df_dateRecord = pd.DataFrame(columns=['Date', 'Team', 'Total_Wins', 'Total_Losses', 'Home_Wins', 'Home_Losses',
                                      'Away_Wins', 'Away_Losses'])

for date in dates:
    for team in teams:
        h_w = df_homeWins.loc[(df_homeWins['Date'] <= date) & (df_homeWins['Team'] == team), 'Home_Win'].sum()
        h_l = df_homeLosses.loc[(df_homeLosses['Date'] <= date) & (df_homeLosses['Team'] == team), 'Home_Loss'].sum()
        a_w = df_awayWins.loc[(df_awayWins['Date'] <= date) & (df_awayWins['Team'] == team), 'Away_Win'].sum()
        a_l = df_awayLosses.loc[(df_awayLosses['Date'] <= date) & (df_awayLosses['Team'] == team), 'Away_Loss'].sum()
        t_w = h_w + a_w
        t_l = h_l + a_l
        df_dateRecord = df_dateRecord.append({'Date': date, 'Team': team, 'Total_Wins': t_w, 'Total_Losses': t_l,
                                              'Home_Wins': h_w, 'Home_Losses': h_l, 'Away_Wins': a_w,
                                              'Away_Losses': a_l}, ignore_index=True)

df_dateRecord.to_csv('Team_RecordbyDate', index=False)



