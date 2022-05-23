from util import RiskByAsset,EfficientFrontier,graficos,pricesDataFromWeb,rate_of_return

def main():
    #Params
    tickers=['BTC','ETH','LTC']
    number_of_simulations = 10000
    RiskFreeRate=0

    #Get prices and calc return
    prices = pricesDataFromWeb(tickers,number_observations=720)
    Returns = rate_of_return(prices,LogReturn=True)

    #Efficient portfolio calc
    RiskReturn_asset = RiskByAsset(Returns)
    EfficientPortfolio=EfficientFrontier(Returns,number_of_simulations,RiskFreeRate)

    #Graphs
    graficos.Risk_Retun(RiskReturn_asset)
    graficos.portfolio_simulation(EfficientPortfolio)
    
if __name__ == '__main__':
    main()
    

