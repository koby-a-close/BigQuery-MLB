# Team Records and Splits for 2016 Season
# TeamRecords_Splits.py
# KAC - 09/02/2019

import pandas as pd
import numpy as np

path = '/Users/Koby/PycharmProjects/MLBData/Input/2016-boxScores.csv'

df_boxScores = pd.read_csv(path)
df_boxScores = df_boxScores.rename(columns = {df_boxScores.columns[1]: 'homeTeam', df_boxScores.columns[2]: 'homeRuns',
                               df_boxScores.columns[3]: 'homeHits', df_boxScores.columns[4]: 'homeErrors',
                               df_boxScores.columns[5]: 'awayTeam', df_boxScores.columns[6]: 'awayRuns',
                               df_boxScores.columns[7]: 'awayHits', df_boxScores.columns[8]: 'awayErrors'})

print(df_boxScores.head(10))

df_temp = pd.DataFrame(df_boxScores.loc[df_boxScores['homeRuns']>df_boxScores['awayRuns']])
df_teamRecords = pd.DataFrame(df_temp.groupby(['homeTeam']).size().reset_index())
df_awayLosses = pd.DataFrame(df_temp.groupby(['awayTeam']).size().reset_index())
# df_teamRecords.drop(df_teamRecords.index[1:])
df_teamRecords = pd.merge(left=df_teamRecords, right=df_awayLosses, how= 'inner', left_on='homeTeam', right_on='awayTeam')
df_teamRecords.drop(labels = ['awayTeam'], inplace=True, axis=1)
df_teamRecords.drop([0])
df_teamRecords = df_teamRecords.rename(columns = {df_teamRecords.columns[0]: 'Team',
                                                  df_teamRecords.columns[1]: 'Home_Wins',
                                                  df_teamRecords.columns[2]: 'Away_Losses'})
df_temp2 = pd.DataFrame(df_boxScores.loc[df_boxScores['homeRuns']<df_boxScores['awayRuns']])
df_homeLosses = pd.DataFrame(df_temp2.groupby(['homeTeam']).size().reset_index())
df_awayWins = pd.DataFrame(df_temp2.groupby(['awayTeam']).size().reset_index())
df_teamRecords = pd.merge(left=df_teamRecords, right=df_homeLosses, how='left', left_on='Team', right_on='homeTeam')
df_teamRecords = pd.merge(left=df_teamRecords, right=df_awayWins, how='left', left_on='Team', right_on='awayTeam')
df_teamRecords.drop(labels = ['awayTeam', 'homeTeam'], inplace=True, axis=1)
df_teamRecords = df_teamRecords.rename(columns = {df_teamRecords.columns[3]: 'Home_Losses',
                                                  df_teamRecords.columns[4]: 'Away_Wins'})
df_teamRecords = df_teamRecords[['Team', 'Home_Wins', 'Home_Losses', 'Away_Wins', 'Away_Losses']]
df_teamRecords.to_csv('Team_RecordSplits.csv', index=False)
