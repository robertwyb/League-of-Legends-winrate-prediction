import requests
import numpy as np
import pandas as pd
import time
import pickle
import glob
import cv2
import sys
import keyboard
import matplotlib.pyplot as plt
from PIL import ImageGrab


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
        for m in data['matches'][:5]:
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
        time.sleep(1)
        match_df = pd.concat([match_df, matchId], ignore_index=True)
        time.sleep(1)
        idx += 1
        if idx % 10 == 0:
            print(idx)

    match_df.to_csv(f'./matchid/matchid{num}.csv')


def get_team_detail(data):
    """
    return dictionary contain team info extract from api returned result
    :param data: api return
    :return: dictionary
    """
    result = {}
    for i in range(len(data['teams'])):
        team = data['teams'][i]
        result[f'team{i + 1}_win'] = convert_str_int(team['win'])
        try:
            result[f'team{i + 1}_firstDragon'] = convert_str_int(team['firstDragon'])
        except:
            result[f'team{i + 1}_firstDragon'] = np.nan
        try:
            result[f'team{i + 1}_firstInhibitor'] = convert_str_int(team['firstInhibitor'])
        except:
            result[f'team{i + 1}_firstInhibitor'] = np.nan
        try:
            result[f'team{i + 1}_firstRiftHerald'] = convert_str_int(team['firstRiftHerald'])
        except:
            result[f'team{i + 1}_firstRiftHerald'] = np.nan
        try:
            result[f'team{i + 1}_firstBaron'] = convert_str_int(team['firstBaron'])
        except:
            result[f'team{i + 1}_firstBaron'] = np.nan
        try:
            result[f'team{i + 1}_firstBlood'] = convert_str_int(team['firstBlood'])
        except:
            result[f'team{i + 1}_firstBlood'] = np.nan
        try:
            result[f'team{i + 1}_firstTower'] = convert_str_int(team['firstTower'])
        except:
            result[f'team{i + 1}_firstTower'] = np.nan
        try:
            result[f'team{i + 1}_baronKills'] = team['baronKills']
        except:
            result[f'team{i + 1}_baronKills'] = np.nan
        try:
            result[f'team{i + 1}_riftKills'] = team['riftHeraldKills']
        except:
            result[f'team{i + 1}_riftKills'] = np.nan
        try:
            result[f'team{i + 1}_inhibitorKills'] = team['inhibitorKills']
        except:
            result[f'team{i + 1}_inhibitorKills'] = np.nan
        try:
            result[f'team{i + 1}_towerKills'] = team['towerKills']
        except:
            result[f'team{i + 1}_towerKills'] = np.nan
        try:
            result[f'team{i + 1}_dragonKills'] = team['dragonKills']
        except:
            result[f'team{i + 1}_dragonKills'] = np.nan
    return result


