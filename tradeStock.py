import robin_stocks as r
import trading_algorithms as m
import financial as f
import pandas as pd
import matplotlib.pyplot as plt
import time 
import threading

def login():
    account = input('Enter account:\n')
    password = input('Enter password:\n')
    r.login(account,password)


#get all hodling stocks with holding values 
def getMyStockListwithPrice():
    stock_list = {}
    my_stocks_info = r.build_holdings()
    #print(my_stocks_info)
    for key in my_stocks_info.keys():
        stock_list[key] = float(my_stocks_info[key]['price'])
    return stock_list

def getMyStockList():
    stock_list = []
    my_stock_info = r.build_holdings()
    for key in my_stock_info.keys():
        stock_list.append(key)
    return stock_list

def getMyStockHoldings():
    my_stock_info = r.build_holdings()
    pd.set_option('display.max_columns',500)
    pd.set_option('display.width',1000)
    p = pd.DataFrame.from_dict(my_stock_info, orient='index')
    return p

def getTotalEquity():
    holdings = getMyStockHoldings()
    total = 0
    for e in holdings['equity']:
        total += float(e)
    return float(total)

def getTotalEquityChange(holdings):
    total = 0
    for e in holdings['equity_change']:
        total += float(e)
    return total

def getEquity(tker, holdings):
    return holdings['equity'].loc[tker]

def getEquity(tker):
    try:
        holdings = getMyStockHoldings()
        return float(holdings['equity'].loc[tker])
    except Exception as exc:
        print('failed to request getEquity(), error: ', exc)

def getEquityChange(tker):
    holdings = getMyStockHoldings()
    return float(holdings['percent_change'].loc[tker]) 

def requestInvestmentProfile():
    d = r.profiles.load_account_profile()
    #pd.set_option('display.max_columns',500)
    #pd.set_option('display.width',1000)
    #return pd.DataFrame.from_dict(d, orient='index')
    return d

def getCashPortfolio():
    data = requestInvestmentProfile()
    return float(data['portfolio_cash'])
 
def getTotalInvest():
    cash = getCashPortfolio()
    equity = getTotalEquity()
    return cash + equity

def getEquityCap(tker):
    getTotalEquity() 

#cypto
def get_my_cypto_value():
    data = r.get_crypto_positions()
    #print(data)
    qt = float(data[0]['quantity'])
    return round(qt*f.get_cypto_price(),2)



if __name__ == "__main__":
    login()
    print(get_my_cypto_value())
    