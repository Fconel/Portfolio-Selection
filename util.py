import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import ssl

def pricesDataFromWeb(symbol:list,sourceURL:str='https://www.cryptodatadownload.com/cdd/',
exchange:str='Binance',pair:str='USDT',periodicity:str='d',number_observations:int=360) -> pd.DataFrame:
    """
    Check https://www.cryptodatadownload.com/data/ for avaible exchanges ,periodicity, and pairs
   
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    data = pd.DataFrame()

    for _ in range(len(symbol)):
                
        data_price = pd.read_csv(sourceURL+exchange+'_'+symbol[_]+pair+'_'+periodicity+'.csv',header=1) 
        data_price = data_price[['date','close']]
        data_price.columns = ['date', symbol[_]]
        data_price.set_index('date', inplace=True)

        data = data.join(data_price, how='outer')
        
    data.dropna(inplace= True)
    data.sort_index(ascending=False, inplace=True)

    return data.head(number_observations)

def rate_of_return(prices: pd.DataFrame,LogReturn=False) -> pd.DataFrame:

    if LogReturn:
        return np.log(1 + prices.pct_change(-1)).dropna()
    else:
        return prices.pct_change(-1).dropna()

def RiskByAsset(Returns:pd.DataFrame)-> pd.DataFrame:

    risk_asset = (Returns.std() * np.sqrt(252)).to_frame()
    risk_asset.columns = ['Risk']

    mean_returns_asset = (Returns.mean()*252).to_frame()
    mean_returns_asset.columns = ['Return']

    return risk_asset.join(mean_returns_asset, how='outer')

def EfficientFrontier(Returns,N_simulations,RiskFreeRate,save_simulatios=True):
    
    portfolio_risk_return=[]
    portfolio_metrics={'portfolio_returns': 0, 'portfolio_risk': 0, 'portfolio_sharpe_ratio': -99,'portfolio_weights':[],'portfolio_risk_return':[]}

    for portfolio in range (N_simulations):
        
        #Random Weight
        weights = np.random.random_sample(len(Returns.columns))
        weights = weights / np.sum(weights)
        
        #Calculate Return
        portfolio_mean_return= sum(Returns.mean()*weights)*252
        
        #Calculate Risk
        cov_matrix = (Returns.cov())*252
        port_variance = (weights.T).dot(cov_matrix.dot(weights))
        port_standard_deviation = np.sqrt(port_variance)
     
        #Calculate Sharpe Ratio
        sharpe_ratio = ((portfolio_mean_return- RiskFreeRate)/port_standard_deviation)
        
        if save_simulatios:
            portfolio_risk_return.append([portfolio_mean_return,port_standard_deviation,sharpe_ratio])
        
        if sharpe_ratio>portfolio_metrics['portfolio_sharpe_ratio']:
            
            portfolio_metrics.update({'portfolio_returns':portfolio_mean_return})
            portfolio_metrics.update({'portfolio_risk':port_standard_deviation})
            portfolio_metrics.update({'portfolio_sharpe_ratio':sharpe_ratio})
            portfolio_metrics.update({'portfolio_weights':weights})

    portfolio_metrics.update({'portfolio_risk_return':portfolio_risk_return})
    
    return portfolio_metrics

class graficos():

    def Risk_Retun(RiskReturn_asset):
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
        ax.xaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
        RiskReturn_asset.plot(x ='Risk', y='Return', kind = 'scatter',ax=ax,title='Return/Risk by asset',alpha=0.5)
        for k, v in RiskReturn_asset.iterrows():
            ax.annotate(k, v)
        plt.grid()
        plt.show()

    def portfolio_simulation(data):

        data_grafico=data['portfolio_risk_return']

        returns = [item[0] for item in data_grafico]
        risk = [item[1] for item in data_grafico]
        sharpe_ratio = [item[2] for item in data_grafico]
       
        plt.scatter(risk, returns, c=sharpe_ratio) 
        plt.colorbar(label='Sharpe Ratio')
        plt.xlabel('Volatility')
        plt.ylabel('Returns')
        plt.scatter(data['portfolio_risk'], data['portfolio_returns'],c='red', s=50)

        plt.show()