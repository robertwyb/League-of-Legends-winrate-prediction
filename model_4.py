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

#
# df = pd.read_csv('full_matchtimeline.csv', index_col=0)
# df_cs = pd.read_csv('champ_select.csv', index_col=0)
# df_win = pd.read_csv('game_win.csv', index_col=0)
# df_objectives = pd.read_csv('game_objectives.csv', index_col=0)
# df_champ_select = df_cs.drop(columns=['game_time', 'team1_win', 'gameId']).multiply(df_cs['game_time'], axis='index')
# df_champ_select['gameId'] = df_cs['gameId']
# df_win_time = pd.merge(df_objectives, df, on='gameId')
# df_win_timeline = pd.merge(df_win_time, df_champ_select, on='gameId')
# for t_1 in [1, 2]:
#     for p_1 in [1, 2, 3, 4, 5]:
#         for m_1 in [5, 10, 15, 20, 25, 30]:
#             df_win_timeline[f'team{t_1}_p{p_1}_total_cs_{m_1}min'] = df_win_timeline[f'team{t_1}_p{p_1}_cs_{m_1}min'] +\
#                                                                df_win_timeline[f'team{t_1}_p{p_1}_jg_{m_1}min']
#
#
# X = df_win_timeline.drop(columns=['team1_win', 'gameId', 'team2_win',
#                                   'team1_p1_jg_5min', 'team1_p1_jg_10min', 'team1_p1_jg_15min', 'team1_p1_jg_20min',
#                                   'team1_p1_jg_25min', 'team1_p1_jg_30min',
#                                   'team1_p2_jg_5min', 'team1_p2_jg_10min', 'team1_p2_jg_15min', 'team1_p2_jg_20min',
#                                   'team1_p2_jg_25min', 'team1_p2_jg_30min',
#                                   'team1_p3_jg_5min', 'team1_p3_jg_10min', 'team1_p3_jg_15min', 'team1_p3_jg_20min',
#                                   'team1_p3_jg_25min', 'team1_p3_jg_30min',
#                                   'team1_p4_jg_5min', 'team1_p4_jg_10min', 'team1_p4_jg_15min', 'team1_p4_jg_20min',
#                                   'team1_p4_jg_25min', 'team1_p4_jg_30min',
#                                   'team1_p5_jg_5min', 'team1_p5_jg_10min', 'team1_p5_jg_15min', 'team1_p5_jg_20min',
#                                   'team1_p5_jg_25min', 'team1_p5_jg_30min',
#                                   'team2_p1_jg_5min', 'team2_p1_jg_10min', 'team2_p1_jg_15min', 'team2_p1_jg_20min',
#                                   'team2_p1_jg_25min', 'team2_p1_jg_30min',
#                                   'team2_p2_jg_5min', 'team2_p2_jg_10min', 'team2_p2_jg_15min', 'team2_p2_jg_20min',
#                                   'team2_p2_jg_25min', 'team2_p2_jg_30min',
#                                   'team2_p3_jg_5min', 'team2_p3_jg_10min', 'team2_p3_jg_15min', 'team2_p3_jg_20min',
#                                   'team2_p3_jg_25min', 'team2_p3_jg_30min',
#                                   'team2_p4_jg_5min', 'team2_p4_jg_10min', 'team2_p4_jg_15min', 'team2_p4_jg_20min',
#                                   'team2_p4_jg_25min', 'team2_p4_jg_30min',
#                                   'team2_p5_jg_5min', 'team2_p5_jg_10min', 'team2_p5_jg_15min', 'team2_p5_jg_20min',
#                                   'team2_p5_jg_25min', 'team2_p5_jg_30min',
#                                   'team1_p1_cs_5min', 'team1_p1_cs_10min', 'team1_p1_cs_15min', 'team1_p1_cs_20min',
#                                   'team1_p1_cs_25min', 'team1_p1_cs_30min',
#                                   'team1_p2_cs_5min', 'team1_p2_cs_10min', 'team1_p2_cs_15min', 'team1_p2_cs_20min',
#                                   'team1_p2_cs_25min', 'team1_p2_cs_30min',
#                                   'team1_p3_cs_5min', 'team1_p3_cs_10min', 'team1_p3_cs_15min', 'team1_p3_cs_20min',
#                                   'team1_p3_cs_25min', 'team1_p3_cs_30min',
#                                   'team1_p4_cs_5min', 'team1_p4_cs_10min', 'team1_p4_cs_15min', 'team1_p4_cs_20min',
#                                   'team1_p4_cs_25min', 'team1_p4_cs_30min',
#                                   'team1_p5_cs_5min', 'team1_p5_cs_10min', 'team1_p5_cs_15min', 'team1_p5_cs_20min',
#                                   'team1_p5_cs_25min', 'team1_p5_cs_30min',
#                                   'team2_p1_cs_5min', 'team2_p1_cs_10min', 'team2_p1_cs_15min', 'team2_p1_cs_20min',
#                                   'team2_p1_cs_25min', 'team2_p1_cs_30min',
#                                   'team2_p2_cs_5min', 'team2_p2_cs_10min', 'team2_p2_cs_15min', 'team2_p2_cs_20min',
#                                   'team2_p2_cs_25min', 'team2_p2_cs_30min',
#                                   'team2_p3_cs_5min', 'team2_p3_cs_10min', 'team2_p3_cs_15min', 'team2_p3_cs_20min',
#                                   'team2_p3_cs_25min', 'team2_p3_cs_30min',
#                                   'team2_p4_cs_5min', 'team2_p4_cs_10min', 'team2_p4_cs_15min', 'team2_p4_cs_20min',
#                                   'team2_p4_cs_25min', 'team2_p4_cs_30min',
#                                   'team2_p5_cs_5min', 'team2_p5_cs_10min', 'team2_p5_cs_15min', 'team2_p5_cs_20min',
#                                   'team2_p5_cs_25min', 'team2_p5_cs_30min',
#                                   'team1_p1_xp_5min', 'team1_p1_xp_10min', 'team1_p1_xp_15min', 'team1_p1_xp_20min',
#                                   'team1_p1_xp_25min', 'team1_p1_xp_30min',
#                                   'team1_p2_xp_5min', 'team1_p2_xp_10min', 'team1_p2_xp_15min', 'team1_p2_xp_20min',
#                                   'team1_p2_xp_25min', 'team1_p2_xp_30min',
#                                   'team1_p3_xp_5min', 'team1_p3_xp_10min', 'team1_p3_xp_15min', 'team1_p3_xp_20min',
#                                   'team1_p3_xp_25min', 'team1_p3_xp_30min',
#                                   'team1_p4_xp_5min', 'team1_p4_xp_10min', 'team1_p4_xp_15min', 'team1_p4_xp_20min',
#                                   'team1_p4_xp_25min', 'team1_p4_xp_30min',
#                                   'team1_p5_xp_5min', 'team1_p5_xp_10min', 'team1_p5_xp_15min', 'team1_p5_xp_20min',
#                                   'team1_p5_xp_25min', 'team1_p5_xp_30min',
#                                   'team2_p1_xp_5min', 'team2_p1_xp_10min', 'team2_p1_xp_15min', 'team2_p1_xp_20min',
#                                   'team2_p1_xp_25min', 'team2_p1_xp_30min',
#                                   'team2_p2_xp_5min', 'team2_p2_xp_10min', 'team2_p2_xp_15min', 'team2_p2_xp_20min',
#                                   'team2_p2_xp_25min', 'team2_p2_xp_30min',
#                                   'team2_p3_xp_5min', 'team2_p3_xp_10min', 'team2_p3_xp_15min', 'team2_p3_xp_20min',
#                                   'team2_p3_xp_25min', 'team2_p3_xp_30min',
#                                   'team2_p4_xp_5min', 'team2_p4_xp_10min', 'team2_p4_xp_15min', 'team2_p4_xp_20min',
#                                   'team2_p4_xp_25min', 'team2_p4_xp_30min',
#                                   'team2_p5_xp_5min', 'team2_p5_xp_10min', 'team2_p5_xp_15min', 'team2_p5_xp_20min',
#                                   'team2_p5_xp_25min', 'team2_p5_xp_30min',
#                                   'team1_p1_level_5min', 'team1_p1_level_10min', 'team1_p1_level_15min',
#                                   'team1_p1_level_20min', 'team1_p1_level_25min', 'team1_p1_level_30min',
#                                   'team1_p2_level_5min', 'team1_p2_level_10min', 'team1_p2_level_15min',
#                                   'team1_p2_level_20min', 'team1_p2_level_25min', 'team1_p2_level_30min',
#                                   'team1_p3_level_5min', 'team1_p3_level_10min', 'team1_p3_level_15min',
#                                   'team1_p3_level_20min', 'team1_p3_level_25min', 'team1_p3_level_30min',
#                                   'team1_p4_level_5min', 'team1_p4_level_10min', 'team1_p4_level_15min',
#                                   'team1_p4_level_20min', 'team1_p4_level_25min', 'team1_p4_level_30min',
#                                   'team1_p5_level_5min', 'team1_p5_level_10min', 'team1_p5_level_15min',
#                                   'team1_p5_level_20min', 'team1_p5_level_25min', 'team1_p5_level_30min',
#                                   'team2_p1_level_5min', 'team2_p1_level_10min', 'team2_p1_level_15min',
#                                   'team2_p1_level_20min', 'team2_p1_level_25min', 'team2_p1_level_30min',
#                                   'team2_p2_level_5min', 'team2_p2_level_10min', 'team2_p2_level_15min',
#                                   'team2_p2_level_20min', 'team2_p2_level_25min', 'team2_p2_level_30min',
#                                   'team2_p3_level_5min', 'team2_p3_level_10min', 'team2_p3_level_15min',
#                                   'team2_p3_level_20min', 'team2_p3_level_25min', 'team2_p3_level_30min',
#                                   'team2_p4_level_5min', 'team2_p4_level_10min', 'team2_p4_level_15min',
#                                   'team2_p4_level_20min', 'team2_p4_level_25min', 'team2_p4_level_30min',
#                                   'team2_p5_level_5min', 'team2_p5_level_10min', 'team2_p5_level_15min',
#                                   'team2_p5_level_20min', 'team2_p5_level_25min', 'team2_p5_level_30min'
#                                   ])
# y = df_win_timeline['team1_win']


