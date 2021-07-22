import pathlib
import pandas as pd
from pathlib import Path
import ssl

#Load data from WEB
def DataFromWeb(names:list) -> pd.DataFrame:
    ssl._create_default_https_context = ssl._create_unverified_context
    
    data = pd.DataFrame()

    for _ in range(len(names)):
                
        data_price = pd.read_csv(r'https://www.cryptodatadownload.com/cdd/Binance_'+names[_]+r'USDT_d.csv',header=1) #Load data from cryptodatadownload.com
        
        data_price.drop(data_price.columns.difference(['date','close']), 1, inplace=True) #Keep 'close price' and 'date' fields
        data_price.columns = ['date', names[_]]
        data_price.set_index('date', inplace=True)
        data = data.join(data_price, how='outer')
        data.dropna(inplace= True)

    return data

#Load data from CSV
def DataFromCSV(Path: pathlib.Path) -> pd.DataFrame:
            
    data = pd.read_csv(Path, index_col=0) 

    return data