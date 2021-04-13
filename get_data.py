import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#Load all data
def get_data(names):
    
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