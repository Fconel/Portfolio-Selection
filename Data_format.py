import pandas as pd
from pathlib import Path

#Load all data
data_BTC = pd.read_csv(Path("Prices\BTCUSD.csv")) 
data_ETH = pd.read_csv(Path("Prices\ETHUSD.csv")) 
data_ADA = pd.read_csv(Path("Prices\ADAUSD.csv")) 

#Keep relevant data, in this case date and close price
data_BTC.drop(data_BTC.columns.difference(['date','close']), 1, inplace=True)
data_ETH.drop(data_ETH.columns.difference(['date','close']), 1, inplace=True)
data_ADA.drop(data_ADA.columns.difference(['date','close']), 1, inplace=True)

#Rename colums
data_BTC.columns = ['date', 'BTC']
data_ETH.columns = ['date', 'ETH']
data_ADA.columns = ['date', 'ADA']

#Set date as index
data_BTC.set_index('date', inplace=True)
data_ETH.set_index('date', inplace=True)
data_ADA.set_index('date', inplace=True)

#Merge data, drop NAN rows and save csv
data = data_BTC.join(data_ETH, how='outer').join(data_ADA, how='outer')
data.dropna(inplace= True)
data.to_csv(Path("Prices\Prices.csv"))
data.to_csv(Path("Prices\Prices_format_esp.csv"),sep =";",decimal=",")