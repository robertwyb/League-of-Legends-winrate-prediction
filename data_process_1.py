import pandas as pd

df = pd.read_csv('full_matchdata.csv', index_col=0)
df_mtl = pd.read_csv('full_matchtimeline.csv', index_col=0)
df_match_timeline = df_mtl[['gameId', 'game_time']]
df_col = list(df.columns)

df_t1_champ = df[['team1_p1_championId', 'team1_p2_championId', 'team1_p3_championId', 'team1_p4_championId',
                  'team1_p5_championId']]
df_t2_champ = df[['team2_p1_championId', 'team2_p2_championId', 'team2_p3_championId', 'team2_p4_championId',
                  'team2_p5_championId']]
df_t1_win = df['team1_win']

df_champ_keys = pd.read_csv('champ_keys.csv')
# df_champ_keys_new = df_champ_keys[['Champ_Name', 'Champ_Key']]

champ_names = list(df_champ_keys['Champ_Name'])
champ_keys = list(df_champ_keys['Champ_Key'])
champ_index = list()

'''create a dict of each matches
champions as column names
1 stands for team1 having this champion
-1 stands for team2 having this champion
0 stands for both or neither team have this champion'''
champ_picks = {}
for i in range(len(df_t1_win)):
    lst = [0] * len(champ_names)
    for key1 in df_t1_champ.loc[i]:
        index1 = champ_keys.index(key1)
        lst[index1] += 1
    for key2 in df_t2_champ.loc[i]:
        index2 = champ_keys.index(key2)
        lst[index2] -= 1
    champ_picks[i] = lst

df_team1_win = df[['gameId', 'team1_win']]
df_c = pd.DataFrame.from_dict(champ_picks, orient='index', columns=champ_names)
df_champ = pd.concat([df_c, df_team1_win], axis=1)
df_champ_select = pd.merge(df_champ, df_match_timeline, on='gameId')
df_champ_select.to_csv('champ_select.csv')

df_win = df[['gameId', 'team1_win', 'team2_win']]
df_win.to_csv('game_win.csv')

df_objectives = df[['gameId', 'team1_win', 'team2_win', 'team1_baronKills', 'team1_riftKills', 'team1_inhibitorKills',
                    'team1_towerKills', 'team1_dragonKills', 'team2_baronKills', 'team2_riftKills',
                    'team2_inhibitorKills', 'team2_towerKills', 'team2_dragonKills', 'team1_firstDragon',
                    'team1_firstInhibitor', 'team1_firstRiftHerald', 'team1_firstBaron', 'team1_firstBlood',
                    'team1_firstTower', 'team2_firstDragon', 'team2_firstInhibitor', 'team2_firstRiftHerald',
                    'team2_firstBaron', 'team2_firstBlood', 'team2_firstTower']]
df_objectives.to_csv('game_objectives.csv')
