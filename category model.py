import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scikitplot as skplt
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import graphviz
from sklearn.tree import export_graphviz

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'



# create team comp dataframe
"""
matchdata_df = pd.read_csv('full_matchdata.csv')
matchtimeline_df = pd.read_csv('full_matchtimeline.csv')
comp_df = matchdata_df[['gameId',
                            'team1_p1_championId',
                            'team1_p2_championId',
                            'team1_p3_championId',
                            'team1_p4_championId',
                            'team1_p5_championId',
                            'team2_p1_championId',
                            'team2_p2_championId',
                            'team2_p3_championId',
                            'team2_p4_championId',
                            'team2_p5_championId']]

df = pd.merge(comp_df, matchtimeline_df[['gameId', 'game_time']])
champ_df = pd.read_csv('champ_keys.csv')
champ_df['Category'] = champ_df['Champ_Tags'].apply(lambda x: x.split("'")[1])
team1_Fighter, team2_Fighter = pd.Series([]), pd.Series([])
team1_Mage, team2_Mage = pd.Series([]), pd.Series([])
team1_Marksman, team2_Marksman = pd.Series([]), pd.Series([])
team1_Tank, team2_Tank = pd.Series([]), pd.Series([])
team1_Assassin, team2_Assassin = pd.Series([]), pd.Series([])
team1_Support, team2_Support = pd.Series([]), pd.Series([])
for i in range(df.shape[0]):
    print(i)
    game = df.iloc[i]
    t1_comp_lst, t2_comp_lst = [], []
    t1_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team1_p1_championId']]['Category'].values[0])
    t1_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team1_p2_championId']]['Category'].values[0])
    t1_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team1_p3_championId']]['Category'].values[0])
    t1_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team1_p4_championId']]['Category'].values[0])
    t1_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team1_p5_championId']]['Category'].values[0])
    t2_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team2_p1_championId']]['Category'].values[0])
    t2_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team2_p2_championId']]['Category'].values[0])
    t2_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team2_p3_championId']]['Category'].values[0])
    t2_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team2_p4_championId']]['Category'].values[0])
    t2_comp_lst.append(champ_df[champ_df['Champ_Key'] == game['team2_p5_championId']]['Category'].values[0])
    team1_Fighter[i], team2_Fighter[i] = t1_comp_lst.count('Fighter'), t2_comp_lst.count('Fighter')
    team1_Mage[i], team2_Mage[i] = t1_comp_lst.count('Mage'), t2_comp_lst.count('Mage')
    team1_Marksman[i], team2_Marksman[i] = t1_comp_lst.count('Marksman'), t2_comp_lst.count('Marksman')
    team1_Tank[i], team2_Tank[i] = t1_comp_lst.count('Tank'), t2_comp_lst.count('Tank')
    team1_Assassin[i], team2_Assassin[i] = t1_comp_lst.count('Assassin'), t2_comp_lst.count('Assassin')
    team1_Support[i], team2_Support[i] = t1_comp_lst.count('Support'), t2_comp_lst.count('Support')

df['team1_Fighter'] = team1_Fighter
df['team1_Mage'] = team1_Mage
df['team1_Marksman'] = team1_Marksman
df['team1_Tank'] = team1_Tank
df['team1_Assassin'] = team1_Assassin
df['team1_Support'] = team1_Support
df['team2_Fighter'] = team2_Fighter
df['team2_Mage'] = team2_Mage
df['team2_Marksman'] = team2_Marksman
df['team2_Tank'] = team2_Tank
df['team2_Assassin'] = team2_Assassin
df['team2_Support'] = team2_Support
"""
df = pd.read_csv('team_comp.csv', index_col=0)
df['Fighter'] = (df['team1_Fighter'] - df['team2_Fighter']) * df['game_time']
df['Mage'] = (df['team1_Mage'] - df['team2_Mage']) * df['game_time']
df['Marksman'] = (df['team1_Marksman'] - df['team2_Marksman']) * df['game_time']
df['Tank'] = (df['team1_Tank'] - df['team2_Tank']) * df['game_time']
df['Assassin'] = (df['team1_Assassin'] - df['team2_Assassin']) * df['game_time']
df['Support'] = (df['team1_Support'] - df['team2_Support']) * df['game_time']

# df['team1_Fighter'] = df['team1_Fighter'] * df['game_time']
# df['team1_Mage'] = df['team1_Mage'] * df['game_time']
# df['team1_Marksman'] = df['team1_Marksman'] * df['game_time']
# df['team1_Tank'] = df['team1_Tank'] * df['game_time']
# df['team1_Assassin'] = df['team1_Assassin'] * df['game_time']
# df['team1_Support'] = df['team1_Support'] * df['game_time']
# df['team2_Fighter'] = df['team2_Fighter'] * df['game_time']
# df['team2_Mage'] = df['team2_Mage'] * df['game_time']
# df['team2_Marksman'] = df['team2_Marksman'] * df['game_time']
# df['team2_Tank'] = df['team2_Tank'] * df['game_time']
# df['team2_Assassin'] = df['team2_Assassin'] * df['game_time']
# df['team2_Support'] = df['team2_Support'] * df['game_time']

X = df[[
       'team2_Fighter', 'team2_Mage',
       'team2_Marksman', 'team2_Tank', 'team2_Assassin', 'team2_Support']]
y = df['team1_win']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
clf = RandomForestClassifier(n_estimators=200, n_jobs=-1)
clf.fit(X_train, y_train)
y_pred_rf = clf.predict(X_test)
pred_prob = clf.predict_proba(X_test)

xgb = XGBClassifier(silent=False, n_jobs=-1)
xgb.fit(X_train, y_train)
print(xgb.score(X_test, y_test))
#
# dt = DecisionTreeClassifier()
# dt.fit(X_train, y_train)
# y_pred_rf = dt.predict(X_test)
# pred_prob = dt.predict_proba(X_test)


# print(pred_prob)
print(classification_report(y_test, y_pred_rf))
feature_names = list(X.columns)
skplt.estimators.plot_feature_importances(clf, feature_names=feature_names, figsize=(20, 20), x_tick_rotation=90)
plt.show()