def drop_gold_cs_columns_before_k_min(k, train_set):
    """
    :param k: in minutes less than 30
    :param train_set: data frame of features
    :return: new data frame of features
    """
    x_new = train_set
    for t in [1, 2]:
        for p in range(1, 6):
            for m in range((k // 5) * 5 + 5, 31, 5):
                x_new = x_new.drop(columns=[f'team{t}_p{p}_total_cs_{m}min', f'team{t}_p{p}_gold_{m}min'])
    return x_new


# def lr_based_on_time(x_1, y_1, k, s=0.3, r=42):
#     """
#     :param x_1: feature set
#     :param y_1: label set
#     :param k: time
#     :param r: random state
#     :param s: test size
#     :return: probability and report
#     """
#     x_2 = drop_gold_cs_columns_before_k_min(k, x_1)
#     df_concat = pd.concat([x_2, y_1], axis=1)
#     df_concat = df_concat.dropna()
#     x_new = df_concat.drop(columns=['team1_win'])
#     y_new = df_concat['team1_win']
#     x_train, x_test, y_train, y_test = train_test_split(x_new, y_new, test_size=s, random_state=r)
#     lr = LogisticRegression()
#     lr.fit(x_train, y_train)
#     y_pred_rf = lr.predict(x_test)
#     pred_prob = lr.predict_proba(x_test)
#     return pred_prob, classification_report(y_test, y_pred_rf)
# print(lr_based_on_time(X, y, 11))


def lr_based_on_time(x_1, y_1, k, s=0.3, r=42):
    """
    :param x_1: feature set
    :param y_1: label set
    :param k: time
    :param r: random state
    :param s: test size
    :return: probability and report
    """
    x_2 = drop_gold_cs_columns_before_k_min(k, x_1)
    df_concat = pd.concat([x_2, y_1], axis=1)
    df_concat = df_concat.dropna()
    x_new = df_concat.drop(columns=['team1_win'])
    y_new = df_concat['team1_win']
    lr = LogisticRegression()
    lr.fit(x_new, y_new)
    filename = f'lrmodel_{k-1}.sav'
    pickle.dump(lr, open(filename, 'wb'))
    return lr


# lr_based_on_time(X, y, 6)
# lr_based_on_time(X, y, 11)
# lr_based_on_time(X, y, 16)
# lr_based_on_time(X, y, 21)
# lr_based_on_time(X, y, 26)
# lr_based_on_time(X, y, 31)