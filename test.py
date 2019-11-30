# import numpy as np
import pandas as pd
#
# import matplotlib.pyplot as plt
#
# import scikitplot as skplt
# from mlxtend.plotting import plot_decision_regions
# from mlxtend.plotting import category_scatter
#
#
# import graphviz
# from sklearn.tree import export_graphviz
# from sklearn.datasets import make_blobs
# from sklearn.datasets import make_moons
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.svm import SVC
# from sklearn.model_selection import train_test_split
# from sklearn.datasets import load_breast_cancer
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import precision_score, recall_score, accuracy_score
# from sklearn.ensemble import RandomForestClassifier
#
# df = pd.read_csv('match_test0.csv')
#
#
# def get_numeric_columns(data):
#     df_new = data
#     for i in range(len(data.dtypes)):
#         if data.dtypes[i] == object:
#             df_new = df_new.drop(columns=data.columns[i])
#     return df_new
#
#
# def get_notnull_columns(data):
#     df_new = data
#     for i in range(len(data.columns)):
#         if data.isnull().sum()[i] != 0:
#             df_new = df_new.drop(columns=data.columns[i])
#     return df_new
#
#
# df_1 = get_notnull_columns(get_numeric_columns(df))
# X = df_1.drop(columns=['team2_win', 'team1_win'])
# y = df_1['team1_win']
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2019)
#
#
# dt = DecisionTreeClassifier()
# dt.fit(X_train, y_train)
# y_pred_dt = dt.predict(X_test)
# print(classification_report(y_test, y_pred_dt))
#
# rf = RandomForestClassifier()
# rf.fit(X_train, y_train)
# y_pred_rf = rf.predict(X_test)
# print(classification_report(y_test, y_pred_rf))
# feature_names = list(X.columns)
# skplt.estimators.plot_feature_importances(rf, feature_names=feature_names, figsize=(20, 20), x_tick_rotation=90)
# # plt.show()
# plt.savefig('feature')

df = pd.read_csv('champ_select.csv', index_col=0)
print(df.head())

