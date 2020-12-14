from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import talib
from talib.abstract import *
from talib import MA_Type
import itertools



class method_BOLL(BackTesting):
    def __init__(self, tker, boll_period, feed):
        self.feed = feed
        self.boll_period = boll_period
        self.stock = self.calulate_stock() 
        super().__init__(tker,self.stock)
 

    def calulate_stock(self):
        #change class attributes before calculation 
        stockstats.StockDataFrame.BOLL_PERIOD = self.boll_period
        stock = stockstats.StockDataFrame().retype(self.feed)
        stock['boll'] 
        #stock._get_boll(stockstats.StockDataFrame())
        stock['boll_ub']
        stock['boll_lb']
        #print('period',stockstats.StockDataFrame.BOLL_PERIOD)
        #print(stock['boll'].tail(3))
        

        #print(stock['boll'].tail(3))
        #print(ind.up_trend(stock['boll'],window=2))
        #print(ind.down_trend(stock['boll'],window=1))

        return stock.round(2)

    def buy(self,stock):
        #lower band down trend, mid band up, upper band up 
        if ind.down_trend(stock['boll_lb'],window=2):
            if ind.up_trend(stock['boll'],window=2):
                if ind.up_trend(stock['boll_ub'],window=2):
                    return True
        else:
            return False 
        pass

    def sell(self,stock):
        #print('close',stock['close'].iloc[-1], 'sma30', stock['close_30_sma'].iloc[-1])
        #if  stock['rsi'].iloc[-1] > 70 and stock['rsi'].iloc[-2] > stock['rsi'].iloc[-1]:
        #if stock['rsi_'+ str(self.rsi_p)].iloc[-1] > 90: 
        #if stock['kdjd_' + str(self.period) +'_xu_kdjk_' + str(self.period)].iloc[-1]:
        #    return True
        #else:
        #    return False
        pass

    def __del__(self):
        pass


#generator combinatons 
def parameteras_generator():
    #period = range(5,100)
    period = range(5,100)
    return itertools.product(period)


tker = 'TDOC'
timeFrame = 200

#evaluation 
"""max_profit = 0
period = 0
for i in parameteras_generator():

    data = ind.load_stock(tker,timeFrame)
    a = method_BOLL(tker, i[0], data)
    a.run()
    #print(i[0])
    if a.get_portfolio() > max_profit:
        max_profit = a.get_portfolio()
        period = i[0]
    del a
print('boll period ', period, 'profit ', max_profit)"""

data = ind.load_stock(tker,timeFrame) 
a = method_BOLL(tker,9, data)
a.run()
a.get_portfolio()
a.get_portfolio_ref()
a.get_transaction_log()
a.plot_profit()