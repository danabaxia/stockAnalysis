"""
========================
Stock financials Module
Version 1.0
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
import signal
from datetime import datetime, timedelta, date

key = '3711ff28a46fd9f7cbc915ca70a67b30'

def requestIncome(tker,period):
    if period == 'quarter':
        r = requests.get('https://financialmodelingprep.com/api/v3/income-statement/' + tker + '?period=quarter&apikey=' + key)
    return r.json()

def requestBalance(tker, period):
    if period == 'quarter':
        r = requests.get('https://financialmodelingprep.com/api/v3/balance-sheet-statement/' + tker + '?period=quarter&apikey=' + key)
    return r.json()

def requestRatio(tker, period):
    if period == 'quarter':
        r = requests.get('https://financialmodelingprep.com/api/v3/ratios/' + tker + '?period=quarter&apikey=' +key)
    return r.json()

def requestProfile(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/profile/' + tker + '?apikey=' + key)
    return r.json()

#====================================================================
#Get company financial data
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

#====================================================================
#Market profle
def requestAllStocks():
    r = requests.get('https://financialmodelingprep.com/api/v3/stock/list?apikey=' + key)
    return r.json()

def requestSectorPerformance():
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-sectors-performance?apikey=' + key)
    return r.json()
#sectors:
#  "utilitiesChangesPercentage" 
#  "basicMaterialsChangesPercentage" 
#  "communicationServicesChangesPercentage" 
#  "conglomeratesChangesPercentage" 
#  "consumerCyclicalChangesPercentage" 
#  "consumerDefensiveChangesPercentage"
#  "energyChangesPercentage" 
#  "financialChangesPercentage" 
#  "financialServicesChangesPercentage" 
#  "healthcareChangesPercentage" 
#  "industrialGoodsChangesPercentage" 
#  "industrialsChangesPercentage" 
#  "realEstateChangesPercentage" 
#  "servicesChangesPercentage" 
#  "technologyChangesPercentage"
def getSectorPerformanceAveragePercent(sector, day):  # day smaller than 6 months
    sectors = ['utilitiesChangesPercentage',
               'basicMaterialsChangesPercentage',
               'communicationServicesChangesPercentage',
               'conglomeratesChangesPercentage',
               'consumerCyclicalChangesPercentage',
               'consumerDefensiveChangesPercentage',
               'energyChangesPercentage',
               'financialChangesPercentage',
               'financialServicesChangesPercentage',
               'healthcareChangesPercentage',
               'industrialGoodsChangesPercentage',
               'industrialsChangesPercentage',
               'realEstateChangesPercentage',
               'servicesChangesPercentage',
               'technologyChangesPercentage']
    #find out the sector based on key words
    for item in sectors:
        if item.find(sector) != -1:
            sector = item
            break
    #print('sector is: '+sector)
    perform = []
    history = requestSectorPerformance()
    for item in history:
       perform.append(item[sector])
    i = 0
    total = 0
    while i<day:
        total += perform[i]
        i += 1
    return total/day

def getSectorsPerformance(day):
    sectors = ['utilitiesChangesPercentage',
               'basicMaterialsChangesPercentage',
               'communicationServicesChangesPercentage',
               'conglomeratesChangesPercentage',
               'consumerCyclicalChangesPercentage',
               'consumerDefensiveChangesPercentage',
               'energyChangesPercentage',
               'financialChangesPercentage',
               'financialServicesChangesPercentage',
               'healthcareChangesPercentage',
               'industrialGoodsChangesPercentage',
               'industrialsChangesPercentage',
               'realEstateChangesPercentage',
               'servicesChangesPercentage',
               'technologyChangesPercentage']   
    history = requestSectorPerformance()
    max = -999
    bestsector = sectors[0]
    for label in sectors:
        perform = []
        for item in history:
            perform.append(item[label])
        i, total = 0,0
        while i < day:
            total += perform[i]
            i += 1
        print(label + ' : ' + str(total/day))
        if max < total/day:
            max = total/day
            bestsector = label
    return bestsector,max

#=============================================================
#requerst historical and current stock price
"""
def requestHistoryStockPrice(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/' + tker + '?apikey=' + key)
    return r.json()['historical']
"""
def requestHistoryStockPrice_n(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/' + tker + '?apikey=' + key)
    return r.json()['historical']

def requestHistoryStockPrice(tker, start, end):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/' + tker +'?from=' + start + '&to=' + end + '&apikey=' + key)
    return r.json()['historical']

def requestCurrentPrice(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/quote-short/' + tker + '?apikey=' + key)
    return r.json()

def request30minStockPrice(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/30min/' + tker + '?apikey=' + key)
    return r.json()

def request1hourStockPrice(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/1hour/' + tker + '?apikey=' + key)
    return r.json()    

def requestMarketOpen():
    r = requests.get('https://financialmodelingprep.com/api/v3/market-hours?apikey='+key)
    data = r.json()
    return data

def isMarketOpen():
    data = requestMarketOpen()
    return data[0]['isTheStockMarketOpen']

def get30minStockPriceChange(tker):
    data = request30minStockPrice(tker)[0]
    openPrice = data['open']
    closePrice = data['close']
    return (closePrice - openPrice)/openPrice*100

def get1hourStockPriceChange(tker):
    data = request1hourStockPrice(tker)[0]
    openPrice = data['open']
    lowPirce = data['low']
    closePrice = data['close']
    return (closePrice - lowPirce)/lowPirce*100
"""
def getPriceAverage(tker, day):
    history = requestHistoryStockPrice(tker)
    #create a list of all prices 
    prices = []
    for item in history: 
        prices.append(float(item['close']))
    #CAL everage
    total = 0
    i = 0
    while i < day:
        total += prices[i]
        i+=1
    #return "{:.2f}".format(total/day)
    return total/day
"""
def calDates(day):
    return date.today() - timedelta(day)

def getPriceAverage(tker, day):
    end = date.today().strftime("%Y-%m-%d")
    start = calDates(day).strftime("%Y-%m-%d")
    #print('end', end)
    #print('start',start)
    history = requestHistoryStockPrice(tker, start, end)
    #print(history)
    #create a list of all prices 
    prices = []
    for item in history: 
        #print(type(item['close']))
        prices.append(item['close'])
    #CAL everage
    #print('prices', prices)
    #print('len',len(prices))
    total = 0
    i = 0
    while i < len(prices):
        total += prices[i]
        i+=1
    #return "{:.2f}".format(total/day)
    return total/len(prices)

def getPriceAverage_n(tker, day):
    history = requestHistoryStockPrice_n(tker)
    #create a list of all prices 
    prices = []
    for item in history: 
        #print(type(item['close']))
        prices.append(item['close'])
    #CAL everage
    total = 0
    i = 0
    while i < day:
        total += prices[i]
        i+=1
    return "{:.2f}".format(total/day)
    

def getPriceCurrent(tker):
    data = requestCurrentPrice(tker)
    return data[0]['price']

def getPriceYesterday(tker):
    return requestHistoryStockPrice(tker)[0]['close']

def getPricePercent(tker, day): 
    return "{:.2f}".format((getPriceCurrent(tker) - getPriceAverage(tker,day))/getPriceAverage(tker,day)*100)

# (current price - yesterday price)/yesterday price 
def getTodayReturn(tker):
    current = getPriceCurrent(tker)
    yesterday = getPriceYesterday(tker)
    return float("{:.2f}".format((float(current) - float(yesterday))/float(yesterday)*100))

#historical volatility 
#===============================



