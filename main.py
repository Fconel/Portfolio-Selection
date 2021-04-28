import optimization
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

#Parametros
Monedas=['BTC','ETH','LTC']
number_of_portfolios = 10000
RiskFreeRate=0

#Assets Risk/Return
RiskReturn_asset = optimization.RiskByAsset(Monedas,optimization.SimpleReturns)

#Assets Risk/Return graph
fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
ax.xaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
RiskReturn_asset.plot(x ='Risk', y='Return', kind = 'scatter',ax=ax,title='Return/Risk by asset',alpha=0.5)
for k, v in RiskReturn_asset.iterrows():
    ax.annotate(k, v)
plt.grid()

#Portfolio Risk/Retun 
MaxSharpeRatioRisk,MaxSharpeRatioReturn,portfolio_risk,portfolio_returns,portfolio_sharpe_ratio= optimization.EfficientFrontier(Monedas,'','',number_of_portfolios,RiskFreeRate,optimization.SimpleReturns)

#Portfolio Risk/Retun graph
plt.figure(figsize=(12, 8))
plt.scatter(portfolio_risk, portfolio_returns, c=portfolio_sharpe_ratio) 
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('volatility')
plt.ylabel('returns')
plt.scatter(MaxSharpeRatioRisk, MaxSharpeRatioReturn,c='red', s=50)

#Show graph
plt.show()

