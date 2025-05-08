import pandas as pd
import pickle

## DataFrame

df = pd.read_csv('../data/processed.csv')

df['date'] = pd.to_datetime(df['date'])
df.drop(columns=['fixture_id','home_team_id','away_team_id','home_score','away_score','league_season','home_result'], inplace=True)



## Modelo
 
modelo = pickle.load(open("../models/model_model.pkl", 'rb'))



## Funcion de Prediccion

def predict(home_team,away_team, date):
    global df, modelo

    date = pd.to_datetime(date)

    n_df = df.copy()
    n_modelo = modelo

    data = pd.DataFrame({
        'date' : [date],
        'home_team': [home_team],
        'away_team': [away_team]
    })

    ## Añadiendo los nuevos datos al DataFrame

    n_df = pd.concat([n_df,data],axis='rows')
    n_df = n_df.reset_index().drop(columns='index')


    ## Ordenando los datos

    n_df = n_df.sort_values('date').reset_index(drop=True)


    new_entry_index = n_df[(n_df['home_team'] == home_team) & (n_df['away_team'] == away_team) & (n_df['date'] == date)].index[0]

    n_df = n_df.iloc[new_entry_index :new_entry_index + 26]

    

    ## HOME

    home_df = n_df[n_df['home_team'] == home_team]
    home_col_list = ['home_avg_goals_last_3','home_avg_goals_against_last_3','home_avg_goals_last_5','home_avg_goals_against_last_5','home_avg_goals_last_10','home_avg_goals_against_last_10','home_avg_goals_season','home_avg_goals_against_season','home_avg_scoring_last_3','home_avg_scoring_last_5','home_avg_scoring_last_10','home_avg_scoring_season','home_points_last_3','home_points_last_5','home_points_last_10']
    n_df.loc[home_df.index[0], home_col_list] = home_df.loc[home_df.index[1], home_col_list].values



    ## AWAY

    away_df = n_df[n_df['away_team'] == away_team]
    away_col_list = ['away_avg_goals_last_3','away_avg_goals_against_last_3','away_avg_goals_last_5','away_avg_goals_against_last_5','away_avg_goals_last_10','away_avg_goals_against_last_10','away_avg_goals_season','away_avg_goals_against_season','away_avg_scoring_last_3','away_avg_scoring_last_5','away_avg_scoring_last_10','away_avg_scoring_season','away_points_last_3','away_points_last_5','away_points_last_10']
    n_df.loc[away_df.index[0], away_col_list] = away_df.loc[away_df.index[1], away_col_list].values


    to_predict = n_df[:1].copy()


    ## Calculating new values


    to_predict['scoring_diff_last_3'] = to_predict['home_avg_scoring_last_3'] - to_predict['away_avg_scoring_last_3']
    to_predict['scoring_diff_last_5'] = to_predict['home_avg_scoring_last_5'] - to_predict['away_avg_scoring_last_5']
    to_predict['scoring_diff_last_10'] = to_predict['home_avg_scoring_last_10'] - to_predict['away_avg_scoring_last_10']
    to_predict['scoring_diff_season'] = to_predict['home_avg_scoring_season'] - to_predict['away_avg_scoring_season']

    to_predict['points_diff_last_3'] = to_predict['home_points_last_3'] - to_predict['away_points_last_3']
    to_predict['points_diff_last_5'] = to_predict['home_points_last_5'] - to_predict['away_points_last_5']
    to_predict['points_diff_last_10'] = to_predict['home_points_last_10'] - to_predict['away_points_last_10']



    ## Prediction

    predictions = n_modelo.predict_proba(to_predict.drop(columns=['home_team', 'away_team','date']))

    results = (predictions*100).round(1)



    return results[0]