import pandas as pd

df = pd.read_csv('full_matchtimeline.csv', index_col=0)

df_1 = pd.read_csv('full_matchdata.csv', index_col=0)
df_2 = pd.read_csv('champ_select.csv')
