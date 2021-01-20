import indicators as ind
import financial as f 
import stockstats
from back_testing import BackTesting, ForwardTesting
from Method_boll import BOLL
from Method_MACD import MACD
from Method_SMA import SMA
import matplotlib.pyplot as plt
import time 
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import talib 


#algo:
#BOLL UP and boll_band bottom -> buy
#boll up and boll_band peak -> sell
#boll down and boll_band bottom -> sell
#boll down and boll_band peak -> buy 
class method_test_boll:
    def __init__(self, tker, feed, timeFrame=200):
        self.feed = feed
        self.tker = tker
        self.timeFrame = timeFrame
        self.buy_price = 0
        self.stock = self.calculate_stock()
        
    def calculate_stock(self):
        stock = stockstats.StockDataFrame.retype(self.feed)
        stock['rsi_14']
        stock['macdh']
        stock = BOLL(20, stock).stock
        print(stock[['macdh','close']].tail(10))
        return stock.tail(self.timeFrame)
    
    #return 1 long 0 hold -1 sell
    def position(self, stock=None):
        if stock is None:
            stock = self.stock
        return 1

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        if stock['boll_ub'].iloc[-2] > stock['close'].iloc[-2]:
            if stock['boll_ub'].iloc[-1] < stock['close'].iloc[-1] and stock['rsi_14'].iloc[-1] <  80: 
                self.buy_price = stock['close'].iloc[-1] 
                result = [False, f.get_cypto_price(), 1, stock.index[-1]] # self.long. stop loss price, buy share,time
                return result
        elif stock['macdh'].iloc[-2] < 0 and stock['macdh'].iloc[-1] > 0: #macd cross 
                self.buy_price = stock['close'].iloc[-1] 
                result = [False, f.get_cypto_price(), 1, stock.index[-1]] # self.long. stop loss price, buy share,time
                return result            
        else:
            return None

    def sell(self, stock=None):
        if stock is None:
            stock = self.stock
        if stock['close'].iloc[-2] > stock['boll'].iloc[-2]: #boll mind band break 
            if stock['close'].iloc[-1] < stock['boll'].iloc[-1]: 
                return [True, f.get_cypto_price(), 1, stock.index[-1]] # self.long , None, sell share, time 
        elif stock['macdh'].iloc[-2] > 0 and stock['macdh'].iloc[-1] < 0: #macdcross
            return [True, f.get_cypto_price(), 1, stock.index[-1]] # self.long , None, sell share, time 
        else:
            return None

    def get_stock(self):
        return self.stock[['close','boll','boll_ub','rsi_14']]


#algo: three sma line
#sma10 >  sma20 > sma30  buy
#sma10 < sma20 sell  
class method_test_3SMA:
    def __init__(self, tker, feed, short_, mid_, long_, timeFrame=200):
        self.feed = feed
        self.tker = tker
        self.short = short_ 
        self.mid = mid_
        self.long = long_ 
        self.timeFrame = timeFrame
        self.buy_price = 0
        self.stock = self.calculate_stock()
        self.sma_short = None
        self.sma_mid = None
        self.sma_long = None
        
    def calculate_stock(self):
        stock = stockstats.StockDataFrame.retype(self.feed)
        self.sma_short = stock['close_'+str(self.short)+'_sma']
        self.sma_mid = stock['close_'+str(self.mid)+'_sma']
        self.sma_long = stock['close_'+str(self.long)+'_sma']
        stock = MACD(self.tker, 12, 26, 9, stock).stock
        stock = BOLL(20, stock).stock


        print(self.sma_short)
        print(stock.tail(5))
        return stock.tail(self.timeFrame)


    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        
        #if ind.long_line(self.sma_short, self.sma_mid, self.sma_long, window=2):
        #if ind.long_line(stock['close_10_sma'], stock['close_30_sma'], stock['close_60_sma'], window=2):
            #if ind.up_trend(stock['macdh']):
        #if stock['macdh'].iloc[-2] < 0 and stock['macdh'].iloc[-1] > 0: 
        if stock['boll_ub'].iloc[-1] < stock['close'].iloc[-1] and stock['rsi'].iloc[-1] <  75: 
                result = [False, f.get_cypto_price(), 1, stock.index[-1]] # self.long. stop loss price, buy share,time
                return result
        else:
            return None

    def sell(self, stock=None):
        if stock is None:
            stock = self.stock
        #if ind.compare_bigger(self.sma_mid, self.smsa_short, window=2): 
        #if ind.long_line(stock['close_10_sma'], stock['close_30_sma'], stock['close_60_sma'], window=2):
        if stock['close'].iloc[-1] < stock['boll'].iloc[-1]: 
                return [True, f.get_cypto_price(), 1, stock.index[-1]] # self.long , None, sell share, time 
        else:
            return None

class method_MACD_vol:
    def __init__(self, tker, feed, timeFrame=200):
        self.feed = feed
        self.tker = tker
        self.timeFrame = timeFrame
        self.buy_price = 0
        self.stock = self.calculate_stock()
        
    def calculate_stock(self):
        stock = stockstats.StockDataFrame.retype(self.feed)
        stock['rsi_14']
        stock['macdh']
        return stock.tail(self.timeFrame)
    
    #return 1 long 0 hold -1 sell
    def position(self, stock=None):
        if stock is None:
            stock = self.stock
        return 1

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        if stock['macdh'].iloc[-2] < 0 and stock['macdh'].iloc[-1] > 0: #macd cross 
                self.buy_price = stock['close'].iloc[-1] 
                result = [False, f.get_cypto_price(), 1, stock.index[-1]] # self.long. stop loss price, buy share,time
                return result            
        else:
            return None

    def sell(self, stock=None):
        if stock is None:
            stock = self.stock
        if stock['macdh'].iloc[-2] > 0 and stock['macdh'].iloc[-1] < 0: #macdcross
            return [True, f.get_cypto_price(), 1, stock.index[-1]] # self.long , None, sell share, time 
        else:
            return None

    def get_stock(self):
        return self.stock[['close','rsi_14','macdh']]

if __name__ == '__main__':
    #data = ind.load_cypto_day_price()
    #data = ind.load_cypto_hour_price()
    data = ind.load_cypto_day_price()
    a = method_MACD_vol('BTC', data)
    test = BackTesting('BTC',a.stock.copy(), a.buy, a.sell, a.position)
    test.run()
    print(test.get_transaction_log())
    


    










