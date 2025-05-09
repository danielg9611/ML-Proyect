import numpy as np
import pandas as pd



df = pd.read_csv('../data/raw/dataset.csv')

df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%m-%Y')



df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')



label_map = {'LOSS': 0, 'DRAW': 1, 'WIN': 2}
df['home_result'] = df['home_result'].map(label_map)

df.drop(columns=['venue_id','venue','status','game_time','extra_time','home_winner','away_winner','home_ht_score','home_ft_score','away_ht_score','away_ft_score','home_extra_score','home_extra_score','away_extra_score','away_extra_score','referee'], inplace=True)


home_df = df[['fixture_id', 'league_season','date', 'home_team', 'home_score','away_score']].copy()
home_df.columns = ['fixture_id', 'season', 'date','team', 'goals_for', 'goals_against']
home_df['location'] = 'home'

away_df = df[['fixture_id','league_season', 'date','away_team', 'away_score','home_score']].copy()
away_df.columns = ['fixture_id', 'season','date', 'team', 'goals_for', 'goals_against']
away_df['location'] = 'away'


long_df = pd.concat([home_df, away_df])
long_df = long_df.sort_values(['team', 'date']).reset_index(drop=True)



for N in [3, 5, 10]:

    long_df[f'avg_goals_last_{N}'] = (long_df.groupby('team')['goals_for'].transform(lambda x: x.shift(1).rolling(window=N, min_periods=1).mean().round(3)))

    long_df[f'avg_goals_against_last_{N}'] = (long_df.groupby('team')['goals_against'].transform(lambda x: x.shift(1).rolling(window=N, min_periods=1).mean().round(3)))


# long_df['avg_goals_season'] = long_df.groupby(['team','season'])['goals_made'].transform('mean')

long_df['avg_goals_season'] = (
    long_df.groupby(['team', 'season'])['goals_for'].transform(lambda x: x.shift(1).expanding(min_periods=1).mean().round(3))
)
long_df['avg_goals_against_season'] = (
    long_df.groupby(['team', 'season'])['goals_against'].transform(lambda x: x.shift(1).expanding(min_periods=1).mean().round(3))
)


long_df.fillna(0, inplace=True)


long_df['avg_scoring_last_3'] = (long_df['avg_goals_last_3'] - long_df['avg_goals_against_last_3']).round(3)
long_df['avg_scoring_last_5'] = (long_df['avg_goals_last_5'] - long_df['avg_goals_against_last_5']).round(3)
long_df['avg_scoring_10'] = (long_df['avg_goals_last_10'] - long_df['avg_goals_against_last_10']).round(3)
long_df['avg_scoring_season'] = (long_df['avg_goals_season'] - long_df['avg_goals_against_season']).round(3)



long_df['points'] = np.where(long_df['goals_for'] > long_df['goals_against'], 3,1)
long_df['points'] = np.where(long_df['goals_for'] < long_df['goals_against'], 0,long_df['points'])


for N in [3, 5, 10]:

    long_df[f'points_last_{N}'] = (long_df.groupby('team')['points'].transform(lambda x: x.shift(1).rolling(window=N, min_periods=1).sum().round(3)))

long_df.fillna(0,inplace=True)



home_feats = long_df[long_df['location'] == 'home'].drop(columns=['season','goals_for','goals_against','date','points','location']).rename(columns={
    'team' : 'home_team',
    'avg_goals_last_3': 'home_avg_goals_last_3',
    'avg_goals_against_last_3' : 'home_avg_goals_against_last_3',
    'avg_goals_last_5' : 'home_avg_goals_last_5',
    'avg_goals_against_last_5' : 'home_avg_goals_against_last_5',
    'avg_goals_last_10' : 'home_avg_goals_last_10',
    'avg_goals_against_last_10' : 'home_avg_goals_against_last_10',
    'avg_goals_season' : 'home_avg_goals_season',
    'avg_goals_against_season' : 'home_avg_goals_against_season',
    'avg_scoring_last_3' : 'home_avg_scoring_last_3',
    'avg_scoring_last_5' : 'home_avg_scoring_last_5',
    'avg_scoring_10' : 'home_avg_scoring_last_10',
    'avg_scoring_season' : 'home_avg_scoring_season',
    'points_last_3' : 'home_points_last_3',
    'points_last_5' : 'home_points_last_5',
    'points_last_10' : 'home_points_last_10'
})




away_feats = long_df[long_df['location'] == 'away'].drop(columns=['season','goals_for','goals_against','date','points','location']).rename(columns={
    'team' : 'away_team',
    'avg_goals_last_3': 'away_avg_goals_last_3',
    'avg_goals_against_last_3' : 'away_avg_goals_against_last_3',
    'avg_goals_last_5' : 'away_avg_goals_last_5',
    'avg_goals_against_last_5' : 'away_avg_goals_against_last_5',
    'avg_goals_last_10' : 'away_avg_goals_last_10',
    'avg_goals_against_last_10' : 'away_avg_goals_against_last_10',
    'avg_goals_season' : 'away_avg_goals_season',
    'avg_goals_against_season' : 'away_avg_goals_against_season',
    'avg_scoring_last_3' : 'away_avg_scoring_last_3',
    'avg_scoring_last_5' : 'away_avg_scoring_last_5',
    'avg_scoring_10' : 'away_avg_scoring_last_10',
    'avg_scoring_season' : 'away_avg_scoring_season',
    'points_last_3' : 'away_points_last_3',
    'points_last_5' : 'away_points_last_5',
    'points_last_10' : 'away_points_last_10'
})


df = df.merge(home_feats, on=['fixture_id', 'home_team'], how='left')
df = df.merge(away_feats, on=['fixture_id', 'away_team'], how='left')



df['scoring_diff_last_3'] = df['home_avg_scoring_last_3'] - df['away_avg_scoring_last_3']
df['scoring_diff_last_5'] = df['home_avg_scoring_last_5'] - df['away_avg_scoring_last_5']
df['scoring_diff_last_10'] = df['home_avg_scoring_last_10'] - df['away_avg_scoring_last_10']
df['scoring_diff_season'] = df['home_avg_scoring_season'] - df['away_avg_scoring_season']

df['points_diff_last_3'] = df['home_points_last_3'] - df['away_points_last_3']
df['points_diff_last_5'] = df['home_points_last_5'] - df['away_points_last_5']
df['points_diff_last_10'] = df['home_points_last_10'] - df['away_points_last_10']





df.to_csv('../data/processed.csv', index=False)
df[:-140].to_csv('../data/train.csv', index=False)
df[-140:].to_csv('../data/test.csv', index=False)