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
        stock = BOLL(20, stock).stock
        #print(stock.index)
        return stock.tail(self.timeFrame)

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        if stock['boll_ub'].iloc[-1] < stock['close'].iloc[-1] and stock['rsi_14'].iloc[-1] <  80: 
            self.buy_price = stock['close'].iloc[-1] 
            result = [False, f.get_cypto_price(), 1, stock.index[-1]] # self.long. stop loss price, buy share,time
            #print(stock.index[-1])
            return result
        else:
            return None

    def sell(self, stock=None):
        if stock is None:
            stock = self.stock
        if stock['close'].iloc[-1] < stock['boll'].iloc[-1]: 
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
        #print(stock.tail(5))
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

if __name__ == '__main__':
    data = ind.load_cypto_day_price()
    #data = ind.load_cypto_hour_price()
    #data = ind.load_cypto_30min_price()
    #data = ind.load_stock('AAPL', 200)
    a = method_test_boll('BCT', data, 200)
    bct = a.stock.copy()
    test = BackTesting('BCT',a.stock,a.buy,a.sell,cash=10000000,debug=0)
    test.run()
    print(test.get_transaction_log())
    buy = test.get_buy()
    sell = test.get_sell()
    print(test.get_returns())
    """plt.plot(bct['close'])
    #plt.plot(bct['close_10_sma'])
    #plt.plot(bct['close_30_sma'])
    #plt.plot(bct['close_60_sma'])
    plt.plot(bct['boll'])
    plt.plot(bct['boll_ub'])
    plt.plot(bct['boll_lb'])
    plt.scatter(buy, bct['close'][buy],label = 'buy', marker = '^', color = 'green')
    plt.scatter(sell, bct['close'][sell],label = 'sell', marker = 'v', color = 'red')
    plt.show()"""










