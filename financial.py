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
 
#df = pd.DataFrame(requestIncome('AAPL')[:2])



def requestBalance(tker, period):
    if period == 'quarter':
        r = requests.get('https://financialmodelingprep.com/api/v3/balance-sheet-statement/' + tker + '?period=quarter&apikey=' + key)
    return r.json()

#df = pd.DataFrame(requestBalance('AAPL'))

def requestAllStocks():
    r = requests.get('https://financialmodelingprep.com/api/v3/stock/list?apikey=' + key)
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

def cal_ROS(tker,freq):
    return get_netIncome(tker,freq)/get_revenue(tker,freq)*100

def cal_currentLiabilitiesRatio(tker, freq):
    return get__totalLiabilities(tker,freq)/get_totalAsset(tker,freq)*100

def cal_currentRatio(tker, freq):
    return get_currentAsset(tker,freq)/get_totalCurrentLiabilities(tker,freq)*100

def cal_ROE(tker, freq):
    return get_netIncome(tker, freq)/get_shareHolderEquity(tker, freq)*100


#Test
print(get_currentAsset('AAPL', 'quarter'))
print(get_totalAsset('AAPL', 'quarter'))
print(get_totalCurrentLiabilities('AAPL', 'quarter'))
print(get__totalLiabilities('AAPL', 'quarter'))
print(get_shareHolderEquity('AAPL', 'quarter'))
print(cal_currentRatio('AAPL', 'quarter'))
print(cal_ROE('AAPL', 'quarter'))