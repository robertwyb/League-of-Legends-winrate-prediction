import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import scikitplot as skplt
from mlxtend.plotting import plot_decision_regions
from mlxtend.plotting import category_scatter
import pickle
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import graphviz
from sklearn.tree import export_graphviz
from sklearn.datasets import make_blobs
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('full_matchtimeline.csv', index_col=0)
df_win = pd.read_csv('game_win.csv', index_col=0)
df_objectives = pd.read_csv('game_objectives.csv', index_col=0)
df_win_timeline = pd.merge(df_objectives, df, on='gameId')

for t in [1, 2]:
    for p in [1, 2, 3, 4, 5]:
        for m in [5, 10, 15, 20, 25, 30]:
            df_win_timeline[f'team{t}_p{p}_total_cs_{m}min'] = df_win_timeline[f'team{t}_p{p}_cs_{m}min'] + \
                                                               df_win_timeline[f'team{t}_p{p}_jg_{m}min']

X = df_win_timeline.drop(columns=['team1_win', 'gameId', 'team2_win',
                                  'team1_p1_jg_5min', 'team1_p1_jg_10min', 'team1_p1_jg_15min', 'team1_p1_jg_20min',
                                  'team1_p1_jg_25min', 'team1_p1_jg_30min',
                                  'team1_p2_jg_5min', 'team1_p2_jg_10min', 'team1_p2_jg_15min', 'team1_p2_jg_20min',
                                  'team1_p2_jg_25min', 'team1_p2_jg_30min',
                                  'team1_p3_jg_5min', 'team1_p3_jg_10min', 'team1_p3_jg_15min', 'team1_p3_jg_20min',
                                  'team1_p3_jg_25min', 'team1_p3_jg_30min',
                                  'team1_p4_jg_5min', 'team1_p4_jg_10min', 'team1_p4_jg_15min', 'team1_p4_jg_20min',
                                  'team1_p4_jg_25min', 'team1_p4_jg_30min',
                                  'team1_p5_jg_5min', 'team1_p5_jg_10min', 'team1_p5_jg_15min', 'team1_p5_jg_20min',
                                  'team1_p5_jg_25min', 'team1_p5_jg_30min',
                                  'team2_p1_jg_5min', 'team2_p1_jg_10min', 'team2_p1_jg_15min', 'team2_p1_jg_20min',
                                  'team2_p1_jg_25min', 'team2_p1_jg_30min',
                                  'team2_p2_jg_5min', 'team2_p2_jg_10min', 'team2_p2_jg_15min', 'team2_p2_jg_20min',
                                  'team2_p2_jg_25min', 'team2_p2_jg_30min',
                                  'team2_p3_jg_5min', 'team2_p3_jg_10min', 'team2_p3_jg_15min', 'team2_p3_jg_20min',
                                  'team2_p3_jg_25min', 'team2_p3_jg_30min',
                                  'team2_p4_jg_5min', 'team2_p4_jg_10min', 'team2_p4_jg_15min', 'team2_p4_jg_20min',
                                  'team2_p4_jg_25min', 'team2_p4_jg_30min',
                                  'team2_p5_jg_5min', 'team2_p5_jg_10min', 'team2_p5_jg_15min', 'team2_p5_jg_20min',
                                  'team2_p5_jg_25min', 'team2_p5_jg_30min',
                                  'team1_p1_cs_5min', 'team1_p1_cs_10min', 'team1_p1_cs_15min', 'team1_p1_cs_20min',
                                  'team1_p1_cs_25min', 'team1_p1_cs_30min',
                                  'team1_p2_cs_5min', 'team1_p2_cs_10min', 'team1_p2_cs_15min', 'team1_p2_cs_20min',
                                  'team1_p2_cs_25min', 'team1_p2_cs_30min',
                                  'team1_p3_cs_5min', 'team1_p3_cs_10min', 'team1_p3_cs_15min', 'team1_p3_cs_20min',
                                  'team1_p3_cs_25min', 'team1_p3_cs_30min',
                                  'team1_p4_cs_5min', 'team1_p4_cs_10min', 'team1_p4_cs_15min', 'team1_p4_cs_20min',
                                  'team1_p4_cs_25min', 'team1_p4_cs_30min',
                                  'team1_p5_cs_5min', 'team1_p5_cs_10min', 'team1_p5_cs_15min', 'team1_p5_cs_20min',
                                  'team1_p5_cs_25min', 'team1_p5_cs_30min',
                                  'team2_p1_cs_5min', 'team2_p1_cs_10min', 'team2_p1_cs_15min', 'team2_p1_cs_20min',
                                  'team2_p1_cs_25min', 'team2_p1_cs_30min',
                                  'team2_p2_cs_5min', 'team2_p2_cs_10min', 'team2_p2_cs_15min', 'team2_p2_cs_20min',
                                  'team2_p2_cs_25min', 'team2_p2_cs_30min',
                                  'team2_p3_cs_5min', 'team2_p3_cs_10min', 'team2_p3_cs_15min', 'team2_p3_cs_20min',
                                  'team2_p3_cs_25min', 'team2_p3_cs_30min',
                                  'team2_p4_cs_5min', 'team2_p4_cs_10min', 'team2_p4_cs_15min', 'team2_p4_cs_20min',
                                  'team2_p4_cs_25min', 'team2_p4_cs_30min',
                                  'team2_p5_cs_5min', 'team2_p5_cs_10min', 'team2_p5_cs_15min', 'team2_p5_cs_20min',
                                  'team2_p5_cs_25min', 'team2_p5_cs_30min',
                                  'team1_p1_xp_5min', 'team1_p1_xp_10min', 'team1_p1_xp_15min', 'team1_p1_xp_20min',
                                  'team1_p1_xp_25min', 'team1_p1_xp_30min',
                                  'team1_p2_xp_5min', 'team1_p2_xp_10min', 'team1_p2_xp_15min', 'team1_p2_xp_20min',
                                  'team1_p2_xp_25min', 'team1_p2_xp_30min',
                                  'team1_p3_xp_5min', 'team1_p3_xp_10min', 'team1_p3_xp_15min', 'team1_p3_xp_20min',
                                  'team1_p3_xp_25min', 'team1_p3_xp_30min',
                                  'team1_p4_xp_5min', 'team1_p4_xp_10min', 'team1_p4_xp_15min', 'team1_p4_xp_20min',
                                  'team1_p4_xp_25min', 'team1_p4_xp_30min',
                                  'team1_p5_xp_5min', 'team1_p5_xp_10min', 'team1_p5_xp_15min', 'team1_p5_xp_20min',
                                  'team1_p5_xp_25min', 'team1_p5_xp_30min',
                                  'team2_p1_xp_5min', 'team2_p1_xp_10min', 'team2_p1_xp_15min', 'team2_p1_xp_20min',
                                  'team2_p1_xp_25min', 'team2_p1_xp_30min',
                                  'team2_p2_xp_5min', 'team2_p2_xp_10min', 'team2_p2_xp_15min', 'team2_p2_xp_20min',
                                  'team2_p2_xp_25min', 'team2_p2_xp_30min',
                                  'team2_p3_xp_5min', 'team2_p3_xp_10min', 'team2_p3_xp_15min', 'team2_p3_xp_20min',
                                  'team2_p3_xp_25min', 'team2_p3_xp_30min',
                                  'team2_p4_xp_5min', 'team2_p4_xp_10min', 'team2_p4_xp_15min', 'team2_p4_xp_20min',
                                  'team2_p4_xp_25min', 'team2_p4_xp_30min',
                                  'team2_p5_xp_5min', 'team2_p5_xp_10min', 'team2_p5_xp_15min', 'team2_p5_xp_20min',
                                  'team2_p5_xp_25min', 'team2_p5_xp_30min',
                                  'team1_p1_level_5min', 'team1_p1_level_10min', 'team1_p1_level_15min',
                                  'team1_p1_level_20min', 'team1_p1_level_25min', 'team1_p1_level_30min',
                                  'team1_p2_level_5min', 'team1_p2_level_10min', 'team1_p2_level_15min',
                                  'team1_p2_level_20min', 'team1_p2_level_25min', 'team1_p2_level_30min',
                                  'team1_p3_level_5min', 'team1_p3_level_10min', 'team1_p3_level_15min',
                                  'team1_p3_level_20min', 'team1_p3_level_25min', 'team1_p3_level_30min',
                                  'team1_p4_level_5min', 'team1_p4_level_10min', 'team1_p4_level_15min',
                                  'team1_p4_level_20min', 'team1_p4_level_25min', 'team1_p4_level_30min',
                                  'team1_p5_level_5min', 'team1_p5_level_10min', 'team1_p5_level_15min',
                                  'team1_p5_level_20min', 'team1_p5_level_25min', 'team1_p5_level_30min',
                                  'team2_p1_level_5min', 'team2_p1_level_10min', 'team2_p1_level_15min',
                                  'team2_p1_level_20min', 'team2_p1_level_25min', 'team2_p1_level_30min',
                                  'team2_p2_level_5min', 'team2_p2_level_10min', 'team2_p2_level_15min',
                                  'team2_p2_level_20min', 'team2_p2_level_25min', 'team2_p2_level_30min',
                                  'team2_p3_level_5min', 'team2_p3_level_10min', 'team2_p3_level_15min',
                                  'team2_p3_level_20min', 'team2_p3_level_25min', 'team2_p3_level_30min',
                                  'team2_p4_level_5min', 'team2_p4_level_10min', 'team2_p4_level_15min',
                                  'team2_p4_level_20min', 'team2_p4_level_25min', 'team2_p4_level_30min',
                                  'team2_p5_level_5min', 'team2_p5_level_10min', 'team2_p5_level_15min',
                                  'team2_p5_level_20min', 'team2_p5_level_25min', 'team2_p5_level_30min'
                                  ])
