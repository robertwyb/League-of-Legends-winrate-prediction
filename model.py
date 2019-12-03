import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import scikitplot as skplt
from mlxtend.plotting import plot_decision_regions
from mlxtend.plotting import category_scatter
import pickle

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


df_cs = pd.read_csv('champ_select.csv', index_col=0)

df_champ_select = df_cs.drop(columns=['gameId', 'game_time', 'team1_win']).multiply(df_cs['game_time'], axis='index')
df_t1_win = df_cs['team1_win']


df_champ_keys = pd.read_csv('champ_keys.csv')
df_champ_keys_new = df_champ_keys[['Champ_Name', 'Champ_Key']]


X_train, X_test, y_train, y_test = train_test_split\
        (df_champ_select, df_t1_win, test_size=0.3, random_state=201)
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
print(classification_report(y_test, y_pred_dt))


lr = LogisticRegression()
lr.fit(X_train, y_train)
y_pred_rf = lr.predict(X_test)
pred_prob = lr.predict_proba(X_test)
print(pred_prob)
print(classification_report(y_test, y_pred_rf))

filename = 'finalized_model_1_lr.sav'
pickle.dump(lr, open(filename, 'wb'))


rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
pred_prob = rf.predict_proba(X_test)
print(pred_prob)
print(classification_report(y_test, y_pred_rf))
feature_names = list(df_champ_select.columns)
skplt.estimators.plot_feature_importances(rf, feature_names=feature_names, figsize=(20, 20), x_tick_rotation=90)
plt.show()
# plt.savefig('feature')