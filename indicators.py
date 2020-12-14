

import robin_stocks as r
import trading_algorithms as m 
import financial as f
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import stockstats
import time 
from datetime import datetime
import csv
import talib


"""def cal_sma(data, n=9):
    return data.rolling(n).mean()

def cal_ema(data,period):
    return data.ewm(span=period, adjust=False).mean()

def cal_macd(group, nslow=26, nfast=12, signal=9):
    emaslow = group.ewm(span=nslow, adjust=False).mean()
    emafast = group.ewm(span=nfast, adjust=False).mean()
    macd = emafast - emaslow
    sig = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - sig
    #result = pd.DataFrame({ 'emaSlw':[emaslow], 'emaFast':[emafast]})
    result = pd.concat(((emafast-emaslow),sig, histogram),axis=1, sort=False)
    result.columns = ['MACD','signal','histogram']
    return result
"""
#########################
#stock tikers grabbing 
#download data 
def get_stocks():
    data = pd.DataFrame(f.requestAllStocks())
    data.to_csv('stock_list.csv',index=True)  

#read from csv 
#return tikers that in nyse and nasdaq
def clean_stocks():
    data = pd.read_csv('stock_list.csv')
    stock_exchanges = ['NYSE','Nasdaq','NYSE Arca',
                   'Nasdaq Global Select','New York Stock Exchange',
                   'NASDAQ Capital Market','NYSE American',
                   'NASDAQ Global Market','NasdaqCM','NasdaqGM','NasdaqGS']
    df = data[data['exchange'].isin(stock_exchanges)] 
    #remove funds: name contains 'Fund' 
    df = df.drop(df[df['name'].str.contains('Fund', na=False)].index)
    #check if the price can be requested 
    df1 = df.copy()
    change = []
    for index, row in df1.iterrows():
        try: 
            #result = f.getPricePercent(row['symbol'],30)
            result = f.getPriceCurrent(row['symbol'])
            print(row['symbol'],result)
            change.append(result)
        except Exception as exc:
            change.append(np.nan) 
    df1.loc[:,'close'] = change
    #remove nan rows
    df2 = df1.dropna(how='any')
    #save to cvs
    df2.to_csv('stock_list_clean1.csv',index=False)

def get_all_tickers():
    tkers = []
    data = pd.read_csv('stock_list_clean.csv')
    for index, row in data.iterrows():
        if row['price'] > 5: #get rid of penny stock
            tkers.append(row['symbol'])
    return tkers


#########################
#create binary data 
def get_binary(x):
    current_value = 0
    current_state = 0
    state = []
    for value in x:
        if value >= current_value:
            current_state = 1
        elif value < current_value:
            current_state = 0
        current_value = value 
        state.append(current_state)
    return state

def get_binary_np(x):
    current_value = 0
    current_state = 0
    state = []
    for value in x:
        if value >= current_value:
            current_state = 1
        elif value < current_value:
            current_state = 0
        current_value = value 
        state.append(current_state)
    return np.array(state)


def load_stock(tker,day):
    X = f.requestHistoryStockPriceByDay(tker,day)
    Data = pd.DataFrame(X)
    Data = pd.concat([Data['date'][::-1],Data['open'][::-1],
                      Data['high'][::-1],Data['low'][::-1],
                      Data['close'][::-1],Data['volume'][::-1],
                      Data['adjClose'][::-1]],axis=1)
    Data.columns = ['date','open','high','low','close','volume','adjClose']
    Data = Data.reset_index(drop=True) #inverse the index number
    return Data

def load_stock_from(tker,end,day):
    start = f.calDatesFrom(end,day).strftime("%Y-%m-%d")
    X = f.requestHistoryStockPrice(tker, start, end)
    Data = pd.DataFrame(X)
    Data = pd.concat([Data['date'][::-1],Data['open'][::-1],
                      Data['high'][::-1],Data['low'][::-1],
                      Data['close'][::-1],Data['volume'][::-1],
                      Data['adjClose'][::-1]],axis=1)
    Data.columns = ['date','Open','High','Low','Close','Volume','adjClose']
    Data = Data.reset_index(drop=True) #inverse the index number
    return Data

def load_stock_30min(tker):
    X = f.request30minStockPrice(tker)
    Data = pd.DataFrame(X)
    Data = pd.concat([Data['date'][::-1],Data['open'][::-1],
                      Data['high'][::-1],Data['low'][::-1],
                      Data['close'][::-1],Data['volume'][::-1]],axis=1)
    Data.columns = ['date','Open','High','Low','Close','Volume']
    Data = Data.reset_index(drop=True) #inverse the index number
    return Data

def cal_stock(data):
    stock = stockstats.StockDataFrame.retype(data)
    stock['cross_kd'] = stock['kdjk'] - stock['kdjd'] #cross kd 
    stock['macdh_b']=get_binary(stock['macdh']) #macdh binary 
    stock['kdjd_b']=get_binary(stock['kdjd']) #kdjd binary
    stock['kdjk_b']=get_binary(stock['kdjk']) #kdjk binary
    stock['cross_kd_b']=get_binary(stock['cross_kd']) #cross kd binary 
    return stock 

