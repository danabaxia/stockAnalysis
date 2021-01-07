from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import talib 
import itertools
import numpy as np 


class SMA:
    def __init__(self, tker, period, feed):
        self.feed = feed
        self.period = period
        self.stock = self.calulate_stock() 
 
    def calulate_stock(self):
        stock = stockstats.StockDataFrame.retype(self.feed)
        stock['close_'+str(self.period)+'_sma']
        stock['close_'+str(self.period)+'_sma_change'] = self.cal_change(stock['close_'+str(self.period)+'_sma'])
        #stock['MA_long'] = talib.MA(stock['close'],  timeperiod=self.long)
        #print(stock['close_30_sma'])
        #print(stock['MA_long'])
        #stock['close_5_sma']
        #stock['MA_short'] = talib.MA(stock['close'],  timeperiod=self.short)
        #print(stock)
        return stock.round(2)

    def cal_change(self,data):
        d = np.array(data.round(2))
        dif = np.diff(d)
        change = dif/d[:-1]*100
        change = np.insert(change,0,0)
        return change


    def buy(self,stock):
        #print('close_3_sma',stock['close_3_sma'].iloc[-1], 'sma30', stock['close_30_sma'].iloc[-1])
        #if stock['close_5_sma'].iloc[-1] < stock['close_30_sma'].iloc[-1]: 
        if stock['MA_short'].iloc[-1] < stock['MA_long'].iloc[-1]:
        #if ind.kd_buy_long(stock):    
            return True
        else:
            return False 

    def sell(self,stock):
        #print('close',stock['close'].iloc[-1], 'sma30', stock['close_30_sma'].iloc[-1])
        if  stock['close'].iloc[-1] > stock['MA_long'].iloc[-1]:
            return True
        else:
            return False
        pass


if __name__ is "__main__":
    pass

    


