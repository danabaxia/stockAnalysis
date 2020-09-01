"""
========================
Stock financials Module
Version 0.1
========================

Author: Jacob H.

List of Included Functions:
1)get_financial_stmts(frequency, statement_type)
  - frequency can be either 'annual' or 'quarter'
  - statement can be 'income', 'balance'

"""
import plotly.graph_objects as go
import requests
import pandas as pd

key = '3711ff28a46fd9f7cbc915ca70a67b30'

def requestIncome(tker,period):
    if period == 'quarter':
        r = requests.get('https://financialmodelingprep.com/api/v3/income-statement/' + tker + '?period=quarter&apikey=' + key)
    return r.json()

def requestBalance(tker, period):
    if period == 'quarter':
        r = requests.get('https://financialmodelingprep.com/api/v3/balance-sheet-statement/' + tker + '?period=quarter&apikey=' + key)
    return r.json()

def requestAllStocks():
    r = requests.get('https://financialmodelingprep.com/api/v3/stock/list?apikey=' + key)
    return r.json()

def requestRatio(tker, period):
    if period == 'quarter':
        r = requests.get('https://financialmodelingprep.com/api/v3/ratios/' + tker + '?period=quarter&apikey=' +key)
    return r.json()

def requestProfile(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/profile/' + tker + '?apikey=' + key)
    return r.json()

def get_revenue(tker, freq):
    return pd.DataFrame(requestIncome(tker, freq))['revenue'].loc[0]

def get_netIncome(tker, freq):
    return pd.DataFrame(requestIncome(tker, freq))['netIncome'].loc[0]

def get_currentAsset(tker, freq):
    return pd.DataFrame(requestBalance(tker, freq))['totalCurrentAssets'].loc[0]

def get_totalAsset(tker, freq):
    return pd.DataFrame(requestBalance(tker, freq))['totalAssets'].loc[0]

def get_totalCurrentLiabilities(tker, freq):
    return pd.DataFrame(requestBalance(tker, freq))['totalCurrentLiabilities'].loc[0]

def get__totalLiabilities(tker, freq):
    return pd.DataFrame(requestBalance(tker, freq))['totalLiabilities'].loc[0]

def get_shareHolderEquity(tker, freq):
    return pd.DataFrame(requestBalance(tker, freq))['totalStockholdersEquity'].loc[0]

#====================================================================================
#company financials ratios

def get_currentRatio(tker, freq):
    return pd.DataFrame(requestRatio(tker,freq))['currentRatio'].loc[0]

def get_debtEquityRatio(tker, freq):
    return pd.DataFrame(requestRatio(tker,freq))['debtEquityRatio'].loc[0]

def get_returnOnEquity(tker,freq):
    return pd.DataFrame(requestRatio(tker,freq))['returnOnEquity'].loc[0]

#also called operating profit margin
def get_ROS(tker,freq):
    return pd.DataFrame(requestRatio(tker,freq))['operatingProfitMargin'].loc[0]

def get_currentLiabilitiesRatio(tker, freq):
    return get_totalCurrentLiabilities(tker,freq)/get_currentAsset(tker,freq)

def get_debtRatio(tker, freq):
    return pd.DataFrame(requestRatio(tker,freq))['debtRatio'].loc[0]

#====================================================================
#stock profile functions
def get_profileIndustry(tker):
    return pd.DataFrame(requestProfile(tker))['industry'].loc[0]

def get_profileSector(tker):
    return pd.DataFrame(requestProfile(tker))['sector'].loc[0]

def get_profileFiftytwoWeeksRange(tker):
    return pd.DataFrame(requestProfile(tker))['range'].loc[0]

"""
#stocks sorting
def get_stockList(): 
    df = pd.DataFrame(requestAllStocks())
    #iterate all stocks
    for ind in df.index:
        stock = df['symbol'][ind]
        #print(stock, get_profileIndustry(stock))
   



#print(get_stockList())    
"""
#=============================================================
#requerst historical stock price
def requestHistoryStockPrice(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/' + tker + '?apikey=' + key)
    return r.json()['historical']

def getPriceAverage(tker, day):
    history = requestHistoryStockPrice(tker)
    #create a list of all prices 
    prices = []
    for item in history: 
        prices.append(item['close'])
    #CAL everage
    total = 0
    i = 0
    while i < day:
        total += prices[i]
        i+=1
    return total/day


#===============================
print(getPriceAverage('AAPL',10))