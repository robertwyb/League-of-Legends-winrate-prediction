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
    return dictionary contain team info extract from api returned result
    :param data: api return
    :return: dictionary
    """
    result = {}
    for i in range(len(data['teams'])):
        team = data['teams'][i]
        result[f'team{i+1}_win'] = convert_str_int(team['win'])
        result[f'team{i+1}_firstDragon'] = convert_str_int(team['firstDragon'])
        result[f'team{i+1}_firstInhibitor'] = convert_str_int(team['firstInhibitor'])
        result[f'team{i+1}_firstRiftHerald'] = convert_str_int(team['firstRiftHerald'])
        result[f'team{i+1}_firstBaron'] = convert_str_int(team['firstBaron'])
        result[f'team{i+1}_firstBlood'] = convert_str_int(team['firstBlood'])
        result[f'team{i+1}_firstTower'] = convert_str_int(team['firstTower'])
        result[f'team{i+1}_baronKills'] = team['baronKills']
        result[f'team{i+1}_riftKills'] = team['riftHeraldKills']
        result[f'team{i+1}_inhibitorKills'] = team['inhibitorKills']
        result[f'team{i+1}_towerKills'] = team['towerKills']
        result[f'team{i+1}_dragonKills'] = team['dragonKills']
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
            result[f'team{team}_p{p}_dmg_taken_diff_permin0'] = player['timeline']['damageTakenDiffPerMinDeltas']['0-10']
        except:
            result[f'team{team}_p{p}_dmg_taken_diff_permin0'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_diff_permin1'] = player['timeline']['damageTakenDiffPerMinDeltas']['10-20']
        except:
            result[f'team{team}_p{p}_dmg_taken_diff_permin1'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_diff_permin2'] = player['timeline']['damageTakenDiffPerMinDeltas']['20-30']
        except:
            result[f'team{team}_p{p}_dmg_taken_diff_permin2'] = np.nan
        try:
            result[f'team{team}_p{p}_dmg_taken_diff_permin3'] = player['timeline']['damageTakenDiffPerMinDeltas']['30-end']
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
        result[f'team{team}_p{p}_fbAssist'] = convert_str_int(player['stats']['firstBloodAssist'])
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
        result[f'team{team}_p{p}_firstBloodKill'] = convert_str_int(player['stats']['firstBloodKill'])
        result[f'team{team}_p{p}_totalDamageDealt'] = player['stats']['totalDamageDealt']
        result[f'team{team}_p{p}_trueDamage_champion'] = player['stats']['trueDamageDealtToChampions']
        result[f'team{team}_p{p}_goldEarned'] = player['stats']['goldEarned']
        result[f'team{team}_p{p}_firstTowerAssists'] = convert_str_int(player['stats']['firstTowerAssist'])
        result[f'team{team}_p{p}_firstTowerKill'] = convert_str_int(player['stats']['firstTowerKill'])
        result[f'team{team}_p{p}_champLevel'] = player['stats']['champLevel']
        result[f'team{team}_p{p}_pink'] = player['stats']['visionWardsBoughtInGame']
        result[f'team{team}_p{p}_pentakills'] = player['stats']['pentaKills']
        result[f'team{team}_p{p}_totalHeal'] = player['stats']['totalHeal']
        result[f'team{team}_p{p}_totalMinionsKilled'] = player['stats']['totalMinionsKilled']
        result[f'team{team}_p{p}_timeCC'] = player['stats']['timeCCingOthers']
    return result


def get_match_detail(matchId, api_key):
    match_detail = {}
    url = f'https://na1.api.riotgames.com/lol/match/v4/matches/{matchId}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    if 'gameId' in data:
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
    result = pd.DataFrame()
    for i in df['matchid']:
        dft = get_match_detail(i, api_key)
        time.sleep(1)
        result = pd.concat([result, dft], ignore_index=True)
    result.to_csv(f'./match/match_{num}.csv')



# helper function
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


def save_obj(obj, name):
    with open('data/'+ name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    print()




