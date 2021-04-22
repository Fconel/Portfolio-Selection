import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pandas.io.formats.format import return_docstring
import get_data
from pathlib import Path

def SimpleReturns(Data: pd.DataFrame) -> pd.DataFrame:
    return Data.pct_change(-1)

def LogReturns(Data: pd.DataFrame) -> pd.DataFrame:
    return np.log(1 + Data.pct_change(-1))

def retorno(prices: pd.DataFrame,arg) -> pd.DataFrame:
    return arg(prices)

def RiskByAsset(tickers,ReturnType):

    prices = get_data.DataFromWeb(tickers)
    prices.sort_index(ascending=False, inplace=True)

    Returns = retorno(prices,ReturnType)

    risk_asset = (Returns.std() * np.sqrt(252)).to_frame()
    risk_asset.columns = ['Risk']

    mean_returns_asset = (Returns.mean()*252).to_frame()
    mean_returns_asset.columns = ['Return']

    RiskReturn_asset = risk_asset.join(mean_returns_asset, how='outer')

    return RiskReturn_asset

def EfficientFrontier(tickers,start_date,end_date,N_simulations,RiskFreeRate,ReturnType):

    prices = get_data.DataFromWeb(tickers)
    prices.sort_index(ascending=False, inplace=True)

    Returns = retorno(prices,ReturnType)
                
    #Portfolio Risk/return 
    portfolio_returns = []
    portfolio_risk = []
    portfolio_sharpe_ratio = []
    portfolio_weights = []

    #weights arrays
    for portfolio in range (N_simulations):

        #Random Weight
        weights = np.random.random_sample(len(tickers))
        weights = weights / np.sum(weights)
        portfolio_weights.append(weights)

        #Calculate Return
        portfolio_mean_return= sum(Returns.mean()*weights)*252
        portfolio_returns.append(portfolio_mean_return)
        
        #Calculate Risk
        cov_matrix = (Returns.cov())*252
        port_variance = (weights.T).dot(cov_matrix.dot(weights))
        port_standard_deviation = np.sqrt(port_variance)
        portfolio_risk.append(port_standard_deviation)
        
        #Calculate Sharpe Ratio
        sharpe_ratio = ((portfolio_mean_return- RiskFreeRate)/port_standard_deviation)
        portfolio_sharpe_ratio.append(sharpe_ratio)
    
    #to arrays
    portfolio_risk = np.array(portfolio_risk)
    portfolio_returns = np.array(portfolio_returns)
    sharpe_ratio_port = np.array(portfolio_sharpe_ratio)
    porfolio_metrics = [portfolio_returns,portfolio_risk,sharpe_ratio_port, portfolio_weights] 

    #from Python list we create a Pandas DataFrame
    portfolio_dfs = pd.DataFrame(porfolio_metrics)
    portfolio_dfs = portfolio_dfs.T

    #Rename the columns:
    portfolio_dfs.columns = ['Port Returns','Port Risk','Sharpe Ratio','Portfolio Weights']

    Max_risk = portfolio_dfs['Port Risk'].max()
    min_risk = portfolio_dfs['Port Risk'].min()

    #range_of_risk = range(min_risk,Max_risk,)

    #convert from object to float the first three columns.
    for col in ['Port Returns', 'Port Risk', 'Sharpe Ratio']:
        portfolio_dfs[col] = portfolio_dfs[col].astype(float)


    #portfolio_dfs.to_csv(Path("output.csv"))
    index_max_SharpeRatio=portfolio_dfs['Sharpe Ratio'].argmax()
    MaxSharpeRatioReturn=portfolio_dfs.iloc[index_max_SharpeRatio,0]
    MaxSharpeRatioRisk=portfolio_dfs.iloc[index_max_SharpeRatio,1]

    print("Max Sharpe ratio is: {}".format(portfolio_dfs['Sharpe Ratio'].max()))
    print("Return of Max Sharpe ratio portfolio: {}".format(MaxSharpeRatioReturn))
    print("Risk of Max Sharpe ratio portfolio: {}".format(MaxSharpeRatioRisk))
    print("Max Sharpe ratio: {}".format(portfolio_dfs.iloc[index_max_SharpeRatio,2]))
    print("Max Sharpe weight: {}".format(portfolio_dfs.iloc[index_max_SharpeRatio,3]))

    return MaxSharpeRatioRisk,MaxSharpeRatioReturn,portfolio_risk,portfolio_returns,portfolio_sharpe_ratio


 