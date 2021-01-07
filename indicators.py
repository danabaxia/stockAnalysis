

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
import itertools
#import talib



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
    data = pd.read_csv('stockS/stocks.csv')
    return data


#########################
#create binary data 
def get_binary(x):
    current_value = 0.1
    current_state = 0
    state = []
    i = 0
    for value in x:
        trend = value - current_value
        if trend > 0:
            current_state = 1
        elif trend <= 0:
            current_state = 0
        else:
            if i == 0:
                current_state = 0
            else: 
                current_state = state[-1]
        current_value = value 
        state.append(current_state)
        i += 1
    return state

def get_binary_angle(x, angle=0.05):
    current_value = 0.1
    current_state = 0
    state = []
    i = 0
    for value in x:
        trend = (value - current_value)/(current_value+0.0001)
        #print(trend)
        if trend > angle:
            current_state = 1
        elif trend <= -angle:
            current_state = 0
        else:
            if i == 0:
                current_state = 0
            else: 
                current_state = state[-1]
        current_value = value 
        state.append(current_state)
        i += 1
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

#load stock data from start day to end day:
#fox example load_stock_from_to('NIO', '2020-04-30', '2020-08-01') 
def load_stock_from_to(tker,start,end):
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

def load_stock_15min(tker):
    X = f.request15minStockPrice(tker)
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

# up and down trends example with winodw = 1
#1, 1, 1   up 
#0, 0, 0   down 
#1, 1, 0   up to down 
#0, 0, 1   down to up  
    
def up_trend(data, window=1):
    b = get_binary(data)
    #print(b)
    w = [1]* window
    if list(b[-window:]) == w:
        return True
    else:
        return False

def down_trend(data, window=1):
    b = get_binary(data)
    w = [0]* window
    if list(b[-window:]) == w: 
        return True
    else:
        return False

def compare_bigger(a, b, window=1):
    dif_ini = a - b 
    dif = np.where(dif_ini> 0, 1, dif_ini)
    w = [1]* window
    if list(dif[-window:]) == w:
        return True
    else:
        return False

def long_line(s, m, l,window=1):
    if up_trend(s,window=window):
        if up_trend(m,window=window):
            if up_trend(l,window=window):
                if compare_bigger(s,m):
                    if compare_bigger(m,l):
                        return True
    return False

def three_line(s, m, l, window=1):
    if compare_bigger(s, m, window=window):
        if compare_bigger(m, l, window=window):
            return True
    return False

def is_peak(data, left_window=2,right_window=1):
    assert left_window >= 0, 'windown size must be >= 0'
    assert right_window >= 0, 'windown size must be >= 0'
    b = get_binary_angle(data)
    #print(b)
    w = [1]*left_window + [0]*right_window
    #print(w)
    if list(b[-(left_window+right_window):]) == w: 
        return True
    else:
        return False

def is_bottom(data, left_window=2, right_window=1):
    assert left_window >= 0, 'windown size must be >= 0'
    assert right_window >= 0, 'windown size must be >= 0'
    b = get_binary_angle(data)
    #print(b)
    w = [0]*left_window + [1]*right_window
    #print(w)
    if list(b[-(left_window+right_window):]) == w: 
        return True
    else:
        return False


def find_bottom(data, left_window=2, right_window=1):
    assert left_window >= 0, 'windown size must be >= 0'
    assert right_window >= 0, 'windown size must be >= 0'
    b = get_binary_angle(data)
    #print(b)
    w = [0]*left_window + [1]*right_window
    #print(w)
    index = []
    value = []
    for i in range(len(b)):
        d = list(b[i:left_window+right_window + i])
        #print(d)
        if d == w:
            index.append(i+1)
            value.append(data[i+1]) 
    return index,value

def find_peak(data, left_window=2, right_window=1):
    assert left_window >= 0, 'windown size must be >= 0'
    assert right_window >= 0, 'windown size must be >= 0'
    b = get_binary_angle(data)
    #print(b)
    w = [1]*left_window + [0]*right_window
    #print(w)
    index = []
    value = []
    for i in range(len(b)):
        d = list(b[i:left_window+right_window + i])
        #print(d)
        if d == w:
            index.append(i+1)
            value.append(data[i+1]) 
    return index,value

#generator combinatons 
def parameteras_generator(*arg):
    pool = {'SMA_short': range(2,14),
            'SMA_mid': range(15,29),
            'SMA_long': range(30,91),
            'rsi_low': range(2,20),
            'rsi_hi': range(65,90),
            'boll': range(5,15)}
    #check if the arguments in the pool 
    assert all(name in pool for name in arg), 'arguments contain error(s)'
    
    output = []
    for key in arg:
        output.append(pool[key])
    
    return itertools.product(*output)

def load_cypto_hour_price():
    X = f.request_CyptoPrice_hour()
    Data = pd.DataFrame(X)
    Data = pd.concat([Data['date'][::-1],Data['open'][::-1],
                      Data['high'][::-1],Data['low'][::-1],
                      Data['close'][::-1],Data['volume'][::-1]]
                      ,axis=1)
    Data.columns = ['date','open','high','low','close','volume']
    Data = Data.reset_index(drop=True) #inverse the index number
    return Data

def load_cypto_30min_price():
    X = f.request_CyptoPrice_30min()
    Data = pd.DataFrame(X)
    Data = pd.concat([Data['date'][::-1],Data['open'][::-1],
                      Data['high'][::-1],Data['low'][::-1],
                      Data['close'][::-1],Data['volume'][::-1]]
                      ,axis=1)
    Data.columns = ['date','open','high','low','close','volume']
    Data = Data.reset_index(drop=True) #inverse the index number
    return Data

def load_cypto_day_price():
    X = f.request_CyptoPrice_day()
    Data = pd.DataFrame(X)
    Data = pd.concat([Data['date'][::-1],Data['open'][::-1],
                      Data['high'][::-1],Data['low'][::-1],
                      Data['close'][::-1],Data['volume'][::-1]]
                      ,axis=1)
    Data.columns = ['date','open','high','low','close','volume']
    Data = Data.reset_index(drop=True) #inverse the index number
    return Data


if __name__ == "__main__":
    tickers = get_all_tickers()
    for tker in tickers['tiker']:
        print(tker)



