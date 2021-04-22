import pathlib
import pandas as pd
from pathlib import Path
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#Load data from WEB OR CSV
def DataFromWeb(names:list) -> pd.DataFrame:
    
    data = pd.DataFrame()

    for _ in range(len(names)):
        
        #Load data from cryptodatadownload.com
        data_price = pd.read_csv(r'https://www.cryptodatadownload.com/cdd/Binance_'+names[_]+r'USDT_d.csv',header=1) 
        
        #Keep close price anda date 
        data_price.drop(data_price.columns.difference(['date','close']), 1, inplace=True)
        
        #Rename colums
        data_price.columns = ['date', names[_]]

        #Set date as index
        data_price.set_index('date', inplace=True)

        #Merge data, drop NAN rows and save csv
        data = data.join(data_price, how='outer')
        data.dropna(inplace= True)

    return data

def DataFromCSV(Path: pathlib.Path) -> pd.DataFrame:
            
    data = pd.read_csv(Path, index_col=0) 

    return data