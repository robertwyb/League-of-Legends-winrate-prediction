import json
import pandas as pd

with open('champion.json', 'rb') as champ_json:
    loaded_json = json.load(champ_json)

champ_list = list(loaded_json['data'].keys())


champ_key_list = []
champ_tags_list = []
for champ in champ_list:
    champ_key = int(loaded_json['data'][champ]['key'])
    champ_key_list.append(champ_key)
    champ_tags = loaded_json['data'][champ]['tags']
    champ_tags_list.append(champ_tags)

df = pd.DataFrame(list(zip(champ_list, champ_key_list, champ_tags_list)),
                  columns=['Champ_Name', 'Champ_Key', 'Champ_Tags'])
df.to_csv('champ_keys')
