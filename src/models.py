import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


train = pd.read_csv('../data/train.csv')
test = pd.read_csv('../data/test.csv')



X = train.drop(columns=['fixture_id','date','home_team','home_team_id','away_team','away_team_id','home_score','away_score','league_season','home_result'])
# X = train[['scoring_diff_last_3','scoring_diff_last_5','scoring_diff_last_10','scoring_diff_season','points_diff_last_3','points_diff_last_5','points_diff_last_10']]
y = train['home_result']


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=20, random_state=42)



pipe = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])
pipe



rf_params = {
    'scaler': [StandardScaler(), MinMaxScaler(), None],
    'classifier__max_depth': np.arange(2,10),
    'classifier__min_samples_leaf': np.arange(2,15)
}

xgb_params = {
    'classifier' : [XGBClassifier()],
    'scaler': [StandardScaler(), MinMaxScaler(), None],
    'classifier__max_depth': np.arange(2,10),
    'classifier__min_samples_leaf': np.arange(2,15),
    # 'classifier__learning_rate': [0.05, 0.1, 0.2],
    # 'classifier__subsample': [0.8, 1.0],
    # 'classifier__colsample_bytree': [0.8, 1.0],
    # 'classifier__gamma': [0, 1],
    # 'classifier__min_child_weight': [1, 5],
    # 'classifier__reg_alpha': [0, 0.1],
    # 'classifier__reg_lambda': [1, 2],
}

search = [rf_params, xgb_params]


gs = GridSearchCV(pipe, search,scoring='accuracy', cv=10,n_jobs=-1)
gs.fit(X_train,y_train)


h_model = gs.best_estimator_


feat_importance = h_model.named_steps['classifier'].feature_importances_

pd.DataFrame({
    'Feature': X.columns,
    "importance": feat_importance
})


test_pred = h_model.predict(test.drop(columns=['fixture_id','date','home_team','home_team_id','away_team','away_team_id','home_score','away_score','league_season','home_result']))


pickle.dump(h_model, open('../models/model_model.pkl', 'wb'))