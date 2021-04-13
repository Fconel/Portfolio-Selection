import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pandas.io.formats.format import return_docstring
from get_data import get_data

#inputs
Monedas=['BTC','ETH','LTC']
number_of_portfolios = 10000
RiskFreeRate=0

#Load  data
Data = get_data(Monedas)
#Data = pd.read_csv(Path("Prices\Prices.csv"), index_col=0) 
Data.sort_index(ascending=False, inplace=True)

# calculate returns 
Returns = Data.pct_change(-1)
LogReturns =  np.log(1 + Data.pct_change(-1))
Returns.dropna(inplace= True)

# Annualized Risk and Annualized mean returns by asset
#-------------------------------------------------------------------------------------
risk_asset = (Returns.std() * np.sqrt(252)).to_frame()
risk_asset.columns = ['Risk']

mean_returns_asset = (Returns.mean()*252).to_frame()
mean_returns_asset.columns = ['Return']

RiskReturn_asset = risk_asset.join(mean_returns_asset, how='outer')
#--------------------------------------------------------------------------------------------------------

#Portfolio Risk/return 

portfolio_returns = []
portfolio_risk = []
portfolio_sharpe_ratio = []
portfolio_weights = []

#weights arrays
for portfolio in range (number_of_portfolios):

    #Random Weight
    weights = np.random.random_sample(len(Monedas))
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
  
#convert to arrays
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


#Graphs

#Risk/Retun portfolio assets
fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
ax.xaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
RiskReturn_asset.plot(x ='Risk', y='Return', kind = 'scatter',ax=ax,title='Return/Risk by asset',alpha=0.5)
for k, v in RiskReturn_asset.iterrows():
    ax.annotate(k, v)
plt.grid()

#Risk/Retun portfolio
plt.figure(figsize=(12, 8))
plt.scatter(portfolio_risk, portfolio_returns, c=portfolio_sharpe_ratio) 
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('volatility')
plt.ylabel('returns')
plt.scatter(MaxSharpeRatioRisk, MaxSharpeRatioReturn,c='red', s=50)
plt.show()