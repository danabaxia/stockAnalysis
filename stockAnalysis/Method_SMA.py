from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import talib 
import itertools


class method_SMA(BackTesting):
    def __init__(self, tker, period_long, period_short, feed):
        self.feed = feed
        self.long = period_long
        self.short = period_short
        self.stock = self.calulate_stock() 
        super().__init__(tker,self.stock)
 

    def calulate_stock(self):
        stock = stockstats.StockDataFrame.retype(self.feed)
        #stock['close_30_sma']
        stock['MA_long'] = talib.MA(stock['close'],  timeperiod=self.long)
        #print(stock['close_30_sma'])
        #print(stock['MA_long'])
        #stock['close_5_sma']
        stock['MA_short'] = talib.MA(stock['close'],  timeperiod=self.short)
        #print(stock)
        return stock.round(2)

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

#generator combinatons 
def parameteras_generator():
    sma_s = range(2,10)
    sma_l = range(10,15)
    return itertools.product(sma_s,sma_l)


tker = 'ARKK'
timeFrame = 200
data = ind.load_stock(tker,timeFrame)

#evaluation 
max_profit = 0
s = 0
l = 0
for i in parameteras_generator():
    a = method_SMA(tker, i[1], i[0], data)
    a.run()
    if a.get_portfolio() > max_profit:
        max_profit = a.get_portfolio()
        s = i[0]
        l = i[1]
print('Long ', l,  'short ',  s, 'profit: ', max_profit )

    