def get_player_detail(players):
    """
    return dictionary contain player info extract from api returned result
    :param players: list of players
    :return: dictionary
    """
    result = {}
    for i in range(len(players)):
        if i <= 4:
            team = 1
            p = i + 1
        else:
            team = 2
            p = i - 4
        player = players[i]
        # summoner player id
        result[f'team{team}_p{p}_id'] = player['participantId']

        # summoner champion id
        result[f'team{team}_p{p}_championId'] = player['championId']

        # summoner speels
        result[f'team{team}_p{p}_Clease'] = 1 if player['spell1Id'] == 1 or player['spell2Id'] == 1 else 0
        result[f'team{team}_p{p}_Exhuast'] = 1 if player['spell1Id'] == 3 or player['spell2Id'] == 3 else 0
        result[f'team{team}_p{p}_Flash'] = 1 if player['spell1Id'] == 4 or player['spell2Id'] == 4 else 0
        result[f'team{team}_p{p}_Ghost'] = 1 if player['spell1Id'] == 6 or player['spell2Id'] == 6 else 0
        result[f'team{team}_p{p}_Heal'] = 1 if player['spell1Id'] == 7 or player['spell2Id'] == 7 else 0
        result[f'team{team}_p{p}_Smite'] = 1 if player['spell1Id'] == 11 or player['spell2Id'] == 11 else 0
        result[f'team{team}_p{p}_Teleport'] = 1 if player['spell1Id'] == 12 or player['spell2Id'] == 12 else 0
        result[f'team{team}_p{p}_Ignite'] = 1 if player['spell1Id'] == 14 or player['spell2Id'] == 14 else 0
        result[f'team{team}_p{p}_Barrier'] = 1 if player['spell1Id'] == 21 or player['spell2Id'] == 21 else 0

        # summoner diff compare with their laners
        try:
            result[f'team{team}_p{p}_lane'] = player['timeline']['lane']
        except:
            result[f'team{team}_p{p}_lane'] = np.nan
        try:
            result[f'team{team}_p{p}_cs_diff_permin0'] = player['timeline']['csDiffPerMinDeltas']['0-10']
        except:
            result[f'team{team}_p{p}_cs_diff_permin0'] = np.nan
        try:
            result[f'team{team}_p{p}_cs_diff_permin1'] = player['timeline']['csDiffPerMinDeltas']['10-20']
        except:
            result[f'team{team}_p{p}_cs_diff_permin1'] = np.nan
        try:
            result[f'team{team}_p{p}_cs_diff_permin2'] = player['timeline']['csDiffPerMinDeltas']['20-30']
        except:
            result[f'team{team}_p{p}_cs_diff_permin2'] = np.nan
        try:
            result[f'team{team}_p{p}_cs_diff_permin3'] = player['timeline']['csDiffPerMinDeltas']['30-end']
        except:
            result[f'team{team}_p{p}_cs_diff_permin3'] = np.nan
        try:
            result[f'team{team}_p{p}_xp_diff_permin0'] = player['timeline']['xpDiffPerMinDeltas']['0-10']
        except:
            result[f'team{team}_p{p}_xp_diff_permin0'] = np.nan
        try:
            result[f'team{team}_p{p}_xp_diff_permin1'] = player['timeline']['xpDiffPerMinDeltas']['10-20']
        except:
            result[f'team{team}_p{p}_xp_diff_permin1'] = np.nan
        try:
            result[f'team{team}_p{p}_xp_diff_permin2'] = player['timeline']['xpDiffPerMinDeltas']['20-30']
        except:
            result[f'team{team}_p{p}_xp_diff_permin2'] = np.nan
        try:
            result[f'team{team}_p{p}_xp_diff_permin3'] = player['timeline']['xpDiffPerMinDeltas']['30-end']
        except:
            result[f'team{team}_p{p}_xp_diff_permin3'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_diff_permin0'] = player['timeline']['damageTakenDiffPerMinDeltas'][
                '0-10']
        except:
            result[f'team{team}_p{p}_dmg_taken_diff_permin0'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_diff_permin1'] = player['timeline']['damageTakenDiffPerMinDeltas'][
                '10-20']
        except:
            result[f'team{team}_p{p}_dmg_taken_diff_permin1'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_diff_permin2'] = player['timeline']['damageTakenDiffPerMinDeltas'][
                '20-30']
        except:
            result[f'team{team}_p{p}_dmg_taken_diff_permin2'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_diff_permin3'] = player['timeline']['damageTakenDiffPerMinDeltas'][
                '30-end']
        except:
            result[f'team{team}_p{p}_dmg_taken_diff_permin3'] = np.nan
        try:
            result[f'team{team}_p{p}_gold_permin0'] = player['timeline']['goldPerMinDeltas']['0-10']
        except:
            result[f'team{team}_p{p}_gold_permin0'] = np.nan
        try:
            result[f'team{team}_p{p}_gold_permin1'] = player['timeline']['goldPerMinDeltas']['10-20']
        except:
            result[f'team{team}_p{p}_gold_permin1'] = np.nan
        try:
            result[f'team{team}_p{p}_gold_permin2'] = player['timeline']['goldPerMinDeltas']['20-30']
        except:
            result[f'team{team}_p{p}_gold_permin2'] = np.nan
        try:
            result[f'team{team}_p{p}_gold_permin3'] = player['timeline']['goldPerMinDeltas']['30-end']
        except:
            result[f'team{team}_p{p}_gold_permin3'] = np.nan
        try:
            result[f'team{team}_p{p}_cs_permin0'] = player['timeline']['creepsPerMinDeltas']['0-10']
        except:
            result[f'team{team}_p{p}_cs_permin0'] = np.nan
        try:
            result[f'team{team}_p{p}_cs_permin1'] = player['timeline']['creepsPerMinDeltas']['10-20']
        except:
            result[f'team{team}_p{p}_cs_permin1'] = np.nan
        try:
            result[f'team{team}_p{p}_cs_permin2'] = player['timeline']['creepsPerMinDeltas']['20-30']
        except:
            result[f'team{team}_p{p}_cs_permin2'] = np.nan
        try:
            result[f'team{team}_p{p}_cs_permin3'] = player['timeline']['creepsPerMinDeltas']['30-end']
        except:
            result[f'team{team}_p{p}_cs_permin3'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_permin0'] = player['timeline']['damageTakenPerMinDeltas']['0-10']
        except:
            result[f'team{team}_p{p}_dmg_taken_permin0'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_permin1'] = player['timeline']['damageTakenPerMinDeltas']['10-20']
        except:
            result[f'team{team}_p{p}_dmg_taken_permin1'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_permin2'] = player['timeline']['damageTakenPerMinDeltas']['20-30']
        except:
            result[f'team{team}_p{p}_dmg_taken_permin2'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_permin3'] = player['timeline']['damageTakenPerMinDeltas']['30-end']
        except:
            result[f'team{team}_p{p}_dmg_taken_permin3'] = np.nan
        try:
            result[f'team{team}_p{p}_xp_permin0'] = player['timeline']['xpPerMinDeltas']['0-10']
        except:
            result[f'team{team}_p{p}_xp_permin0'] = np.nan
        try:
            result[f'team{team}_p{p}_xp_permin1'] = player['timeline']['xpPerMinDeltas']['10-20']
        except:
            result[f'team{team}_p{p}_xp_permin1'] = np.nan
        try:
            result[f'team{team}_p{p}_xp_permin2'] = player['timeline']['xpPerMinDeltas']['20-30']
        except:
            result[f'team{team}_p{p}_xp_permin2'] = np.nan
        try:
            result[f'team{team}_p{p}_xp_permin3'] = player['timeline']['xpPerMinDeltas']['30-end']
        except:
            result[f'team{team}_p{p}_xp_permin3'] = np.nan

        # summoner detail match info
        result[f'team{team}_p{p}_teamJungle'] = player['stats']['neutralMinionsKilledTeamJungle']
        result[f'team{team}_p{p}_visionScore'] = player['stats']['visionScore']
        result[f'team{team}_p{p}_apdmg_champion'] = player['stats']['magicDamageDealtToChampions']
        result[f'team{team}_p{p}_longestTimeLiving'] = player['stats']['longestTimeSpentLiving']
        result[f'team{team}p1{p}_tripleKills'] = player['stats']['tripleKills']
        result[f'team{team}_p{p}_kills'] = player['stats']['kills']
        result[f'team{team}_p{p}_jungle'] = player['stats']['neutralMinionsKilled']
        result[f'team{team}_p{p}_dmg_to_turrets'] = player['stats']['damageDealtToTurrets']
        result[f'team{team}_p{p}_addmg_champion'] = player['stats']['physicalDamageDealtToChampions']
        result[f'team{team}_p{p}_dmg_to_objectives'] = player['stats']['damageDealtToObjectives']
        result[f'team{team}_p{p}_total_dmg_taken'] = player['stats']['totalDamageTaken']
        result[f'team{team}_p{p}_wardsKilled'] = player['stats']['wardsKilled']
        result[f'team{team}_p{p}_killingSpree'] = player['stats']['largestKillingSpree']
        result[f'team{team}_p{p}_quadraKills'] = player['stats']['quadraKills']
        result[f'team{team}_p{p}_apdmg'] = player['stats']['magicDamageDealt']
        try:
            result[f'team{team}_p{p}_firstBloodKill'] = convert_str_int(player['stats']['firstBloodKill'])
            result[f'team{team}_p{p}_fbAssist'] = convert_str_int(player['stats']['firstBloodAssist'])
        except:
            result[f'team{team}_p{p}_firstBloodKill'] = np.nan
            result[f'team{team}_p{p}_fbAssist'] = np.nan
        result[f'team{team}_p{p}_dmgSelfMitigated'] = player['stats']['damageSelfMitigated']
        result[f'team{team}_p{p}_apdmg_taken'] = player['stats']['magicalDamageTaken']
        result[f'team{team}_p{p}_assists'] = player['stats']['assists']
        result[f'team{team}_p{p}_goldSpent'] = player['stats']['goldSpent']
        result[f'team{team}_p{p}_truedmg'] = player['stats']['trueDamageDealt']
        result[f'team{team}_p{p}_addmg'] = player['stats']['physicalDamageDealt']
        result[f'team{team}_p{p}_total_dmg_champion'] = player['stats']['totalDamageDealtToChampions']
        result[f'team{team}_p{p}_addmg_taken'] = player['stats']['physicalDamageTaken']
        result[f'team{team}_p{p}_deaths'] = player['stats']['deaths']
        result[f'team{team}_p{p}_wardsPlaced'] = player['stats']['wardsPlaced']
        result[f'team{team}_p{p}_turretKills'] = player['stats']['turretKills']
        result[f'team{team}_p{p}_totalDamageDealt'] = player['stats']['totalDamageDealt']
        result[f'team{team}_p{p}_trueDamage_champion'] = player['stats']['trueDamageDealtToChampions']
        result[f'team{team}_p{p}_goldEarned'] = player['stats']['goldEarned']
        try:
            result[f'team{team}_p{p}_firstTowerAssists'] = convert_str_int(player['stats']['firstTowerAssist'])
            result[f'team{team}_p{p}_firstTowerKill'] = convert_str_int(player['stats']['firstTowerKill'])
        except:
            result[f'team{team}_p{p}_firstTowerAssists'] = np.nan
            result[f'team{team}_p{p}_firstTowerKill'] = np.nan
        result[f'team{team}_p{p}_champLevel'] = player['stats']['champLevel']
        result[f'team{team}_p{p}_pink'] = player['stats']['visionWardsBoughtInGame']
        result[f'team{team}_p{p}_pentakills'] = player['stats']['pentaKills']
        result[f'team{team}_p{p}_totalHeal'] = player['stats']['totalHeal']
        result[f'team{team}_p{p}_totalMinionsKilled'] = player['stats']['totalMinionsKilled']
        result[f'team{team}_p{p}_timeCC'] = player['stats']['timeCCingOthers']
    return result


def get_match_detail(matchId, api_key):
    """
    return dataframe includes all match detail we want
    :param matchId: str
    :param api_key: str
    :return: dataframe
    """
    match_detail = {}
    url = f'https://na1.api.riotgames.com/lol/match/v4/matches/{matchId}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    if 'gameId' in data and data['gameDuration'] > 240 and data['seasonId'] == 13 and data['queueId'] == 420:
        match_detail['gameId'] = data['gameId']
        # stats for team
        team_info = get_team_detail(data)
        for col in team_info.items():
            match_detail[col[0]] = col[1]
        # player info
        players = data['participants']
        player_info = get_player_detail(players)
        for col in player_info.items():
            match_detail[col[0]] = col[1]
        return pd.DataFrame(match_detail, index=[0])
    return pd.DataFrame()


def multi_match_detail(df, num, api_key):
    """
    use get_match_detail function to save match data to csv file
    :param df: dataframe contain matchid
    :param num: int, index of file
    :param api_key: str
    :return: None
    """
    result = pd.DataFrame()
    cnt = 0
    for i in df['matchid']:
        cnt += 1
        dft = get_match_detail(i, api_key)
        time.sleep(1)
        result = pd.concat([result, dft], ignore_index=True)
        if cnt % 10 == 0:
            print(cnt)
    result.to_csv(f'match_detail{num}.csv')


def get_match_timeline(matchId, api_key):
    """
    return dataframe contain ingame timeline data
    :param matchId: str
    :param api_key: str
    :return: dataframe
    """
    match_timeline = {}
    url = f'https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/{matchId}?api_key={api_key}'
    response = requests.get(url)
    try:
        data = response.json()['frames']
        match_timeline['gameId'] = [matchId]
        match_timeline['game_time'] = [data[-1]['timestamp'] / 1000]
        for i in [5, 10, 15, 20, 25, 30]:
            try:
                for k, pframe in data[i]['participantFrames'].items():
                    pid = pframe['participantId']
                    if pid <= 5:
                        match_timeline[f'team1_p{pid}_gold_{i}min'] = [pframe['totalGold']]
                        match_timeline[f'team1_p{pid}_level_{i}min'] = [pframe['level']]
                        match_timeline[f'team1_p{pid}_cs_{i}min'] = [pframe['minionsKilled']]
                        match_timeline[f'team1_p{pid}_xp_{i}min'] = [pframe['xp']]
                        match_timeline[f'team1_p{pid}_jg_{i}min'] = [pframe['jungleMinionsKilled']]
                    else:
                        match_timeline[f'team2_p{pid-5}_gold_{i}min'] = [pframe['totalGold']]
                        match_timeline[f'team2_p{pid-5}_level_{i}min'] = [pframe['level']]
                        match_timeline[f'team2_p{pid-5}_cs_{i}min'] = [pframe['minionsKilled']]
                        match_timeline[f'team2_p{pid-5}_xp_{i}min'] = [pframe['xp']]
                        match_timeline[f'team2_p{pid-5}_jg_{i}min'] = [pframe['jungleMinionsKilled']]

            except:
                match_timeline[f'team1_p1_gold_{i}min'] = np.nan
                match_timeline[f'team1_p2_level_{i}min'] = np.nan
                match_timeline[f'team1_p3_cs_{i}min'] = np.nan
                match_timeline[f'team1_p4_xp_{i}min'] = np.nan
                match_timeline[f'team1_p5_jg_{i}min'] = np.nan
                match_timeline[f'team2_p1_gold_{i}min'] = np.nan
                match_timeline[f'team2_p2_level_{i}min'] = np.nan
                match_timeline[f'team2_p3_cs_{i}min'] = np.nan
                match_timeline[f'team2_p4_xp_{i}min'] = np.nan
                match_timeline[f'team2_p5_jg_{i}min'] = np.nan
    except:
        return pd.DataFrame(match_timeline)
    return pd.DataFrame(match_timeline)


def multi_get_timeline(df, num, apikey):
    """
    us get_match_timeline and save data to csv
    :param df:
    :param num:
    :param apikey:
    :return:
    """
    result = pd.DataFrame()
    cnt = 0
    for i in df['gameId']:
        cnt += 1
        dft = get_match_timeline(i, apikey)
        time.sleep(1)
        result = pd.concat([result, dft], ignore_index=True)
        if cnt % 10 == 0:
            print(cnt)
    result.to_csv(f'match_timeline{num}.csv')


# real-time recognize part
def begin_prediction(t1_champ, t2_champ):
    """
    Capture screen to extract ingame real time data and use data to predict winrate
    :return:
    """
    # read all icon to be recognized in game
    blue_baron = cv2.resize(cv2.imread('./icon/blue baron.png'), None, fx=0.625, fy=0.625)
    blue_rift = cv2.resize(cv2.imread('./icon/blue rift.png'), None, fx=0.625, fy=0.625)
    blue_elder_dragon = cv2.resize(cv2.imread('./icon/blue elder dragon.png'), None, fx=0.625, fy=0.625)
    blue_infernal_dragon = cv2.resize(cv2.imread('./icon/blue infernal dragon.png'), None, fx=0.625, fy=0.625)
    blue_mountain_dragon = cv2.resize(cv2.imread('./icon/blue mountain dragon.png'), None, fx=0.625, fy=0.625)
    blue_ocean_dragon = cv2.resize(cv2.imread('./icon/blue ocean dragon.png'), None, fx=0.625, fy=0.625)
    blue_cloud_dragon = cv2.resize(cv2.imread('./icon/blue wind dragon.png'), None, fx=0.625, fy=0.625)
    blue_kill_inhib = cv2.resize(cv2.imread('./icon/blue kill inhib.png'), None, fx=0.625, fy=0.625)
    blue_kill_tower = cv2.resize(cv2.imread('./icon/blue kill tower.png'), None, fx=0.625, fy=0.625)
    red_baron = cv2.resize(cv2.imread('./icon/red baron.png'), None, fx=0.625, fy=0.625)
    red_rift = cv2.resize(cv2.imread('./icon/red rift.png'), None, fx=0.625, fy=0.625)
    red_elder_dragon = cv2.resize(cv2.imread('./icon/red elder dragon.png'), None, fx=0.625, fy=0.625)
    red_infernal_dragon = cv2.resize(cv2.imread('./icon/red infernal dragon.png'), None, fx=0.625, fy=0.625)
    red_mountain_dragon = cv2.resize(cv2.imread('./icon/red mountain dragon.png'), None, fx=0.625, fy=0.625)
    red_ocean_dragon = cv2.resize(cv2.imread('./icon/red ocean dragon.png'), None, fx=0.625, fy=0.625)
    red_cloud_dragon = cv2.resize(cv2.imread('./icon/red wind dragon.png'), None, fx=0.625, fy=0.625)
    red_kill_inhib = cv2.resize(cv2.imread('./icon/red kill inhib.png'), None, fx=1, fy=1)
    red_kill_tower = cv2.resize(cv2.imread('./icon/red kill tower.png'), None, fx=1, fy=1)

    # initial data
    team1_dragons, team1_towers, team1_inhibs, team1_barons, team1_rifts = 0, 0, 0, 0, 0
    team2_dragons, team2_towers, team2_inhibs, team2_barons, team2_rifts = 0, 0, 0, 0, 0

    team1_p1_cs, team1_p2_cs, team1_p3_cs, team1_p4_cs, team1_p5_cs = 0, 0, 0, 0, 0
    team2_p1_cs, team2_p2_cs, team2_p3_cs, team2_p4_cs, team2_p5_cs = 0, 0, 0, 0, 0

    team1_p1_kills, team1_p2_kills, team1_p3_kills, team1_p4_kills, team1_p5_kills = 0, 0, 0, 0, 0
    team2_p1_kills, team2_p2_kills, team2_p3_kills, team2_p4_kills, team2_p5_kills = 0, 0, 0, 0, 0

    team1_p1_deaths, team1_p2_deaths, team1_p3_deaths, team1_p4_deaths, team1_p5_deaths = 0, 0, 0, 0, 0
    team2_p1_deaths, team2_p2_deaths, team2_p3_deaths, team2_p4_deaths, team2_p5_deaths = 0, 0, 0, 0, 0

    team1_p1_assists, team1_p2_assists, team1_p3_assists, team1_p4_assists, team1_p5_assists = 0, 0, 0, 0, 0
    team2_p1_assists, team2_p2_assists, team2_p3_assists, team2_p4_assists, team2_p5_assists = 0, 0, 0, 0, 0

    team1_baronKills = 0
    team1_riftKills = 0
    team1_inhibitorKills = 0
    team1_towerKills = 0
    team1_dragonKills = 0
    team2_baronKills = 0
    team2_riftKills = 0
    team2_inhibitorKills = 0
    team2_towerKills = 0
    team2_dragonKills = 0
    team1_firstDragon = 0
    team1_firstInhibitor = 0
    team1_firstRiftHerald = 0
    team1_firstBaron = 0
    team1_firstBlood = 0
    team1_firstTower = 0
    team2_firstDragon = 0
    team2_firstInhibitor = 0
    team2_firstRiftHerald = 0
    team2_firstBaron = 0
    team2_firstBlood = 0
    team2_firstTower = 0

    team1_p1_cs_10min = np.nan
    team1_p1_cs_15min = np.nan
    team1_p1_cs_20min = np.nan
    team1_p1_cs_25min = np.nan
    team1_p1_cs_30min = np.nan
    team1_p1_cs_5min = np.nan
    team1_p1_gold_10min = np.nan
    team1_p1_gold_15min = np.nan
    team1_p1_gold_20min = np.nan
    team1_p1_gold_25min = np.nan
    team1_p1_gold_30min = np.nan
    team1_p1_gold_5min = np.nan
    team1_p2_cs_10min = np.nan
    team1_p2_cs_15min = np.nan
    team1_p2_cs_20min = np.nan
    team1_p2_cs_25min = np.nan
    team1_p2_cs_30min = np.nan
    team1_p2_cs_5min = np.nan
    team1_p2_gold_10min = np.nan
    team1_p2_gold_15min = np.nan
    team1_p2_gold_20min = np.nan
    team1_p2_gold_25min = np.nan
    team1_p2_gold_30min = np.nan
    team1_p2_gold_5min = np.nan
    team1_p3_cs_10min = np.nan
    team1_p3_cs_15min = np.nan
    team1_p3_cs_20min = np.nan
    team1_p3_cs_25min = np.nan
    team1_p3_cs_30min = np.nan
    team1_p3_cs_5min = np.nan
    team1_p3_gold_10min = np.nan
    team1_p3_gold_15min = np.nan
    team1_p3_gold_20min = np.nan
    team1_p3_gold_25min = np.nan
    team1_p3_gold_30min = np.nan
    team1_p3_gold_5min = np.nan
    team1_p4_cs_10min = np.nan
    team1_p4_cs_15min = np.nan
    team1_p4_cs_20min = np.nan
    team1_p4_cs_25min = np.nan
    team1_p4_cs_30min = np.nan
    team1_p4_cs_5min = np.nan
    team1_p4_gold_10min = np.nan
    team1_p4_gold_15min = np.nan
    team1_p4_gold_20min = np.nan
    team1_p4_gold_25min = np.nan
    team1_p4_gold_30min = np.nan
    team1_p4_gold_5min = np.nan
    team1_p5_cs_10min = np.nan
    team1_p5_cs_15min = np.nan
    team1_p5_cs_20min = np.nan
    team1_p5_cs_25min = np.nan
    team1_p5_cs_30min = np.nan
    team1_p5_cs_5min = np.nan
    team1_p5_gold_10min = np.nan
    team1_p5_gold_15min = np.nan
    team1_p5_gold_20min = np.nan
    team1_p5_gold_25min = np.nan
    team1_p5_gold_30min = np.nan
    team1_p5_gold_5min = np.nan
    team2_p1_cs_10min = np.nan
    team2_p1_cs_15min = np.nan
    team2_p1_cs_20min = np.nan
    team2_p1_cs_25min = np.nan
    team2_p1_cs_30min = np.nan
    team2_p1_cs_5min = np.nan
    team2_p1_gold_10min = np.nan
    team2_p1_gold_15min = np.nan
    team2_p1_gold_20min = np.nan
    team2_p1_gold_25min = np.nan
    team2_p1_gold_30min = np.nan
    team2_p1_gold_5min = np.nan
    team2_p2_cs_10min = np.nan
    team2_p2_cs_15min = np.nan
    team2_p2_cs_20min = np.nan
    team2_p2_cs_25min = np.nan
    team2_p2_cs_30min = np.nan
    team2_p2_cs_5min = np.nan
    team2_p2_gold_10min = np.nan
    team2_p2_gold_15min = np.nan
    team2_p2_gold_20min = np.nan
    team2_p2_gold_25min = np.nan
    team2_p2_gold_30min = np.nan
    team2_p2_gold_5min = np.nan
    team2_p3_cs_10min = np.nan
    team2_p3_cs_15min = np.nan
    team2_p3_cs_20min = np.nan
    team2_p3_cs_25min = np.nan
    team2_p3_cs_30min = np.nan
    team2_p3_cs_5min = np.nan
    team2_p3_gold_10min = np.nan
    team2_p3_gold_15min = np.nan
    team2_p3_gold_20min = np.nan
    team2_p3_gold_25min = np.nan
    team2_p3_gold_30min = np.nan
    team2_p3_gold_5min = np.nan
    team2_p4_cs_10min = np.nan
    team2_p4_cs_15min = np.nan
    team2_p4_cs_20min = np.nan
    team2_p4_cs_25min = np.nan
    team2_p4_cs_30min = np.nan
    team2_p4_cs_5min = np.nan
    team2_p4_gold_10min = np.nan
    team2_p4_gold_15min = np.nan
    team2_p4_gold_20min = np.nan
    team2_p4_gold_25min = np.nan
    team2_p4_gold_30min = np.nan
    team2_p4_gold_5min = np.nan
    team2_p5_cs_10min = np.nan
    team2_p5_cs_15min = np.nan
    team2_p5_cs_20min = np.nan
    team2_p5_cs_25min = np.nan
    team2_p5_cs_30min = np.nan
    team2_p5_cs_5min = np.nan
    team2_p5_gold_10min = np.nan
    team2_p5_gold_15min = np.nan
    team2_p5_gold_20min = np.nan
    team2_p5_gold_25min = np.nan
    team2_p5_gold_30min = np.nan
    team2_p5_gold_5min = np.nan



    sw1, sw2, sw3, sw4, sw5, sw6, sw7, sw8, sw9, sw10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    sw11, sw12, sw13, sw14, sw15, sw16, sw17, sw18, sw19, sw20 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    team_comp_lst = [0] * 146
    for c in t1_champ:
        index1 = champ_df[champ_df['Champ_Name'] == c]['Champ_Key'].index[0]
        team_comp_lst[index1] += 1
    for c in t2_champ:
        index1 = champ_df[champ_df['Champ_Name'] == c]['Champ_Key'].index[0]
        team_comp_lst[index1] -= 1
    # TODO USE LR TEAM MODEL

    comp_model = pickle.load(open('finalized_model_1_lr.sav', 'rb'))
    t1 = team_comp_lst[:]
    t1 = [i * 600 for i in t1]
    t2 = team_comp_lst[:]
    t2 = [i * 1200 for i in t2]
    t3 = team_comp_lst[:]
    t3 = [i * 1800 for i in t3]
    t4 = team_comp_lst[:]
    t4 = [i * 2400 for i in t4]
    t5 = team_comp_lst[:]
    t5 = [i * 3000 for i in t5]
    team_comp_10 = np.array([t1])
    team_comp_20 = np.array([t2])
    team_comp_30 = np.array([t3])
    team_comp_40 = np.array([t4])
    team_comp_50 = np.array([t5])
    team_comp_10.reshape(1, -1)
    team_comp_20.reshape(1, -1)
    team_comp_30.reshape(1, -1)
    team_comp_40.reshape(1, -1)
    team_comp_50.reshape(1, -1)
    # print(team_comp_10)
    winrate_10 = comp_model.predict_proba(team_comp_10)[0][0]
    winrate_20 = comp_model.predict_proba(team_comp_20)[0][0]
    winrate_30 = comp_model.predict_proba(team_comp_30)[0][0]
    winrate_40 = comp_model.predict_proba(team_comp_40)[0][0]
    winrate_50 = comp_model.predict_proba(team_comp_50)[0][0]
    #
    plt.plot([10, 20, 30, 40, 50], [winrate_10, winrate_20, winrate_30, winrate_40, winrate_50])
    plt.show()

    keyboard.wait('F1')
    print('Game Start')
    start_time = time.time()
    while True:
        while True:
            change = 0
            # 1600x900 windowed mode
            time.sleep(0.5)
            printscreen = np.array(ImageGrab.grab(bbox=(0, 25, 1610, 931)))

            scene = cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
            # cv2.imshow('window', scene)
            event_area = scene[:, 1450:, :]

            team1_p1_cs_area = scene[277 + 2:297 + 2, 465:500, :]
            team1_p2_cs_area = scene[341 + 2:361 + 2, 465:500, :]
            team1_p3_cs_area = scene[405 + 2:425 + 2, 465:500, :]
            team1_p4_cs_area = scene[469 + 2:489 + 2, 465:500, :]
            team1_p5_cs_area = scene[533 + 2:553 + 2, 465:500, :]
            team1_p1_kda_area = scene[277 + 2:297 + 2, 515:575, :]
            team1_p2_kda_area = scene[341 + 2:361 + 2, 515:575, :]
            team1_p3_kda_area = scene[405 + 2:425 + 2, 515:575, :]
            team1_p4_kda_area = scene[469 + 2:489 + 2, 515:575, :]
            team1_p5_kda_area = scene[533 + 2:553 + 2, 515:575, :]

            team2_p1_cs_area = scene[277 + 2:297 + 2, 945:980, :]
            team2_p2_cs_area = scene[341 + 2:361 + 2, 945:980, :]
            team2_p3_cs_area = scene[405 + 2:425 + 2, 945:980, :]
            team2_p4_cs_area = scene[469 + 2:489 + 2, 945:980, :]
            team2_p5_cs_area = scene[533 + 2:553 + 2, 945:980, :]
            team2_p1_kda_area = scene[277 + 2:297 + 2, 990:1060, :]
            team2_p2_kda_area = scene[341 + 2:361 + 2, 990:1060, :]
            team2_p3_kda_area = scene[405 + 2:425 + 2, 990:1060, :]
            team2_p4_kda_area = scene[469 + 2:489 + 2, 990:1060, :]
            team2_p5_kda_area = scene[533 + 2:553 + 2, 990:1060, :]

            team1_p1_level_area = scene[332-31:344-31, 432:448,:]
            team1_p2_level_area = scene[396-31:408-31, 432:448,:]
            team1_p3_level_area = scene[460-31:472-31, 432:448,:]
            team1_p4_level_area = scene[524-31:536-31, 432:448,:]
            team1_p5_level_area = scene[588-31:600-31, 432:448,:]

            team2_p1_level_area = scene[332-31:344-31, 910:925, :]
            team2_p2_level_area = scene[396-31:408-31, 910:925, :]
            team2_p3_level_area = scene[460-31:472-31, 910:925, :]
            team2_p4_level_area = scene[524-31:536-31, 910:925, :]
            team2_p5_level_area = scene[588-31:600-31, 910:925, :]



            # cv2.imshow('window', team1_p1_cs_area)
            # cv2.imshow('window', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
            # cv2.imshow('window', event_area)



            # ------------------------------------------------------- dragons kills data ----------------------------------
            # print('-------------------------------------------------------------------')
            prev_team1_dragons = team1_dragons
            team1_dragons_change, sw1, _ = event_template_match(event_area, blue_infernal_dragon, 0.85, sw1)
            team1_dragons += team1_dragons_change
            team1_dragons_change, sw2, _ = event_template_match(event_area, blue_ocean_dragon, 0.85, sw2)
            team1_dragons += team1_dragons_change
            team1_dragons_change, sw3, _ = event_template_match(event_area, blue_mountain_dragon, 0.85, sw3)
            team1_dragons += team1_dragons_change
            team1_dragons_change, sw4, _ = event_template_match(event_area, blue_cloud_dragon, 0.85, sw4)
            team1_dragons += team1_dragons_change
            team1_dragons_change, sw5, _ = event_template_match(event_area, blue_elder_dragon, 0.85, sw5)
            team1_dragons += team1_dragons_change
            # print(team1_dragons)
            if team1_dragons != 0 and team1_dragons != prev_team1_dragons:
                # print('team1_dragons: ' + str(int(team1_dragons)))
                change += 1

            prev_team2_dragons = team2_dragons
            team2_dragons_change, sw6, _ = event_template_match(event_area, red_infernal_dragon, 0.85, sw6)
            team2_dragons += team2_dragons_change
            team2_dragons_change, sw7, _ = event_template_match(event_area, red_ocean_dragon, 0.85, sw7)
            team2_dragons += team2_dragons_change
            team2_dragons_change, sw8, _ = event_template_match(event_area, red_mountain_dragon, 0.85, sw8)
            team2_dragons += team2_dragons_change
            team2_dragons_change, sw9, _ = event_template_match(event_area, red_cloud_dragon, 0.85, sw9)
            team2_dragons += team2_dragons_change
            team2_dragons_change, sw10, _ = event_template_match(event_area, red_elder_dragon, 0.85, sw10)
            team2_dragons += team2_dragons_change
            # print(team2_dragons)
            if team2_dragons != 0 and team2_dragons != prev_team2_dragons:
                # print(str(time.time() - start_time) + '  team2_dragons: ' + str(int(team2_dragons)))
                change += 1

            # ------------------------------------------------------ baron kills data ------------------------------
            prev_team1_barons = team1_barons
            team1_barons_change, sw11, _ = event_template_match(event_area, blue_baron, 0.7, sw11)

            team1_barons += team1_barons_change
            if team1_barons != 0 and team1_barons != prev_team1_barons:
                # print(str(time.time() - start_time) + '  team1_barons: ' + str(int(team1_barons)))
                change += 1

            prev_team2_barons = team2_barons
            team2_barons_change, sw12, _ = event_template_match(event_area, red_baron, 0.85, sw12)
            team2_barons += team2_barons_change
            if team2_barons != 0 and team2_barons == int(team2_barons) and team2_barons != prev_team2_barons:
                # print(str(time.time() - start_time) + '  team2_barons: ' + str(int(team2_barons)))
                change += 1

            # ------------------------------------------------------ rift kills data -------------------------------
            prev_team1_rifts = team1_rifts
            team1_rifts_change, sw13, _ = event_template_match(event_area, blue_rift, 0.75, sw13)

            team1_rifts += team1_rifts_change
            if team1_rifts != 0 and team1_rifts != prev_team1_rifts:
                # print(str(time.time() - start_time) + '  team1_rifts: ' + str(int(team1_rifts)))
                change += 1
            prev_team2_rifts = team2_rifts
            team2_rifts_change, sw14, _ = event_template_match(event_area, red_rift, 0.9, sw14)
            team2_rifts += team2_rifts_change
            if team2_rifts != 0 and team2_rifts == int(team2_rifts) and team2_rifts != prev_team2_rifts:
                # print(str(time.time() - start_time) + '  team2_rifts: ' + str(int(team2_rifts)))
                change += 1

            # ------------------------------------------------------ tower and inhib kills data --------------------
            prev_team1_towers = team1_towers
            team1_towers_change, sw15, prob_tower1 = event_template_match(event_area, blue_kill_tower, 0.8, sw15)
            prev_team1_inhibs = team1_inhibs
            team1_inhibs_change, sw16, prob_inhib1 = event_template_match(event_area, blue_kill_inhib, 0.8, sw16)
            team1_towers += team1_towers_change
            team1_inhibs += team1_inhibs_change

            if team1_towers != prev_team1_towers:
                print(str(time.time() - start_time) + '  team1_towers: ' + str(int(team1_towers)))
                change += 1
            if team1_inhibs != prev_team1_inhibs:
                print(str(time.time() - start_time) + '  team1_inhibs: ' + str(int(team1_inhibs)))
                change += 1

            prev_team2_towers = team2_towers
            team2_towers_change, sw17, prob_tower2 = event_template_match(event_area, red_kill_tower, 0.8, sw17)
            team2_towers += team2_towers_change

            prev_team2_inhibs = team2_inhibs
            team2_inhibs_change, sw18, prob_inhib2 = event_template_match(event_area, red_kill_inhib, 0.8, sw18)
            team2_inhibs += team2_inhibs_change

            if team2_towers != prev_team2_towers:
                # print(str(time.time() - start_time) + '  team2_towers: ' + str(int(team2_towers)))
                change += 1
            if team2_inhibs != prev_team2_inhibs:
                # print(str(time.time() - start_time) + '  team2_inhibs: ' + str(int(team2_inhibs)))
                change += 1

            if team1_towers == 1 and team2_towers == 0:
                team1_firstTower = 1
            if team1_towers == 0 and team2_towers == 1:
                team2_firstTower = 1
            if team1_inhibs == 1 and team2_inhibs == 0:
                team1_firstInhibitor = 1
            if team1_inhibs == 0 and team2_inhibs == 1:
                team2_firstInhibitor = 1
            if team1_dragons == 1 and team2_dragons == 0:
                team1_firstDragon = 1
            if team1_dragons == 0 and team2_dragons == 1:
                team2_firstDragon = 1
            if team1_barons == 1 and team2_barons == 0:
                team1_firstBaron = 1
            if team1_barons == 0 and team2_barons == 1:
                team2_firstBaron = 1
            if team1_rifts == 1 and team2_rifts == 0:
                team1_firstRiftHerald = 1
            if team1_rifts == 0 and team2_rifts == 1:
                team2_firstRiftHerald = 1



                # get player cs and kda
            prev_team1_p1_cs, prev_team1_p1_kills, prev_team1_p1_deaths, prev_team1_p1_assists = team1_p1_cs, team1_p1_kills, team1_p1_deaths, team1_p1_assists
            prev_team1_p2_cs, prev_team1_p2_kills, prev_team1_p2_deaths, prev_team1_p2_assists = team1_p2_cs, team1_p2_kills, team1_p2_deaths, team1_p2_assists
            prev_team1_p3_cs, prev_team1_p3_kills, prev_team1_p3_deaths, prev_team1_p3_assists = team1_p3_cs, team1_p3_kills, team1_p3_deaths, team1_p3_assists
            prev_team1_p4_cs, prev_team1_p4_kills, prev_team1_p4_deaths, prev_team1_p4_assists = team1_p4_cs, team1_p4_kills, team1_p4_deaths, team1_p4_assists
            prev_team1_p5_cs, prev_team1_p5_kills, prev_team1_p5_deaths, prev_team1_p5_assists = team1_p5_cs, team1_p5_kills, team1_p5_deaths, team1_p5_assists

            prev_team2_p1_cs, prev_team2_p1_kills, prev_team2_p1_deaths, prev_team2_p1_assists = team2_p1_cs, team2_p1_kills, team2_p1_deaths, team2_p1_assists
            prev_team2_p2_cs, prev_team2_p2_kills, prev_team2_p2_deaths, prev_team2_p2_assists = team2_p2_cs, team2_p2_kills, team2_p2_deaths, team2_p2_assists
            prev_team2_p3_cs, prev_team2_p3_kills, prev_team2_p3_deaths, prev_team2_p3_assists = team2_p3_cs, team2_p3_kills, team2_p3_deaths, team2_p3_assists
            prev_team2_p4_cs, prev_team2_p4_kills, prev_team2_p4_deaths, prev_team2_p4_assists = team2_p4_cs, team2_p4_kills, team2_p4_deaths, team2_p4_assists
            prev_team2_p5_cs, prev_team2_p5_kills, prev_team2_p5_deaths, prev_team2_p5_assists = team2_p5_cs, team2_p5_kills, team2_p5_deaths, team2_p5_assists

            team1_p1_cs = get_cs(team1_p1_cs_area)
            team1_p1_kills, team1_p1_deaths, team1_p1_assists = get_kda(team1_p1_kda_area)
            team1_p2_cs = get_cs(team1_p2_cs_area)
            team1_p2_kills, team1_p2_deaths, team1_p1_assists = get_kda(team1_p2_kda_area)
            team1_p3_cs = get_cs(team1_p3_cs_area)
            team1_p3_kills, team1_p3_deaths, team1_p1_assists = get_kda(team1_p3_kda_area)
            team1_p4_cs = get_cs(team1_p4_cs_area)
            team1_p4_kills, team1_p4_deaths, team1_p1_assists = get_kda(team1_p4_kda_area)
            team1_p5_cs = get_cs(team1_p5_cs_area)
            team1_p5_kills, team1_p5_deaths, team1_p1_assists = get_kda(team1_p5_kda_area)

            if prev_team1_p1_cs != team1_p1_cs:
                change += 1
                # print(f'{time.time() - start_time}  team1_p1_cs{team1_p1_cs}')
            if prev_team1_p2_cs != team1_p2_cs:
                change += 1
                # print(f'{time.time() - start_time}  team1_p2_cs{team1_p2_cs}')
            if prev_team1_p3_cs != team1_p3_cs:
                change += 1
                # print(f'{time.time() - start_time}  team1_p3_cs{team1_p3_cs}')
            if prev_team1_p4_cs != team1_p4_cs:
                change += 1
                # print(f'{time.time() - start_time}  team1_p4_cs{team1_p4_cs}')
            if prev_team1_p5_cs != team1_p5_cs:
                change += 1
                # print(f'{time.time() - start_time}  team1_p5_cs{team1_p5_cs}')
            if prev_team1_p1_kills != team1_p1_kills:
                change += 1
                # print(f'{time.time() - start_time}  team1_p1_kills{team1_p1_kills}')
            if prev_team1_p2_kills != team1_p2_kills:
                change += 1
                # print(f'{time.time() - start_time}  team1_p2_kills{team1_p2_kills}')
            if prev_team1_p3_kills != team1_p3_kills:
                change += 1
                # print(f'{time.time() - start_time}  team1_p3_kills{team1_p3_kills}')
            if prev_team1_p4_kills != team1_p4_kills:
                change += 1
                # print(f'{time.time() - start_time}  team1_p4_kills{team1_p4_kills}')
            if prev_team1_p5_kills != team1_p5_kills:
                change += 1
                # print(f'{time.time() - start_time}  team1_p5_kills{team1_p5_kills}')
            if prev_team1_p1_deaths != team1_p1_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team1_p1_deaths{team1_p1_deaths}')
            if prev_team1_p2_deaths != team1_p2_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team1_p2_deaths{team1_p2_deaths}')
            if prev_team1_p3_deaths != team1_p3_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team1_p3_deaths{team1_p3_deaths}')
            if prev_team1_p4_deaths != team1_p4_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team1_p4_deaths{team1_p4_deaths}')
            if prev_team1_p5_deaths != team1_p5_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team1_p5_deaths{team1_p5_deaths}')
            if prev_team1_p1_assists != team1_p1_assists:
                change += 1
                # print(f'{time.time() - start_time}  team1_p1_assists{team1_p1_assists}')
            if prev_team1_p2_assists != team1_p2_assists:
                change += 1
                # print(f'{time.time() - start_time}  team1_p2_assists{team1_p2_assists}')
            if prev_team1_p3_assists != team1_p3_assists:
                change += 1
                # print(f'{time.time() - start_time}  team1_p3_assists{team1_p3_assists}')
            if prev_team1_p4_assists != team1_p4_assists:
                change += 1
                # print(f'{time.time() - start_time}  team1_p4_assists{team1_p4_assists}')
            if prev_team1_p5_assists != team1_p5_assists:
                change += 1
                # print(f'{time.time() - start_time}  team1_p5_assists{team1_p5_assists}')

            team2_p1_cs = get_cs(team2_p1_cs_area)
            team2_p1_kills, team2_p1_deaths, team2_p1_assists = get_kda(team2_p1_kda_area)
            team2_p2_cs = get_cs(team2_p2_cs_area)
            team2_p2_kills, team2_p2_deaths, team2_p1_assists = get_kda(team2_p2_kda_area)
            team2_p3_cs = get_cs(team2_p3_cs_area)
            team2_p3_kills, team2_p3_deaths, team2_p1_assists = get_kda(team2_p3_kda_area)
            team2_p4_cs = get_cs(team2_p4_cs_area)
            team2_p4_kills, team2_p4_deaths, team2_p1_assists = get_kda(team2_p4_kda_area)
            team2_p5_cs = get_cs(team2_p5_cs_area)
            team2_p5_kills, team2_p5_deaths, team2_p1_assists = get_kda(team2_p5_kda_area)

            if prev_team2_p1_cs != team2_p1_cs:
                change += 1
                # print(f'{time.time() - start_time}  team2_p1_cs{team2_p1_cs}')
            if prev_team2_p2_cs != team2_p2_cs:
                change += 1
                # print(f'{time.time() - start_time}  team2_p2_cs{team2_p2_cs}')
            if prev_team2_p3_cs != team2_p3_cs:
                change += 1
                # print(f'{time.time() - start_time}  team2_p3_cs{team2_p3_cs}')
            if prev_team2_p4_cs != team2_p4_cs:
                change += 1
                # print(f'{time.time() - start_time}  team2_p4_cs{team2_p4_cs}')
            if prev_team2_p5_cs != team2_p5_cs:
                change += 1
                # print(f'{time.time() - start_time}  team2_p5_cs{team2_p5_cs}')
            if prev_team2_p1_kills != team2_p1_kills:
                change += 1
                # print(f'{time.time() - start_time}  team2_p1_kills{team2_p1_kills}')
            if prev_team2_p2_kills != team2_p2_kills:
                change += 1
                # print(f'{time.time() - start_time}  team2_p2_kills{team2_p2_kills}')
            if prev_team2_p3_kills != team2_p3_kills:
                change += 1
                # print(f'{time.time() - start_time}  team2_p3_kills{team2_p3_kills}')
            if prev_team2_p4_kills != team2_p4_kills:
                change += 1
                # print(f'{time.time() - start_time}  team2_p4_kills{team2_p4_kills}')
            if prev_team2_p5_kills != team2_p5_kills:
                change += 1
                # print(f'{time.time() - start_time}  team2_p5_kills{team2_p5_kills}')
            if prev_team2_p1_deaths != team2_p1_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team2_p1_deaths{team2_p1_deaths}')
            if prev_team2_p2_deaths != team2_p2_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team2_p2_deaths{team2_p2_deaths}')
            if prev_team2_p3_deaths != team2_p3_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team2_p3_deaths{team2_p3_deaths}')
            if prev_team2_p4_deaths != team2_p4_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team2_p4_deaths{team2_p4_deaths}')
            if prev_team2_p5_deaths != team2_p5_deaths:
                change += 1
                # print(f'{time.time() - start_time}  team2_p5_deaths{team2_p5_deaths}')
            if prev_team2_p1_assists != team2_p1_assists:
                change += 1
                # print(f'{time.time() - start_time}  team2_p1_assists{team2_p1_assists}')
            if prev_team2_p2_assists != team2_p2_assists:
                change += 1
                # print(f'{time.time() - start_time}  team2_p2_assists{team2_p2_assists}')
            if prev_team2_p3_assists != team2_p3_assists:
                change += 1
                # print(f'{time.time() - start_time}  team2_p3_assists{team2_p3_assists}')
            if prev_team2_p4_assists != team2_p4_assists:
                change += 1
                # print(f'{time.time() - start_time}  team2_p4_assists{team2_p4_assists}')
            if prev_team2_p5_assists != team2_p5_assists:
                change += 1
                # print(f'{time.time() - start_time}  team2_p5_assists{team2_p5_assists}')

            team1_kills = team1_p1_kills + team1_p2_kills + team1_p3_kills + team1_p4_kills + team1_p5_kills
            team2_kills = team2_p1_kills + team2_p2_kills + team2_p3_kills + team2_p4_kills + team2_p5_kills
            if team1_kills == 1 and team2_kills == 0:
                team1_firstBlood = 1
            if team1_kills == 0 and team2_kills == 1:
                team2_firstBlood = 1
            playerdata = {'team1_cs': [team1_p1_cs, team1_p2_cs, team1_p3_cs, team1_p4_cs, team1_p5_cs],
                          'team1_k': [team1_p1_kills, team1_p2_kills, team1_p3_kills, team1_p4_kills,
                                      team1_p5_kills],
                          'team1_d': [team1_p1_deaths, team1_p2_deaths, team1_p3_deaths, team1_p4_deaths,
                                      team1_p5_deaths],
                          'team1_a': [team1_p1_assists, team1_p2_assists, team1_p3_assists, team1_p4_assists,
                                      team1_p5_assists],
                          'team2_cs': [team2_p1_cs, team2_p2_cs, team2_p3_cs, team2_p4_cs, team2_p5_cs],
                          'team2_k': [team2_p1_kills, team2_p2_kills, team2_p3_kills, team2_p4_kills,
                                      team2_p5_kills],
                          'team2_d': [team2_p1_deaths, team2_p2_deaths, team2_p3_deaths, team2_p4_deaths,
                                      team2_p5_deaths],
                          'team2_a': [team2_p1_assists, team2_p2_assists, team2_p3_assists, team2_p4_assists,
                                      team2_p5_assists]
                          }
            teamdata = {'t1_tow': [team1_towers],
                        't1_in': [team1_inhibs],
                        't1_drg': [team1_dragons],
                        't1_rf': [team1_rifts],
                        't1_br': [team1_barons],
                        't2_tow': [team2_towers],
                        't2_in': [team2_inhibs],
                        't2_drg': [team2_dragons],
                        't2_rf': [team2_rifts],
                        't2_br': [team2_barons]
                        }
            # team1_p1_level = get_cs(team1_p1_level_area)
            # cv2.imshow('window', team1_p1_level_area)
            # print(team1_p1_level)
            # print(change)
            cv2.imshow('window', team1_p1_cs_area)
            if change > 0:
                # TODO: use the model to predict winrate if there is a change in match data below
                print(pd.DataFrame(teamdata))
                print(pd.DataFrame(playerdata))

                game_time = time.time() - start_time
                print(game_time)
                team1_p1_level = get_cs(team1_p1_level_area)
                team1_p2_level = get_cs(team1_p2_level_area)
                team1_p3_level = get_cs(team1_p3_level_area)
                team1_p4_level = get_cs(team1_p4_level_area)
                team1_p5_level = get_cs(team1_p5_level_area)
                team2_p1_level = get_cs(team2_p1_level_area)
                team2_p2_level = get_cs(team2_p2_level_area)
                team2_p3_level = get_cs(team2_p3_level_area)
                team2_p4_level = get_cs(team2_p4_level_area)
                team2_p5_level = get_cs(team2_p5_level_area)

                if game_time <= 300:
                    team1_p1_cs_5min = team1_p1_cs
                    team1_p1_gold_5min = team1_p1_kills * 300 + team1_p1_assists * 150 + team1_p1_cs * 30
                    team1_p1_level_5min = team1_p1_level
                    team1_p2_cs_5min = team1_p2_cs
                    team1_p2_gold_5min = team1_p2_kills * 300 + team1_p2_assists * 150 + team1_p2_cs * 30
                    team1_p2_level_5min = team1_p2_level
                    team1_p3_cs_5min = team1_p3_cs
                    team1_p3_gold_5min = team1_p3_kills * 300 + team1_p3_assists * 150 + team1_p3_cs * 30
                    team1_p3_level_5min = team1_p3_level
                    team1_p4_cs_5min = team1_p4_cs
                    team1_p4_gold_5min = team1_p4_kills * 300 + team1_p4_assists * 150 + team1_p4_cs * 30
                    team1_p4_level_5min = team1_p4_level
                    team1_p5_cs_5min = team1_p5_cs
                    team1_p5_gold_5min = team1_p5_kills * 300 + team1_p5_assists * 150 + team1_p5_cs * 30
                    team1_p5_level_5min = team1_p5_level
                    team2_p1_cs_5min = team2_p1_cs
                    team2_p1_gold_5min = team2_p1_kills * 300 + team2_p1_assists * 150 + team2_p1_cs * 30
                    team2_p1_level_5min = team2_p1_level
                    team2_p2_cs_5min = team2_p2_cs
                    team2_p2_gold_5min = team2_p2_kills * 300 + team2_p2_assists * 150 + team2_p2_cs * 30
                    team2_p2_level_5min = team2_p2_level
                    team2_p3_cs_5min = team2_p3_cs
                    team2_p3_gold_5min = team2_p3_kills * 300 + team2_p3_assists * 150 + team2_p3_cs * 30
                    team2_p3_level_5min = team2_p3_level
                    team2_p4_cs_5min = team2_p4_cs
                    team2_p4_gold_5min = team2_p4_kills * 300 + team2_p4_assists * 150 + team2_p4_cs * 30
                    team2_p4_level_5min = team2_p4_level
                    team2_p5_cs_5min = team2_p5_cs
                    team2_p5_gold_5min = team2_p5_kills * 300 + team2_p5_assists * 150 + team2_p5_cs * 30
                    team2_p5_level_5min = team2_p5_level
                if game_time <= 600:
                    team1_p1_cs_10min = team1_p1_cs
                    team1_p1_gold_10min = team1_p1_kills * 300 + team1_p1_assists * 150 + team1_p1_cs * 30
                    team1_p1_level_10min = team1_p1_level
                    team1_p2_cs_10min = team1_p2_cs
                    team1_p2_gold_10min = team1_p2_kills * 300 + team1_p2_assists * 150 + team1_p2_cs * 30
                    team1_p2_level_10min = team1_p2_level
                    team1_p3_cs_10min = team1_p3_cs
                    team1_p3_gold_10min = team1_p3_kills * 300 + team1_p3_assists * 150 + team1_p3_cs * 30
                    team1_p3_level_10min = team1_p3_level
                    team1_p4_cs_10min = team1_p4_cs
                    team1_p4_gold_10min = team1_p4_kills * 300 + team1_p4_assists * 150 + team1_p4_cs * 30
                    team1_p4_level_10min = team1_p4_level
                    team1_p5_cs_10min = team1_p5_cs
                    team1_p5_gold_10min = team1_p5_kills * 300 + team1_p5_assists * 150 + team1_p5_cs * 30
                    team1_p5_level_10min = team1_p5_level
                    team2_p1_cs_10min = team2_p1_cs
                    team2_p1_gold_10min = team2_p1_kills * 300 + team2_p1_assists * 150 + team2_p1_cs * 30
                    team2_p1_level_10min = team2_p1_level
                    team2_p2_cs_10min = team2_p2_cs
                    team2_p2_gold_10min = team2_p2_kills * 300 + team2_p2_assists * 150 + team2_p2_cs * 30
                    team2_p2_level_10min = team2_p2_level
                    team2_p3_cs_10min = team2_p3_cs
                    team2_p3_gold_10min = team2_p3_kills * 300 + team2_p3_assists * 150 + team2_p3_cs * 30
                    team2_p3_level_10min = team2_p3_level
                    team2_p4_cs_10min = team2_p4_cs
                    team2_p4_gold_10min = team2_p4_kills * 300 + team2_p4_assists * 150 + team2_p4_cs * 30
                    team2_p4_level_10min = team2_p4_level
                    team2_p5_cs_10min = team2_p5_cs
                    team2_p5_gold_10min = team2_p5_kills * 300 + team2_p5_assists * 150 + team2_p5_cs * 30
                    team2_p5_level_10min = team2_p5_level
                if game_time <= 900:
                    team1_p1_cs_15min = team1_p1_cs
                    team1_p1_gold_15min = team1_p1_kills * 300 + team1_p1_assists * 150 + team1_p1_cs * 30
                    team1_p1_level_15min = team1_p1_level
                    team1_p2_cs_15min = team1_p2_cs
                    team1_p2_gold_15min = team1_p2_kills * 300 + team1_p2_assists * 150 + team1_p2_cs * 30
                    team1_p2_level_15min = team1_p2_level
                    team1_p3_cs_15min = team1_p3_cs
                    team1_p3_gold_15min = team1_p3_kills * 300 + team1_p3_assists * 150 + team1_p3_cs * 30
                    team1_p3_level_15min = team1_p3_level
                    team1_p4_cs_15min = team1_p4_cs
                    team1_p4_gold_15min = team1_p4_kills * 300 + team1_p4_assists * 150 + team1_p4_cs * 30
                    team1_p4_level_15min = team1_p4_level
                    team1_p5_cs_15min = team1_p5_cs
                    team1_p5_gold_15min = team1_p5_kills * 300 + team1_p5_assists * 150 + team1_p5_cs * 30
                    team1_p5_level_15min = team1_p5_level
                    team2_p1_cs_15min = team2_p1_cs
                    team2_p1_gold_15min = team2_p1_kills * 300 + team2_p1_assists * 150 + team2_p1_cs * 30
                    team2_p1_level_15min = team2_p1_level
                    team2_p2_cs_15min = team2_p2_cs
                    team2_p2_gold_15min = team2_p2_kills * 300 + team2_p2_assists * 150 + team2_p2_cs * 30
                    team2_p2_level_15min = team2_p2_level
                    team2_p3_cs_15min = team2_p3_cs
                    team2_p3_gold_15min = team2_p3_kills * 300 + team2_p3_assists * 150 + team2_p3_cs * 30
                    team2_p3_level_15min = team2_p3_level
                    team2_p4_cs_15min = team2_p4_cs
                    team2_p4_gold_15min = team2_p4_kills * 300 + team2_p4_assists * 150 + team2_p4_cs * 30
                    team2_p4_level_15min = team2_p4_level
                    team2_p5_cs_15min = team2_p5_cs
                    team2_p5_gold_15min = team2_p5_kills * 300 + team2_p5_assists * 150 + team2_p5_cs * 30
                    team2_p5_level_15min = team2_p5_level
                if game_time <= 1200:
                    team1_p1_cs_20min = team1_p1_cs
                    team1_p1_gold_20min = team1_p1_kills * 300 + team1_p1_assists * 150 + team1_p1_cs * 30
                    team1_p1_level_20min = team1_p1_level
                    team1_p2_cs_20min = team1_p2_cs
                    team1_p2_gold_20min = team1_p2_kills * 300 + team1_p2_assists * 150 + team1_p2_cs * 30
                    team1_p2_level_20min = team1_p2_level
                    team1_p3_cs_20min = team1_p3_cs
                    team1_p3_gold_20min = team1_p3_kills * 300 + team1_p3_assists * 150 + team1_p3_cs * 30
                    team1_p3_level_20min = team1_p3_level
                    team1_p4_cs_20min = team1_p4_cs
                    team1_p4_gold_20min = team1_p4_kills * 300 + team1_p4_assists * 150 + team1_p4_cs * 30
                    team1_p4_level_20min = team1_p4_level
                    team1_p5_cs_20min = team1_p5_cs
                    team1_p5_gold_20min = team1_p5_kills * 300 + team1_p5_assists * 150 + team1_p5_cs * 30
                    team1_p5_level_20min = team1_p5_level
                    team2_p1_cs_20min = team2_p1_cs
                    team2_p1_gold_20min = team2_p1_kills * 300 + team2_p1_assists * 150 + team2_p1_cs * 30
                    team2_p1_level_20min = team2_p1_level
                    team2_p2_cs_20min = team2_p2_cs
                    team2_p2_gold_20min = team2_p2_kills * 300 + team2_p2_assists * 150 + team2_p2_cs * 30
                    team2_p2_level_20min = team2_p2_level
                    team2_p3_cs_20min = team2_p3_cs
                    team2_p3_gold_20min = team2_p3_kills * 300 + team2_p3_assists * 150 + team2_p3_cs * 30
                    team2_p3_level_20min = team2_p3_level
                    team2_p4_cs_20min = team2_p4_cs
                    team2_p4_gold_20min = team2_p4_kills * 300 + team2_p4_assists * 150 + team2_p4_cs * 30
                    team2_p4_level_20min = team2_p4_level
                    team2_p5_cs_20min = team2_p5_cs
                    team2_p5_gold_20min = team2_p5_kills * 300 + team2_p5_assists * 150 + team2_p5_cs * 30
                    team2_p5_level_20min = team2_p5_level
                if game_time <= 1500:
                    team1_p1_cs_25min = team1_p1_cs
                    team1_p1_gold_25min = team1_p1_kills * 300 + team1_p1_assists * 150 + team1_p1_cs * 30
                    team1_p1_level_25min = team1_p1_level
                    team1_p2_cs_25min = team1_p2_cs
                    team1_p2_gold_25min = team1_p2_kills * 300 + team1_p2_assists * 150 + team1_p2_cs * 30
                    team1_p2_level_25min = team1_p2_level
                    team1_p3_cs_25min = team1_p3_cs
                    team1_p3_gold_25min = team1_p3_kills * 300 + team1_p3_assists * 150 + team1_p3_cs * 30
                    team1_p3_level_25min = team1_p3_level
                    team1_p4_cs_25min = team1_p4_cs
                    team1_p4_gold_25min = team1_p4_kills * 300 + team1_p4_assists * 150 + team1_p4_cs * 30
                    team1_p4_level_25min = team1_p4_level
                    team1_p5_cs_25min = team1_p5_cs
                    team1_p5_gold_25min = team1_p5_kills * 300 + team1_p5_assists * 150 + team1_p5_cs * 30
                    team1_p5_level_25min = team1_p5_level
                    team2_p1_cs_25min = team2_p1_cs
                    team2_p1_gold_25min = team2_p1_kills * 300 + team2_p1_assists * 150 + team2_p1_cs * 30
                    team2_p1_level_25min = team2_p1_level
                    team2_p2_cs_25min = team2_p2_cs
                    team2_p2_gold_25min = team2_p2_kills * 300 + team2_p2_assists * 150 + team2_p2_cs * 30
                    team2_p2_level_25min = team2_p2_level
                    team2_p3_cs_25min = team2_p3_cs
                    team2_p3_gold_25min = team2_p3_kills * 300 + team2_p3_assists * 150 + team2_p3_cs * 30
                    team2_p3_level_25min = team2_p3_level
                    team2_p4_cs_25min = team2_p4_cs
                    team2_p4_gold_25min = team2_p4_kills * 300 + team2_p4_assists * 150 + team2_p4_cs * 30
                    team2_p4_level_25min = team2_p4_level
                    team2_p5_cs_25min = team2_p5_cs
                    team2_p5_gold_25min = team2_p5_kills * 300 + team2_p5_assists * 150 + team2_p5_cs * 30
                    team2_p5_level_25min = team2_p5_level
                if game_time > 1500:
                    team1_p1_cs_30min = team1_p1_cs
                    team1_p1_gold_30min = team1_p1_kills * 300 + team1_p1_assists * 150 + team1_p1_cs * 30
                    team1_p1_level_30min = team1_p1_level
                    team1_p2_cs_30min = team1_p2_cs
                    team1_p2_gold_30min = team1_p2_kills * 300 + team1_p2_assists * 150 + team1_p2_cs * 30
                    team1_p2_level_30min = team1_p2_level
                    team1_p3_cs_30min = team1_p3_cs
                    team1_p3_gold_30min = team1_p3_kills * 300 + team1_p3_assists * 150 + team1_p3_cs * 30
                    team1_p3_level_30min = team1_p3_level
                    team1_p4_cs_30min = team1_p4_cs
                    team1_p4_gold_30min = team1_p4_kills * 300 + team1_p4_assists * 150 + team1_p4_cs * 30
                    team1_p4_level_30min = team1_p4_level
                    team1_p5_cs_30min = team1_p5_cs
                    team1_p5_gold_30min = team1_p5_kills * 300 + team1_p5_assists * 150 + team1_p5_cs * 30
                    team1_p5_level_30min = team1_p5_level
                    team2_p1_cs_30min = team2_p1_cs
                    team2_p1_gold_30min = team2_p1_kills * 300 + team2_p1_assists * 150 + team2_p1_cs * 30
                    team2_p1_level_30min = team2_p1_level
                    team2_p2_cs_30min = team2_p2_cs
                    team2_p2_gold_30min = team2_p2_kills * 300 + team2_p2_assists * 150 + team2_p2_cs * 30
                    team2_p2_level_30min = team2_p2_level
                    team2_p3_cs_30min = team2_p3_cs
                    team2_p3_gold_30min = team2_p3_kills * 300 + team2_p3_assists * 150 + team2_p3_cs * 30
                    team2_p3_level_30min = team2_p3_level
                    team2_p4_cs_30min = team2_p4_cs
                    team2_p4_gold_30min = team2_p4_kills * 300 + team2_p4_assists * 150 + team2_p4_cs * 30
                    team2_p4_level_30min = team2_p4_level
                    team2_p5_cs_30min = team2_p5_cs
                    team2_p5_gold_30min = team2_p5_kills * 300 + team2_p5_assists * 150 + team2_p5_cs * 30
                    team2_p5_level_30min = team2_p5_level

                data_lst = []
                data_lst.append(team1_baronKills)
                data_lst.append(team1_riftKills)
                data_lst.append(team1_inhibitorKills)
                data_lst.append(team1_towerKills)
                data_lst.append(team1_dragonKills)
                data_lst.append(team2_baronKills)
                data_lst.append(team2_riftKills)
                data_lst.append(team2_inhibitorKills)
                data_lst.append(team2_towerKills)
                data_lst.append(team2_dragonKills)
                data_lst.append(team1_firstDragon)
                data_lst.append(team1_firstInhibitor)
                data_lst.append(team1_firstRiftHerald)
                data_lst.append(team1_firstBaron)
                data_lst.append(team1_firstBlood)
                data_lst.append(team1_firstTower)
                data_lst.append(team2_firstDragon)
                data_lst.append(team2_firstInhibitor)
                data_lst.append(team2_firstRiftHerald)
                data_lst.append(team2_firstBaron)
                data_lst.append(team2_firstBlood)
                data_lst.append(team2_firstTower)
                data_lst.append(game_time)
                data_lst.append(team1_p1_gold_10min)
                data_lst.append(team1_p1_gold_15min)
                data_lst.append(team1_p1_gold_20min)
                data_lst.append(team1_p1_gold_25min)
                data_lst.append(team1_p1_gold_30min)
                data_lst.append(team1_p1_gold_5min)
                data_lst.append(team1_p2_gold_10min)
                data_lst.append(team1_p2_gold_15min)
                data_lst.append(team1_p2_gold_20min)
                data_lst.append(team1_p2_gold_25min)
                data_lst.append(team1_p2_gold_30min)
                data_lst.append(team1_p2_gold_5min)
                data_lst.append(team1_p3_gold_10min)
                data_lst.append(team1_p3_gold_15min)
                data_lst.append(team1_p3_gold_20min)
                data_lst.append(team1_p3_gold_25min)
                data_lst.append(team1_p3_gold_30min)
                data_lst.append(team1_p3_gold_5min)
                data_lst.append(team1_p4_gold_10min)
                data_lst.append(team1_p4_gold_15min)
                data_lst.append(team1_p4_gold_20min)
                data_lst.append(team1_p4_gold_25min)
                data_lst.append(team1_p4_gold_30min)
                data_lst.append(team1_p4_gold_5min)
                data_lst.append(team1_p5_gold_10min)
                data_lst.append(team1_p5_gold_15min)
                data_lst.append(team1_p5_gold_20min)
                data_lst.append(team1_p5_gold_25min)
                data_lst.append(team1_p5_gold_30min)
                data_lst.append(team1_p5_gold_5min)
                data_lst.append(team2_p1_gold_10min)
                data_lst.append(team2_p1_gold_15min)
                data_lst.append(team2_p1_gold_20min)
                data_lst.append(team2_p1_gold_25min)
                data_lst.append(team2_p1_gold_30min)
                data_lst.append(team2_p1_gold_5min)
                data_lst.append(team2_p2_gold_10min)
                data_lst.append(team2_p2_gold_15min)
                data_lst.append(team2_p2_gold_20min)
                data_lst.append(team2_p2_gold_25min)
                data_lst.append(team2_p2_gold_30min)
                data_lst.append(team2_p2_gold_5min)
                data_lst.append(team2_p3_gold_10min)
                data_lst.append(team2_p3_gold_15min)
                data_lst.append(team2_p3_gold_20min)
                data_lst.append(team2_p3_gold_25min)
                data_lst.append(team2_p3_gold_30min)
                data_lst.append(team2_p3_gold_5min)
                data_lst.append(team2_p4_gold_10min)
                data_lst.append(team2_p4_gold_15min)
                data_lst.append(team2_p4_gold_20min)
                data_lst.append(team2_p4_gold_25min)
                data_lst.append(team2_p4_gold_30min)
                data_lst.append(team2_p4_gold_5min)
                data_lst.append(team2_p5_gold_10min)
                data_lst.append(team2_p5_gold_15min)
                data_lst.append(team2_p5_gold_20min)
                data_lst.append(team2_p5_gold_25min)
                data_lst.append(team2_p5_gold_30min)
                data_lst.append(team2_p5_gold_5min)
                data_lst.append(team1_p1_cs_5min)
                data_lst.append(team1_p1_cs_10min)
                data_lst.append(team1_p1_cs_15min)
                data_lst.append(team1_p1_cs_20min)
                data_lst.append(team1_p1_cs_25min)
                data_lst.append(team1_p1_cs_30min)
                data_lst.append(team1_p2_cs_5min)
                data_lst.append(team1_p2_cs_10min)
                data_lst.append(team1_p2_cs_15min)
                data_lst.append(team1_p2_cs_20min)
                data_lst.append(team1_p2_cs_25min)
                data_lst.append(team1_p2_cs_30min)
                data_lst.append(team1_p3_cs_5min)
                data_lst.append(team1_p3_cs_10min)
                data_lst.append(team1_p3_cs_15min)
                data_lst.append(team1_p3_cs_20min)
                data_lst.append(team1_p3_cs_25min)
                data_lst.append(team1_p3_cs_30min)
                data_lst.append(team1_p4_cs_5min)
                data_lst.append(team1_p4_cs_10min)
                data_lst.append(team1_p4_cs_15min)
                data_lst.append(team1_p4_cs_20min)
                data_lst.append(team1_p4_cs_25min)
                data_lst.append(team1_p4_cs_30min)
                data_lst.append(team1_p5_cs_5min)
                data_lst.append(team1_p5_cs_10min)
                data_lst.append(team1_p5_cs_15min)
                data_lst.append(team1_p5_cs_20min)
                data_lst.append(team1_p5_cs_25min)
                data_lst.append(team1_p5_cs_30min)
                data_lst.append(team2_p1_cs_5min)
                data_lst.append(team2_p1_cs_10min)
                data_lst.append(team2_p1_cs_15min)
                data_lst.append(team2_p1_cs_20min)
                data_lst.append(team2_p1_cs_25min)
                data_lst.append(team2_p1_cs_30min)
                data_lst.append(team2_p2_cs_5min)
                data_lst.append(team2_p2_cs_10min)
                data_lst.append(team2_p2_cs_15min)
                data_lst.append(team2_p2_cs_20min)
                data_lst.append(team2_p2_cs_25min)
                data_lst.append(team2_p2_cs_30min)
                data_lst.append(team2_p3_cs_5min)
                data_lst.append(team2_p3_cs_10min)
                data_lst.append(team2_p3_cs_15min)
                data_lst.append(team2_p3_cs_20min)
                data_lst.append(team2_p3_cs_25min)
                data_lst.append(team2_p3_cs_30min)
                data_lst.append(team2_p4_cs_5min)
                data_lst.append(team2_p4_cs_10min)
                data_lst.append(team2_p4_cs_15min)
                data_lst.append(team2_p4_cs_20min)
                data_lst.append(team2_p4_cs_25min)
                data_lst.append(team2_p4_cs_30min)
                data_lst.append(team2_p5_cs_5min)
                data_lst.append(team2_p5_cs_10min)
                data_lst.append(team2_p5_cs_15min)
                data_lst.append(team2_p5_cs_20min)
                data_lst.append(team2_p5_cs_25min)
                data_lst.append(team2_p5_cs_30min)
                columns = [
                    'team1_baronKills',
                    'team1_riftKills',
                    'team1_inhibitorKills',
                    'team1_towerKills',
                    'team1_dragonKills',
                    'team2_baronKills',
                    'team2_riftKills',
                    'team2_inhibitorKills',
                    'team2_towerKills',
                    'team2_dragonKills',
                    'team1_firstDragon',
                    'team1_firstInhibitor',
                    'team1_firstRiftHerald',
                    'team1_firstBaron',
                    'team1_firstBlood',
                    'team1_firstTower',
                    'team2_firstDragon',
                    'team2_firstInhibitor',
                    'team2_firstRiftHerald',
                    'team2_firstBaron',
                    'team2_firstBlood',
                    'team2_firstTower',
                    'game_time',
                    'team1_p1_gold_10min',
                    'team1_p1_gold_15min',
                    'team1_p1_gold_20min',
                    'team1_p1_gold_25min',
                    'team1_p1_gold_30min',
                    'team1_p1_gold_5min',
                    'team1_p2_gold_10min',
                    'team1_p2_gold_15min',
                    'team1_p2_gold_20min',
                    'team1_p2_gold_25min',
                    'team1_p2_gold_30min',
                    'team1_p2_gold_5min',
                    'team1_p3_gold_10min',
                    'team1_p3_gold_15min',
                    'team1_p3_gold_20min',
                    'team1_p3_gold_25min',
                    'team1_p3_gold_30min',
                    'team1_p3_gold_5min',
                    'team1_p4_gold_10min',
                    'team1_p4_gold_15min',
                    'team1_p4_gold_20min',
                    'team1_p4_gold_25min',
                    'team1_p4_gold_30min',
                    'team1_p4_gold_5min',
                    'team1_p5_gold_10min',
                    'team1_p5_gold_15min',
                    'team1_p5_gold_20min',
                    'team1_p5_gold_25min',
                    'team1_p5_gold_30min',
                    'team1_p5_gold_5min',
                    'team2_p1_gold_10min',
                    'team2_p1_gold_15min',
                    'team2_p1_gold_20min',
                    'team2_p1_gold_25min',
                    'team2_p1_gold_30min',
                    'team2_p1_gold_5min',
                    'team2_p2_gold_10min',
                    'team2_p2_gold_15min',
                    'team2_p2_gold_20min',
                    'team2_p2_gold_25min',
                    'team2_p2_gold_30min',
                    'team2_p2_gold_5min',
                    'team2_p3_gold_10min',
                    'team2_p3_gold_15min',
                    'team2_p3_gold_20min',
                    'team2_p3_gold_25min',
                    'team2_p3_gold_30min',
                    'team2_p3_gold_5min',
                    'team2_p4_gold_10min',
                    'team2_p4_gold_15min',
                    'team2_p4_gold_20min',
                    'team2_p4_gold_25min',
                    'team2_p4_gold_30min',
                    'team2_p4_gold_5min',
                    'team2_p5_gold_10min',
                    'team2_p5_gold_15min',
                    'team2_p5_gold_20min',
                    'team2_p5_gold_25min',
                    'team2_p5_gold_30min',
                    'team2_p5_gold_5min',
                    'team1_p1_total_cs_5min',
                    'team1_p1_total_cs_10min',
                    'team1_p1_total_cs_15min',
                    'team1_p1_total_cs_20min',
                    'team1_p1_total_cs_25min',
                    'team1_p1_total_cs_30min',
                    'team1_p2_total_cs_5min',
                    'team1_p2_total_cs_10min',
                    'team1_p2_total_cs_15min',
                    'team1_p2_total_cs_20min',
                    'team1_p2_total_cs_25min',
                    'team1_p2_total_cs_30min',
                    'team1_p3_total_cs_5min',
                    'team1_p3_total_cs_10min',
                    'team1_p3_total_cs_15min',
                    'team1_p3_total_cs_20min',
                    'team1_p3_total_cs_25min',
                    'team1_p3_total_cs_30min',
                    'team1_p4_total_cs_5min',
                    'team1_p4_total_cs_10min',
                    'team1_p4_total_cs_15min',
                    'team1_p4_total_cs_20min',
                    'team1_p4_total_cs_25min',
                    'team1_p4_total_cs_30min',
                    'team1_p5_total_cs_5min',
                    'team1_p5_total_cs_10min',
                    'team1_p5_total_cs_15min',
                    'team1_p5_total_cs_20min',
                    'team1_p5_total_cs_25min',
                    'team1_p5_total_cs_30min',
                    'team2_p1_total_cs_5min',
                    'team2_p1_total_cs_10min',
                    'team2_p1_total_cs_15min',
                    'team2_p1_total_cs_20min',
                    'team2_p1_total_cs_25min',
                    'team2_p1_total_cs_30min',
                    'team2_p2_total_cs_5min',
                    'team2_p2_total_cs_10min',
                    'team2_p2_total_cs_15min',
                    'team2_p2_total_cs_20min',
                    'team2_p2_total_cs_25min',
                    'team2_p2_total_cs_30min',
                    'team2_p3_total_cs_5min',
                    'team2_p3_total_cs_10min',
                    'team2_p3_total_cs_15min',
                    'team2_p3_total_cs_20min',
                    'team2_p3_total_cs_25min',
                    'team2_p3_total_cs_30min',
                    'team2_p4_total_cs_5min',
                    'team2_p4_total_cs_10min',
                    'team2_p4_total_cs_15min',
                    'team2_p4_total_cs_20min',
                    'team2_p4_total_cs_25min',
                    'team2_p4_total_cs_30min',
                    'team2_p5_total_cs_5min',
                    'team2_p5_total_cs_10min',
                    'team2_p5_total_cs_15min',
                    'team2_p5_total_cs_20min',
                    'team2_p5_total_cs_25min',
                    'team2_p5_total_cs_30min'
                ]

                X = np.array(data_lst)
                X = X.reshape((1, -1))
                X = pd.DataFrame(X, columns=columns)
                # print(X.shape)
                print(X['team2_p1_total_cs_5min'])
                winrate_model = pickle.load(open('finalized_model_2.sav', 'rb'))
                print(f'Win/Loss: {winrate_model.predict(X)}')
                print(f'winrate: {winrate_model.predict_proba(X)}')
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


# ------------- helper function ---------------------------------------------------------------------------------------
def event_template_match(scene, template, th, sw, debug=False):
    res = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
    minmax = cv2.minMaxLoc(res)
    _, max_val, _, max_loc = minmax
    corner1 = max_loc
    corner2 = (max_loc[0] + template[1], max_loc[1] + template[0])
    # cv2.rectangle(scene, corner1, corner2, (255, 0, 0), 3)
    # cv2.imshow("output", scene)
    prev_sw = sw
    if debug:
        print(f'prob: {max_val}, sw: {sw}, prev_sw: {prev_sw}')
    if max_val > th:
        sw = 1
    else:
        sw = 0

    if sw == 0 and prev_sw == 1:
        print('event happened')
        return 1, 0, max_val
    return 0, sw, max_val


def train_digits(img):
    """
    create training data by manually input number label, save training data to file
    :return: None
    """
    im = cv2.imread(img)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.THRESH_BINARY_INV, 1, 3, 3)

    #################      Now finding Contours         ###################

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    samples = np.empty((0, 100))
    responses = []
    keys = [i for i in range(47, 58)]

    for cnt in contours:
        if 5 < cv2.contourArea(cnt) < 100:
            [x, y, w, h] = cv2.boundingRect(cnt)
            print(w, h)
            if 10 < h and 6 < w:
                temp = im.copy()
                cv2.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 1)
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                cv2.imshow('norm', temp)
                key = cv2.waitKey(0)

                if key == 27:  # (escape to quit)
                    sys.exit()
                elif key in keys:
                    if key == 47:
                        responses.append(11)
                    else:
                        responses.append(int(chr(key)))
                    sample = roismall.reshape((1, 100))
                    samples = np.append(samples, sample, 0)

    responses = np.array(responses, np.float32)
    responses = responses.reshape((responses.size, 1))

    np.savetxt('generalsamples1.data', samples)
    np.savetxt('generalresponses1.data', responses)


def get_cs(scene):
    """
    return recognized minions killed
    :param scene:
    :return: int
    """
    # fit model using training data
    samples = np.loadtxt('generalsamples.data', np.float32)
    responses = np.loadtxt('generalresponses.data', np.float32)
    responses = responses.reshape((responses.size, 1))
    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
    # predict digit
    gray = cv2.cvtColor(scene, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 3)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    digits = []
    position = []
    appeared = {}
    # print(f'number of contours: {len(contours)}')
    for cnt in contours:
        if 5 < cv2.contourArea(cnt) < 150:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if (5 < w < 13 and h > 10) or (14 < w < 18 and h > 10):
                if 5 < w < 13:
                    roi = thresh[y:y + h, x:x + w]
                    # cv2.imshow('window', roi)
                    # cv2.waitKey(0)
                    roismall = cv2.resize(roi, (10, 10))
                    roismall = roismall.reshape((1, 100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                    if x-1 not in appeared and x+1 not in appeared and x not in appeared:
                        appeared[x] = [results[0][0], dists[0][0]]
                        if dists[0][0] < 1000000 or (results[0][0] == 1 and dists[0][0] < 1500000):
                            digit = int((results[0][0]))
                            digits.append(digit)
                            position.append(x)
                    elif x-1 in appeared:
                        if dists[0][0] < appeared[x-1][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x-1][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
                    elif x+1 in appeared:
                        if dists[0][0] < appeared[x+1][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x+1][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
                    elif x in appeared:
                        if dists[0][0] < appeared[x][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
                if 14 < w < 18:
                    roi1 = thresh[y:y + h, x:x + w - int(w/2)]
                    roismall1 = cv2.resize(roi1, (10, 10))
                    roismall1 = roismall1.reshape((1, 100))
                    roismall1 = np.float32(roismall1)
                    retval, results, neigh_resp, dists = model.findNearest(roismall1, k=1)
                    if x-1 not in appeared and x+1 not in appeared and x not in appeared:
                        appeared[x] = [results[0][0], dists[0][0]]
                        if dists[0][0] < 1000000 or (results[0][0] == 1 and dists[0][0] < 1500000):
                            digit = int((results[0][0]))
                            digits.append(digit)
                            position.append(x)
                    elif x-1 in appeared:
                        if dists[0][0] < appeared[x-1][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x-1][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
                    elif x+1 in appeared:
                        if dists[0][0] < appeared[x+1][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x+1][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
                    elif x in appeared:
                        if dists[0][0] < appeared[x][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
                    roi2 = thresh[y:y + h, x + int(w/2):x + w]
                    x += int(w/2)
                    roismall2 = cv2.resize(roi2, (10, 10))
                    roismall2 = roismall2.reshape((1, 100))
                    roismall2 = np.float32(roismall2)
                    retval, results, neigh_resp, dists = model.findNearest(roismall2, k=1)
                    if x-1 not in appeared and x+1 not in appeared and x not in appeared:
                        appeared[x] = [results[0][0], dists[0][0]]
                        if dists[0][0] < 1000000 or (results[0][0] == 1 and dists[0][0] < 1500000):
                            digit = int((results[0][0]))
                            digits.append(digit)
                            position.append(x)
                    elif x-1 in appeared:
                        if dists[0][0] < appeared[x-1][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x-1][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
                    elif x+1 in appeared:
                        if dists[0][0] < appeared[x+1][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x+1][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
                    elif x in appeared:
                        if dists[0][0] < appeared[x][1]:
                            rm_idx = [i for i in range(len(digits)) if digits[i] == appeared[x][0]][-1]
                            digits.pop(rm_idx)
                            digit = int((results[0][0]))
                            digits.append(digit)
    if len(digits) != 0:
        position, digits = zip(*sorted(zip(position, digits)))
        # print(digits)
        # print(position)
        return concat_number_from_lst(digits)
    return 0


def get_kda(scene):
    """
    return recognized minions killed
    :param scene:
    :return: int
    """
    # fit model using training data
    samples = np.loadtxt('generalsamples.data', np.float32)
    responses = np.loadtxt('generalresponses.data', np.float32)
    responses = responses.reshape((responses.size, 1))
    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
    # predict digit
    gray = cv2.cvtColor(scene, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 4)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    digits = []
    position = []
    appeared = {}
    for cnt in contours:
        if 5 < cv2.contourArea(cnt) < 150:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > 8:
                # print(f'position: {x}, {w}, {h}')
                roi = thresh[y:y + h, x:x + w]
                # cv2.imshow('window', roi)
                # cv2.waitKey(0)
                roismall = cv2.resize(roi, (10, 10))
                roismall = roismall.reshape((1, 100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                if x-1 not in appeared and x+1 not in appeared and x not in appeared:
                    appeared[x] = dists[0][0]
                    # print(results[0][0], dists[0][0])
                    if dists[0][0] < 900000 or ((results[0][0] == 1 or results [0][0] == 11) and dists[0][0] < 1500000):
                        digit = int((results[0][0]))
                        digits.append(digit)
                        position.append(x)
                elif x-1 in appeared:
                    if dists[0][0] < appeared[x-1]:
                        digit = int(results[0][0])
                        digits.append(digit)
                        position.append(x)
                elif x+1 in appeared:
                    if dists[0][0] < appeared[x+1]:
                        digit = int(results[0][0])
                        digits.append(digit)
                        position.append(x)
                elif x in appeared:
                    if dists[0][0] < appeared[x]:
                        digit = int(results[0][0])
                        digits.append(digit)
                        position.append(x)
    # print(digits)
    if len(digits) != 0:
        position, digits = zip(*sorted(zip(position, digits)))
        slash_index = [i for i, d in enumerate(digits) if d == 11]
        if len(slash_index) != 0 and len(slash_index) == 2 and slash_index[1] + 1 <= len(digits):
            # print(slash_index)
            # print(digits)
            kills_lst = digits[:slash_index[0]]
            deaths_lst = digits[slash_index[0] + 1: slash_index[1]]
            assists_lst = digits[slash_index[1] + 1:]
            kills = concat_number_from_lst(kills_lst)
            deaths = concat_number_from_lst(deaths_lst)
            assists = concat_number_from_lst(assists_lst)
            return kills, deaths, assists
    return 0, 0, 0


def concat_number_from_lst(lst):
    num = 0
    num_digits = len(lst)
    for i, d in enumerate(lst):
        num += d * (10 ** (num_digits - 1 - i))
    return num


def concat_file(path, name):
    output_df = pd.DataFrame()
    for filename in glob.glob(f'{path}*.csv'):
        temp_df = pd.read_csv(filename)
        output_df = pd.concat([output_df, temp_df], ignore_index=True)
    output_df = output_df.drop(columns=['Unnamed: 0'])
    output_df.to_csv(name)


def convert_str_int(s):
    if s == 'true' or s == '"Win"' or s == 'Win':
        return 1
    return 0


if __name__ == '__main__':
    # concat_file('./match_timeline/', 'full_matchtimeline.csv')
    # ------------------------------------
    # concat_file('C:/Users/rober/OneDrive/csc/lol-ml/matchid/', 'full_matchid.csv')
    # matchid_df = pd.read_csv('full_matchid.csv', index_col=0)
    # matchid_df = matchid_df.drop_duplicates()
    # idx = 0
    # lst = [0]
    # for l in range(22):
    #     idx += 46323
    #     lst.append(idx)
    #


    # concat_file('C:/Users/rober/OneDrive/csc/lol-ml/match_detail/', 'full_matchdata.csv')
    # matchid_df = pd.read_csv('matchid.csv', index_col=0)
    # idx = 0
    # lst = [0]
    # for l in range(22):
    #     idx += 15236
    #     lst.append(idx)
    #
    # matchid0 = matchid_df.iloc[lst[0]:lst[0 + 1]]
    # matchid1 = matchid_df.iloc[lst[1]:lst[1 + 1]]
    # matchid2 = matchid_df.iloc[lst[2]:lst[2 + 1]]
    # matchid3 = matchid_df.iloc[lst[3]:lst[3 + 1]]
    # matchid4 = matchid_df.iloc[lst[4]:lst[4 + 1]]
    # matchid5 = matchid_df.iloc[lst[5]:lst[5 + 1]]
    # matchid6 = matchid_df.iloc[lst[6]:lst[6 + 1]]
    # matchid7 = matchid_df.iloc[lst[7]:lst[7 + 1]]
    # matchid8 = matchid_df.iloc[lst[8]:lst[8 + 1]]
    # matchid9 = matchid_df.iloc[lst[9]:lst[9 + 1]]
    # matchid10 = matchid_df.iloc[lst[10]:lst[10 + 1]]
    # matchid11 = matchid_df.iloc[lst[11]:lst[11 + 1]]
    # matchid12 = matchid_df.iloc[lst[12]:lst[12 + 1]]
    # matchid13 = matchid_df.iloc[lst[13]:lst[13 + 1]]
    # matchid14 = matchid_df.iloc[lst[14]:lst[14 + 1]]
    # matchid15 = matchid_df.iloc[lst[15]:lst[15 + 1]]
    # matchid16 = matchid_df.iloc[lst[16]:lst[16 + 1]]
    # matchid17 = matchid_df.iloc[lst[17]:lst[17 + 1]]
    # matchid18 = matchid_df.iloc[lst[18]:lst[18 + 1]]
    # matchid19 = matchid_df.iloc[lst[19]:lst[19 + 1]]
    # matchid20 = matchid_df.iloc[lst[20]:lst[20 + 1]]
    # matchid21 = matchid_df.iloc[lst[21]:]
    # #

    # multi_get_timeline(matchid0, 0, api_key0)
    # multi_get_timeline(matchid1, 1, api_key1)
    # multi_get_timeline(matchid2, 2, api_key2)
    # multi_get_timeline(matchid3, 3, api_key3)
    # multi_get_timeline(matchid4, 4, api_key4)
    # multi_get_timeline(matchid5, 5, api_key5)
    # multi_get_timeline(matchid6, 6, api_key6)
    # multi_get_timeline(matchid7, 7, api_key7)
    # multi_get_timeline(matchid8, 8, api_key8)
    # multi_get_timeline(matchid9, 9, api_key9)
    # multi_get_timeline(matchid10, 10, api_key10)
    # multi_get_timeline(matchid11, 11, api_key11)
    # multi_get_timeline(matchid12, 12, api_key12)
    # multi_get_timeline(matchid13, 13, api_key13)
    # multi_get_timeline(matchid14, 14, api_key14)
    # multi_get_timeline(matchid15, 15, api_key15)
    # multi_get_timeline(matchid16, 16, api_key16)
    # multi_get_timeline(matchid17, 17, api_key17)
    # multi_get_timeline(matchid18, 18, api_key18)
    # multi_get_timeline(matchid19, 19, api_key19)
    # multi_get_timeline(matchid20, 20, api_key20)
    # multi_get_timeline(matchid21, 21, api_key21)

    # concat_file('./match_timeline/', 'full_matchtimeline.csv')
    # train_digits('./New Folder/Layer 1.png')
    # pd.set_option('display.max_columns', 10)
    champ_df = pd.read_csv('champ_keys.csv')
    begin_prediction(['Ashe', 'Vayne', 'Lucian', 'Kaisa', 'Leona'], ['Ashe', 'Vayne', 'Lucian', 'Kaisa', 'Ezreal'])
    # get_cs(cv2.imread('testdigit .png'))






