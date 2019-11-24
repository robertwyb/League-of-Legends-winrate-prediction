import requests
import numpy as np
import pandas as pd
import time
import pickle
import glob


def get_leagueId(df, tier):
    """
    return leagueId based on given tier
    :param df: dataframe with tier and leagueId
    :param tier: str, tier in rank game (Iron, Bronze, Silver, ...)
    :return: dataframe with leagueId
    """
    return df[df['tier'] == tier]


def get_sum_from_league(division, tier, pagenum, api_key):
    """
    return pandas datafram contain summoner info
    :param division: str
    :param tier: str
    :param pagenum: int
    :param api_key: str
    :return: dataframe
    """
    summoners = {'summonerId': [], 'summonerName': []}
    for p in range(1, pagenum):
        url = f'https://na1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{division}/{tier}' \
              f'?page={p}&api_key={api_key}'
        response = requests.get(url)
        time.sleep(1)
        data = response.json()
        for i in data:
            summoners['summonerId'].append(i['summonerId'])
            summoners['summonerName'].append(i['summonerName'])
    return pd.DataFrame(summoners)


def get_all_sum_info(summonerName, api_key):
    """
    get detail summoner info based on given summoner name
    :param summonerName: str
    :param api_key: str
    :return: pandas df contain summonerId, summonerName, accountId, puuid
    """
    summoners = {'summonerId': [], 'summonerName': [], 'accountId': [], 'puuid': []}
    url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    try:
        summoners['summonerId'].append(data['id'])
        summoners['summonerName'].append(data['name'])
        summoners['accountId'].append(data['accountId'])
        summoners['puuid'].append(data['puuid'])
        return pd.DataFrame(summoners)
    except:
        return pd.DataFrame()


def multi_sum_info(df, num, api_key):
    """
    function that use get_all_sum_info to store summoner info to csv file
    :param df: dataframe includes summonerName
    :param num: int, index of file
    :param api_key: str
    :return: None
    """
    summoner_df = pd.DataFrame()
    for sum_name in df['summonerName']:
        sum_info = get_all_sum_info(sum_name, api_key)
        summoner_df = pd.concat([summoner_df, sum_info], ignore_index=True)
        time.sleep(1)
    summoner_df.to_csv(f'summoner{num}.csv')


def get_match_list(accountId, api_key):
    """
    return dataframe contain gameId based on accountId
    :param accountId: str
    :param api_key: str
    :return: dataframe
    """
    match_list = {'matchid': []}
    url = f'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{accountId}?queue=420&api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    try:
        for m in data['matches'][:20]:
            match_list['matchid'].append(m['gameId'])
        return pd.DataFrame(match_list)
    except:
        return pd.DataFrame()


def multi_match_id(df, num, api_key):
    """
        function that use get_match_list to store matchId to csv file
        :param df: dataframe includes accountId
        :param num: int, index of file
        :param api_key: str
        :return: None
    """
    match_df = pd.DataFrame()
    idx = 0
    for aid in df['accountId']:
        matchId = get_match_list(aid, api_key)
        match_df = pd.concat([match_df, matchId], ignore_index=True)
        time.sleep(1)
        idx += 1
        if idx % 10 == 0:
            print(idx)

    match_df.to_csv(f'./matchid/matchid{num}.csv')


def get_team_detail(data):
    result = {}
    for i in range(len(data['teams'])):
        team = data['teams'][i]
        result[f'team{i+1}_win'] = convert_str_int(team['Win'])
        result[f'team{i+1}_firstDragon'] = convert_str_int(team['firstDragon'])
        result[f'team{i+1}_firstInhibitor'] = convert_str_int(team['firstInhibitor'])
        result[f'team{i+1}_firstRiftHerald'] = convert_str_int(team['firstRiftHerald'])
        result[f'team{i+1}_firstBaron'] = convert_str_int(team['firstBaron'])
        result[f'team{i+1}_firstBlood'] = convert_str_int(team['firstBlood'])
        result[f'team{i+1}_firstTower'] = convert_str_int(team['firstTower'])
        result[f'team{i+1}_baronKills'] = team['baronKills']
        result[f'team{i+1}_riftKills'] = team['riftKills']
        result[f'team{i+1}_inhibitorKills'] = team['inhibitorKills']
        result[f'team{i+1}_towerKills'] = team['towerKills']
        result[f'team{i+1}_dragonKills'] = team['dragonKills']


