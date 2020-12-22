"""
========================
Stock financials Module
Version 1.0
========================

Author: Jacob Han

"""
import plotly.graph_objects as go
import requests
import pandas as pd
import signal
from datetime import datetime, timedelta, date
import math
import csv
import re


key = input('Enter the key:\n')

def round_half_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier - 0.5) / multiplier

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
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/' + tker + '?apikey=' + key)
        return r.json()['historical']
    except Exception as exc:
        print('error: ',exc)

def requestHistoryStockPrice_s(tker):
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/' + tker + '?serietype=line&apikey=' + key)
        return r.json()['historical']
    except Exception as exc:
        print('error: ',exc)

def requestHistoryStockPriceByDay(tker,day):
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/' + tker + '?timeseries=' + str(day) + '&apikey=' + key)
        return r.json()['historical']
    except Exception as exc:
        print('error:', exc)

def requestHistoryStockPrice(tker, start, end):
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/' + tker +'?from=' + start + '&to=' + end + '&apikey=' + key)
        return r.json()['historical']
    except Exception as exc:
        print('error: ',exc)

def requestCurrentPrice(tker):
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/quote-short/' + tker + '?apikey=' + key)
        return r.json()
    except Exception as exc:
        print('requestCurrentPrice error: ', exc)

def request15minStockPrice(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/15min/' + tker + '?apikey=' + key)
    return r.json()

def request30minStockPrice(tker):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/30min/' + tker + '?apikey=' + key)
    return r.json()

def request1hourStockPrice(tker):
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/1hour/' + tker + '?apikey=' + key)
        return r.json()
    except Exception as exc:
        print('error: ', exc)    

def requestMarketOpen():
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/market-hours?apikey='+key)
        data = r.json()
        return data
    except Exception as exc:
        print('error ', exc)


def isMarketOpen():
    try:
        data = requestMarketOpen()
        return data[0]['isTheStockMarketOpen']
    except Exception as exc:
        print('error',exc)
        return False

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
    return round_half_down((closePrice - lowPirce)/lowPirce*100,2)
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

def calDatesFrom(end, day):
    date_obj = datetime.strptime(end, '%Y-%m-%d')
    end_date = date_obj.date()
    
    return (end_date - timedelta(day))

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
    return round_half_down(total/len(prices),2)

def getPriceAverageFrom(tker, end, day):
    #end_date = date.today().strftime("%Y-%m-%d")
    start = calDatesFrom(end,day).strftime("%Y-%m-%d")
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
    return round_half_down(total/len(prices),2)

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
    return round_half_down(total/i)

def getPriceAverageByDay(tker,day):
    try:
        history = requestHistoryStockPriceByDay(tker,day)
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
        return round_half_down(total/i)  
    except Exception as exc:
        print('getPriceAverageByDay error:', exc)    

def getPriceCurrent(tker):
    data = requestCurrentPrice(tker)
    return data[0]['price']

def getPriceYesterday(tker):
    return requestHistoryStockPrice(tker)[0]['close']

def getPricePercent(tker, day): 
    return round_half_down((getPriceCurrent(tker) - getPriceAverage(tker,day))/getPriceAverage(tker,day)*100,2)

# (current price - yesterday price)/yesterday price 
def getTodayReturn(tker):
    current = getPriceCurrent(tker)
    yesterday = getPriceYesterday(tker)
    return float("{:.2f}".format((float(current) - float(yesterday))/float(yesterday)*100))

#historical volatility 
#===============================


#Stock data
#==============================
def getStockListToCVS():
    data = requestAllStocks()
    print(len(data))
    stock_list = open('stock_list.csv','w')
    csv_writer = csv.writer(stock_list)
    count = 0

    for element in data:
        if count == 0:
            header = element.keys()
            csv_writer.writerow(header)
        csv_writer.writerow(element.values())
        count+=1
    stock_list.close()

def saveListToCSV(data,header=None,isHeader=False):
    f = open('good_candidates_new.csv','w')
    csv_writer = csv.writer(f)
    if isHeader:
        csv_writer.writerow(header)
    for element in data:
        csv_writer.writerow(element)
    f.close()

def readStockFromCSV(file):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def requestStockRate(tker):
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/rating/' + tker + '?apikey=' + key)
        return r.json()[0]['ratingScore']
    except Exception as exc:
        print('request stock rate error:', exc)


def read_labels(file):
    t = readStockFromCSV(file)
    return [item for sublist in t for item in sublist]  #faltten the list of lists

def read_sectors(file):
    t = readStockFromCSV(file)
    return [item for sublist in t for item in sublist]  #faltten the list of lists

def read_stocks(file):
    return pd.read_csv(file)

if __name__ == "__main__":
    #print(read_labels('stocks/labels.csv'))
    #print(read_sectors('stocks/sectors.csv'))
    df = read_stocks('stocks/stocks.csv')
    df['label'] = df['label'].str.findall(r'#(\w+)') #parse hashtag to list of tags 
    #print(df['label'].str.findall(r'#(\w+)'))
    print(df['label'])
    labels = df['label'].explode()
    indexes = labels[labels=='banking'].index
    print(df['tiker'].iloc[indexes])
    print(list(df['tiker']))
    
    
