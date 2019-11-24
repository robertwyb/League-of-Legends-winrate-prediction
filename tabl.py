import pandas as pd

df = pd.read_csv('uber-apr-jul.csv')
df['date'] = pd.to_datetime(df['Date/Time']).dt.date
# df.to_csv('uber-data.csv')