def get_match_detail(matchId, api_key):
    match_detail = {}
    url = f'https://na1.api.riotgames.com/lol/match/v4/matches/{matchId}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    try:
        match_detail['gameId'] = data['gameId']
        # stats for team


        # player info for team 1
        players = data['participants']
        p1, p2, p3, p4, p5 = players[0], players[1], players[2], players[3], players[4]
        match_detail['team1_p1_id'] = p1['participantId']
        match_detail['team1_p1_Clease'] = 1 if p1['spell1Id'] == 1 or p1['spell2Id'] == 1 else 0
        match_detail['team1_p1_Exhuast'] = 1 if p1['spell1Id'] == 3 or p1['spell2Id'] == 3 else 0
        match_detail['team1_p1_Flash'] = 1 if p1['spell1Id'] == 4 or p1['spell2Id'] == 4 else 0
        match_detail['team1_p1_Ghost'] = 1 if p1['spell1Id'] == 6 or p1['spell2Id'] == 6 else 0
        match_detail['team1_p1_Heal'] = 1 if p1['spell1Id'] == 7 or p1['spell2Id'] == 7 else 0
        match_detail['team1_p1_Smite'] = 1 if p1['spell1Id'] == 11 or p1['spell2Id'] == 11 else 0
        match_detail['team1_p1_Teleport'] = 1 if p1['spell1Id'] == 12 or p1['spell2Id'] == 12 else 0
        match_detail['team1_p1_Ignite'] = 1 if p1['spell1Id'] == 14 or p1['spell2Id'] == 14 else 0
        match_detail['team1_p1_Barrier'] = 1 if p1['spell1Id'] == 21 or p1['spell2Id'] == 21 else 0

        match_detail['team1_p1_lane'] = p1[]
        match_detail['team1_p1_cs_diff_permin0'] = p1[]
        match_detail['team1_p1_cs_diff_permin1'] = p1[]
        match_detail['team1_p1_cs_diff_permin2'] = p1[]
        match_detail['team1_p1_cs_diff_permin3'] = p1[]
        match_detail['team1_p1_xp_diff_permin0'] = p1[]
        match_detail['team1_p1_xp_diff_permin1'] = p1[]
        match_detail['team1_p1_xp_diff_permin2'] = p1[]
        match_detail['team1_p1_xp_diff_permin3'] = p1[]
        match_detail['team1_p1_dmg_taken_diff_permin0'] = p1[]
        match_detail['team1_p1_dmg_taken_diff_permin1'] = p1[]
        match_detail['team1_p1_dmg_taken_diff_permin2'] = p1[]
        match_detail['team1_p1_dmg_taken_diff_permin3'] = p1[]
        match_detail['team1_p1_gold_permin0'] = p1[]
        match_detail['team1_p1_gold_permin1'] = p1[]
        match_detail['team1_p1_gold_permin2'] = p1[]
        match_detail['team1_p1_gold_permin3'] = p1[]
        match_detail['team1_p1_cs_permin0'] = p1[]
        match_detail['team1_p1_cs_permin1'] = p1[]
        match_detail['team1_p1_cs_permin2'] = p1[]
        match_detail['team1_p1_cs_permin3'] = p1[]
        match_detail['team1_p1_dmg_taken_permin0'] = p1[]
        match_detail['team1_p1_dmg_taken_permin1'] = p1[]
        match_detail['team1_p1_dmg_taken_permin2'] = p1[]
        match_detail['team1_p1_dmg_taken_permin3'] = p1[]


    except:
        return pd.DataFrame()


def multi_match_detail(df, num, api_key):
    match_save = []
    for i in df['matchid']:
        dct = get_match_detail(i, api_key)
        match_save.append(dct)
    save_obj(match_save, f'match_detail{num}')


def extract_match_detail(file):
    match_detail = {}
    data = load_obj(file)



# helper function
def concat_file(path, name):
    output_df = pd.DataFrame()
    for filename in glob.glob(f'{path}*.csv'):
        temp_df = pd.read_csv(filename)
        output_df = pd.concat([output_df, temp_df], ignore_index=True)
    output_df = output_df.drop(columns=['Unnamed: 0'])
    output_df.to_csv(name)


def convert_str_int(s):
    if s == 'true' or s == '"Win"':
        return 1
    return 0