#kd rules:
#current D < average D
#last kd_cross < 0 and current kd_cross > 0
#current D up trend 
def kd_buy_long(stock):
    last_kd_cross = stock.iloc[-2]['cross_kd']
    curr_kd_cross = stock.iloc[-1]['cross_kd']
    curr_kdjd = stock.iloc[-1]['kdjd']
    curr_kdjd_b = stock.iloc[-1]['kdjd_b']
    kdjd_ave = stock['kdjd'].mean()
    if curr_kdjd < kdjd_ave and last_kd_cross < 0 and curr_kd_cross > 0 and curr_kdjd_b == 1: 
        return True
    else: 
        return False 

#ma rules:
#30ma up trend 
def ma_buy_long(stock):
    last_ma30 = stock['close_30_sma'].iloc[-2]
    curr_ma30 = stock['close_30_sma'].iloc[-1]
    if curr_ma30 > last_ma30:
        return True
    else:
        return False  

#ma rules:
#30ma up trend 
def ma_buy_short(stock):
    last_ma30 = stock['close_30_sma'].iloc[-2]
    curr_ma30 = stock['close_30_sma'].iloc[-1]
    if curr_ma30 > last_ma30:
        return True
    else:
        return False  

#macd rules:
#last three macdh up trend 
#last macdh > 0 
def macd_buy_long(stock):
    curr_macdh = stock.iloc[-1]['macdh']
    win = [1,1,1]
    if list(stock['macdh_b'].tail(3)) ==  win and curr_macdh > - 0.5:
        return True
    else:
        return False 

#macd rules:
#last three macdh up trend 
def macd_buy_short(stock):
    curr_macdh = stock.iloc[-1]['macdh']
    win = [1,1,1]
    if list(stock['macdh_b'].tail(3)) == win and curr_macdh > - 0.1:
        return True
    else:
        return False 

#kd rules:
#current D < average D
#last kd_cross < 0 and current kd_cross > 0
#current D up trend 
def kd_buy_short(stock):
    last_kd_cross = stock.iloc[-2]['cross_kd']
    curr_kd_cross = stock.iloc[-1]['cross_kd']
    curr_kdjd = stock.iloc[-1]['kdjd']
    curr_kdjd_b = stock.iloc[-1]['kdjd_b']
    kdjd_ave = stock['kdjd'].mean()
    
    if curr_kdjd < kdjd_ave and last_kd_cross < 0 and curr_kd_cross > 0 and curr_kdjd_b == 1: 
        print('d_ave',kdjd_ave)
        print('d',curr_kdjd)
        return True
    else: 
        return False 

#this function returns stock tikers watch list 
def algo_watch():
    watch = []
    tikers = ['AAPL','MSFT','NIO']
    for tker in get_all_tickers():
        try:
            day = 100
            data = load_stock(tker,day)
            stock = cal_stock(data)
            print(tker)
            if kd_buy_long(stock) == True and ma_buy_long(stock)==True and macd_buy_long(stock) == True:
                print('buy ',tker)
                watch.append(tker)
        except Exception as ex:
            print('error', ex)
    return watch 




#buy signal 
def buy_signal(stock):
    if kd_buy_short(stock) == True and macd_buy_short(stock) == True and ma_buy_short(stock):
        return True 
    else: 
        return False

#this function find the timing to buy 
#return true to buy and false to continue to watch
def algo_buy(tker):
    try:
        data = load_stock_30min(tker)
        stock = cal_stock(data)
        print('tkert',tker)
        print(stock[['close','kdjk','kdjd','cross_kd','macdh']].tail())
        if buy_signal(stock):
            print(tker,'is to buy')
            money = 10
            check = m.checkCap(tker,200)
            if check:
                return m.buyStock(tker,money)
    except Exception as exc:
        print('failed to track ', tker,'error:',exc)
#this is for test purpose             
def algo_buy_test(tker):
    try:
        data = load_stock_30min(tker)
        stock = cal_stock(data)
        print('tker',tker)
        print(stock[['close','kdjk','kdjd','cross_kd','macdh']].tail())
        if buy_signal(stock):
            print(tker)
            return tker
        else:
            print(tker)
    except Exception as exc:
        print('failed to track ', tker,'error:',exc)


def watch_list():
    watch = algo_watch()
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open('watch_list.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([now,watch])
    return watch 


def save_to_csv(tker,day):
    data = load_stock(tker,day)
    data.to_csv(tker+'.csv',index=True)

    
def up_trend(data, window=1):
    b = get_binary(data)
    #print(b)
    w = []
    for i in range(window):
        w.append(1)
    if list(b[-window:]) == w:
        return True
    else:
        return False

def down_trend(data, window=1):
    b = get_binary_np(data)
    w = []
    for i in range(window):
        w.append(0)
    if list(b[-window:]) == w:
        return True
    else:
        return False

#data = [1,1,1,1]
#dt = pd.DataFrame(data)
#up_trend(dt,window=1)