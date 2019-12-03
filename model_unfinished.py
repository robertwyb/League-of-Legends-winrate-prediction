import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import scikitplot as skplt
from mlxtend.plotting import plot_decision_regions
from mlxtend.plotting import category_scatter

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

df = pd.read_csv('full_matchdata.csv')


def get_numeric_columns(data):
    df_new = data
    for i in range(len(data.dtypes)):
        if data.dtypes[i] == object:
            df_new = df_new.drop(columns=data.columns[i])
    return df_new


def get_notnull_columns(data):
    df_new = data
    for i in range(len(data.columns)):
        if data.isnull().sum()[i] != 0:
            df_new = df_new.drop(columns=data.columns[i])
    return df_new


df_1 = df[['team1_win', 'team2_win',
           'team1_baronKills', 'team1_riftKills', 'team1_inhibitorKills', 'team1_towerKills', 'team1_dragonKills',
           'team2_baronKills', 'team2_riftKills', 'team2_inhibitorKills', 'team2_towerKills', 'team2_dragonKills',
           'team1_p1_cs_permin0', 'team1_p1_cs_permin1', 'team1_p1_cs_permin2', 'team1_p1_cs_permin3',
           'team1_p2_cs_permin0', 'team1_p2_cs_permin1', 'team1_p2_cs_permin2', 'team1_p2_cs_permin3',
           'team1_p3_cs_permin0', 'team1_p3_cs_permin1', 'team1_p3_cs_permin2', 'team1_p3_cs_permin3',
           'team1_p4_cs_permin0', 'team1_p4_cs_permin1', 'team1_p4_cs_permin2', 'team1_p4_cs_permin3',
           'team1_p5_xp_permin0', 'team1_p5_xp_permin1', 'team1_p5_xp_permin2', 'team1_p5_xp_permin3',
           'team1_p1_xp_permin0', 'team1_p1_xp_permin1', 'team1_p1_xp_permin2', 'team1_p1_xp_permin3',
           'team1_p2_xp_permin0', 'team1_p2_xp_permin1', 'team1_p2_xp_permin2', 'team1_p2_xp_permin3',
           'team1_p3_xp_permin0', 'team1_p3_xp_permin1', 'team1_p3_xp_permin2', 'team1_p3_xp_permin3',
           'team1_p4_xp_permin0', 'team1_p4_xp_permin1', 'team1_p4_xp_permin2', 'team1_p4_xp_permin3',
           'team1_p5_xp_permin0', 'team1_p5_xp_permin1', 'team1_p5_xp_permin2', 'team1_p5_xp_permin3',
           'team2_p1_kills', 'team2_p1_assists', 'team2_p1_deaths',
           'team2_p2_kills', 'team2_p2_assists', 'team2_p2_deaths',
           'team2_p3_kills', 'team2_p3_assists', 'team2_p3_deaths',
           'team2_p4_kills', 'team2_p4_assists', 'team2_p4_deaths',
           'team2_p5_kills', 'team2_p5_assists', 'team2_p5_deaths',
           'team2_p1_kills', 'team2_p1_assists', 'team2_p1_deaths',
           'team2_p2_kills', 'team2_p2_assists', 'team2_p2_deaths',
           'team2_p3_kills', 'team2_p3_assists', 'team2_p3_deaths',
           'team2_p4_kills', 'team2_p4_assists', 'team2_p4_deaths',
           'team2_p5_kills', 'team2_p5_assists', 'team2_p5_deaths']]

# df_2 = get_notnull_columns(get_numeric_columns(df_1))
df_2 = df_1
X = df_2.drop(columns=['team2_win', 'team1_win'])
y = df_2['team1_win']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2019)

dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
print(classification_report(y_test, y_pred_dt))

lr = LogisticRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
pred_prob_lr = lr.predict_proba(X_test)
print(pred_prob_lr)
print(classification_report(y_test, y_pred_lr))

rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print(classification_report(y_test, y_pred_rf))
feature_names = list(X.columns)
skplt.estimators.plot_feature_importances(rf, feature_names=feature_names, figsize=(20, 20), x_tick_rotation=90)
plt.show()
# plt.savefig('feature')