y = df_win_timeline['team1_win']

# def get_data_before_x_min(data, x):
#     minutes_5 =
#     data.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]

X_train, X_test, y_train, y_test = train_test_split \
    (X, y, test_size=0.3, random_state=2019)
xgb_cls = xgb.XGBClassifier(objective='reg:linear', colsample_bytree=0.3, learning_rate=0.1,
                            max_depth=10, alpha=10, n_estimators=10)

xgb_cls.fit(X_train, y_train)
y_pred_xgb = xgb_cls.predict(X_test)
print(classification_report(y_test, y_pred_xgb))
pred_prob_xgb = xgb_cls.predict_proba(X_test)
print(pred_prob_xgb)
feature_importance_xgb = list(xgb_cls.feature_importances_)
print(feature_importance_xgb)


def get_feature_importance_greater_than(n):
    feature_importance_xgb_1 = []
    for i in range(len(feature_importance_xgb)):
        if feature_importance_xgb[i] > n:
            feature_importance_xgb_1.append([list(X.columns)[i], feature_importance_xgb[i]])
    feature_importance_xgb_1.sort(key=lambda x: x[1], reverse=True)
    feature_importance_xgb_2 = np.array(feature_importance_xgb_1, dtype=object)
    plt.bar(range(len(list(feature_importance_xgb_2[:, 0]))), list(feature_importance_xgb_2[:, 1]))
    plt.xticks(range(len(list(feature_importance_xgb_2[:, 0]))), list(feature_importance_xgb_2[:, 0]))
    plt.xticks(rotation=90)
    plt.show()


get_feature_importance_greater_than(0.01)

filename = 'finalized_model_2.sav'
pickle.dump(xgb_cls, open(filename, 'wb'))

# dt = DecisionTreeClassifier()
# dt.fit(X_train, y_train)
# y_pred_dt = dt.predict(X_test)
# print(classification_report(y_test, y_pred_dt))
#
# rf = RandomForestClassifier()
# rf.fit(X_train, y_train)
# y_pred_rf = rf.predict(X_test)
# pred_prob = rf.predict_proba(X_test)
# print(pred_prob)
# print(classification_report(y_test, y_pred_rf))
# feature_names = list(df_champ_select.columns)
# skplt.estimators.plot_feature_importances(rf, feature_names=feature_names, figsize=(20, 20), x_tick_rotation=90)
# plt.show()
# plt.savefig('feature')
