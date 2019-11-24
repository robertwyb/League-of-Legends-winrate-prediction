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
    """
    return dictionary contain team info extract from api returned
    :param data: api return
    :return: dictionary
    """
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
    return result


def get_match_detail(matchId, api_key):
    match_detail = {}
    url = f'https://na1.api.riotgames.com/lol/match/v4/matches/{matchId}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    try:
        match_detail['gameId'] = data['gameId']
        # stats for team
        team_info = get_team_detail(data)
        for col in team_info.items():
            match_detail[col[0]] = col[1]

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
    print()






