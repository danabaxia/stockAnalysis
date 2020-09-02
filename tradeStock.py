import robin_stocks as r
import trading_algorithms as m
import financial as f
import pandas as pd
import matplotlib.pyplot as plt
import time 
import signal 

#get all hodling stocks with holding values 
def getMyStockList():
    stock_list = {}
    my_stocks_info = r.build_holdings()
    print(my_stocks_info)
    for key in my_stocks_info.keys():
        stock_list[key] = float(my_stocks_info[key]['price'])
    return stock_list

def getMyStockHoldings():
    my_stock_info = r.build_holdings()
    pd.set_option('display.max_columns',500)
    pd.set_option('display.width',1000)
    p = pd.DataFrame.from_dict(my_stock_info, orient='index')
    return p

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

def getTotalEquity(holdings):
    total = 0
    for e in holdings['equity']:
        total += float(e)
    return total

def getTotalEquityChange(holdings):
    total = 0
    for e in holdings['equity_change']:
        total += float(e)
    return total

def requestInvestmentProfile():
    d = r.profiles.load_account_profile()
    #pd.set_option('display.max_columns',500)
    #pd.set_option('display.width',1000)
    #return pd.DataFrame.from_dict(d, orient='index')
    return d

def getCashPortfolio(investment):
    return investment['portfolio_cash']
"""
def getCryptoPos():
    d = r.crypto.get_crypto_positions()[0]['cost_bases']
    #pd.set_option('display.max_columns',500)
    #pd.set_option('display.width',1000)
    #d = pd.DataFrame(d)
    print(type(d))
    return d
"""    
def getTotalInvestment():
    return (float(getTotalEquity(getMyStockHoldings())) + float(getCashPortfolio(requestInvestmentProfile())))

r.login('danabaxia@gmail.com','Hjb1314!@#$')

###read all the holdings
print(getTotalEquity(getMyStockHoldings()))
print(getCashPortfolio(requestInvestmentProfile()))
print(getTotalInvestment())



"""

#=================================================================
###mian function start from here with ^ + C as interruption å
signal.signal(signal.SIGINT, keyboardInterruptHandler)
while True:
    for ticker in my_stocks_list.keys():
        price = r.stocks.get_latest_price(ticker)
        print(ticker, float(price[0]))
        #m.in_and_out(ticker, float(my_stocks_list[ticker]), float(price[0]), 0.03, 1)
    pass
"""