def save_obj(obj, name):
    with open('data/'+ name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    api_key0 = 'RGAPI-7b61855c-d932-4544-89c1-f131631908f7'
    api_key1 = 'RGAPI-ed57fba6-e823-4bd4-bc40-0904d7d4c9e5'
    api_key2 = 'RGAPI-d8e6b52d-a441-4d6d-aee3-1ec56c320e0a'
    api_key3 = 'RGAPI-03c17d5a-73b1-496b-bc19-be79d3ed7772'
    api_key4 = 'RGAPI-e3636151-d64e-4354-9310-76d68a903314'
    api_key5 = 'RGAPI-651fea6d-86a6-49e5-8666-88df3a2bcecc'
    api_key6 = 'RGAPI-6bd47992-85fb-4224-9979-e70af2fba376'
    api_key7 = 'RGAPI-721fccd9-1772-48a5-a0ad-b290da5c2514'
    api_key8 = 'RGAPI-593563a2-9aaf-432a-adcb-b1103e2ccde1'
    api_key9 = 'RGAPI-b7047fa3-4565-4dcb-b7c5-0c0b9e03beb9'
    api_key10 = 'RGAPI-3710e912-bfc7-4a44-844e-2da7f6b4c89f'
    api_key11 = 'RGAPI-60008437-00cc-440f-8c36-6150a97b2b72'
    api_key12 = 'RGAPI-f6b96a83-211e-44f0-9b10-d6258b1ac288'
    api_key13 = 'RGAPI-d65ecd4b-43f3-484e-bd2d-4c72e09414f6'
    api_key14 = 'RGAPI-a0137b97-6cc0-46dd-85e1-efae408aa1e9'

    df1 = get_all_sum_info('loserobert', api_key0)
    df2 = get_all_sum_info('PrinzFrank', api_key0)
    df3 = get_all_sum_info('winnerichard', api_key0)
    df4 = get_all_sum_info('Mr sinan', api_key0)
    df5 = get_all_sum_info('Ronnyzrz', api_key0)
    df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

    # get summoners info in that division
    # plat = (['I', 'II', 'III', 'IV'], [163, 166, 251, 750])
    # diam = (['I', 'II', 'III', 'IV'], [15, 20, 50, 100])
    # league_sum_df = get_sum_from_league('DIAMOND', 'IV', 100, api_key8)
    # league_sum_df.to_csv('diam4sum.csv')

    # concat_file('C:/Users/rober/OneDrive/csc/lol-ml/sum/', 'full_sumid.csv')


    # --------------------- get detail summoner info
    league_sum_df = pd.read_csv('full_sumid.csv')
    sum0 = league_sum_df.loc[:26000]
    sum1 = league_sum_df.loc[26000:52000]
    sum2 = league_sum_df.loc[52000:78000]
    sum3 = league_sum_df.loc[78000:104000]
    sum4 = league_sum_df.loc[104000:130000]
    sum5 = league_sum_df.loc[130000:156000]
    sum6 = league_sum_df.loc[156000:182000]
    sum7 = league_sum_df.loc[182000:208000]
    sum8 = league_sum_df.loc[208000:234000]
    sum9 = league_sum_df.loc[234000:250000]
    sum10 = league_sum_df.loc[250000:270000]
    sum11 = league_sum_df.loc[270000:280000]
    sum12 = league_sum_df.loc[280000:295000]
    sum13 = league_sum_df.loc[295000:]

    # multi_sum_info(sum0, 0, api_key0)
    # multi_sum_info(sum1, 1, api_key1)
    # multi_sum_info(sum2, 2, api_key2)
    # multi_sum_info(sum3, 3, api_key3)
    # multi_sum_info(sum4, 4, api_key4)
    # multi_sum_info(sum5, 5, api_key5)
    # multi_sum_info(sum6, 6, api_key6)
    # multi_sum_info(sum7, 7, api_key7)
    # multi_sum_info(sum8, 8, api_key8)
    # multi_sum_info(sum9, 9, api_key9)
    # multi_sum_info(sum10, 10, api_key10)
    # multi_sum_info(sum11, 11, api_key11)
    # multi_sum_info(sum12, 12, api_key12)
    # multi_sum_info(sum13, 13, api_key13)

    # -----------------------------------
    # concat_file('C:/Users/rober/OneDrive/csc/lol-ml/fullsum/', 'full_suminfo.csv')



    # multi_match_id(sum0, 0, api_key0)
    # multi_match_id(sum1, 1, api_key1)
    # multi_match_id(sum2, 2, api_key2)
    # multi_match_id(sum3, 3, api_key3)
    # multi_match_id(sum4, 4, api_key4)
    # multi_match_id(sum5, 5, api_key5)
    # multi_match_id(sum6, 6, api_key6)
    # multi_match_id(sum7, 7, api_key7)

    #------------------------------------
    # match01 = pd.read_csv('full_match.csv').loc[:14700]
    #
    # multi_match_detail(match01, 0, api_key0)
    # test = load_obj('match_detail0')








