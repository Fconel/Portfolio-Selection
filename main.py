from util import risk_by_asset,efficient_frontier,graphs,web_prices,rate_of_return

def main():
    #Params
    TICKERS=['BTC','ETH','LTC']
    NUMBER_OF_SIMULATIONS = 10000
    RISK_FREE_RATE=0

    #Get prices and calc return
    prices = web_prices(TICKERS,number_observations=720)
    returns = rate_of_return(prices,LogReturn=True)

    #Efficient portfolio calc
    risk_return_by_asset = risk_by_asset(returns)
    efficient_portfolio=efficient_frontier(returns,NUMBER_OF_SIMULATIONS,RISK_FREE_RATE)

    #Graphs
    graphs.risk_retun(risk_return_by_asset)
    graphs.portfolio_simulation(efficient_portfolio)
    
if __name__ == '__main__':
    main()
    

