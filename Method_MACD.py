from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import talib
from talib.abstract import *
from talib import MA_Type
import itertools



class method_MACD(BackTesting):
    def __init__(self, tker, fast, slow, signal, rsi, feed):
        self.feed = feed
        self.fast = fast 
        self.slow = slow
        self.signal = signal
        self.stock = self.calulate_stock() 
        self.rsi = rsi
        super().__init__(tker,self.stock)
 

    def calulate_stock(self):
        stock = stockstats.StockDataFrame.retype(self.feed)
        stock.MACD_EMA_SHORT = 15
        macdh = talib.MACD(stock['close'], fastperiod=self.fast, 
                           slowperiod=self.slow,signalperiod=self.signal)[2]
        #stock['macdh_b']=ind.get_binary(macdh) #macdh binary 
        stock['macdh'] = macdh
        stock['rsi'] = talib.RSI(stock['close'])
        #print(stock.head(50))
        return stock.round(2)

    def buy(self,stock):
        if stock['macdh'].iloc[-1] > 0 and  stock['macdh'].iloc[-2] < 0: 
            return True
        else:
            return False 

    def sell(self,stock):
        #print('close',stock['close'].iloc[-1], 'sma30', stock['close_30_sma'].iloc[-1])
        #if  stock['rsi'].iloc[-1] > 70 and stock['rsi'].iloc[-2] > stock['rsi'].iloc[-1]:
        if stock['rsi'].iloc[-1] > self.rsi: 
            return True
        else:
            return False
        pass

#generator combinatons 
def parameteras_generator():
    fast = range(2,12)
    slow = range(12,26)
    signal = range(2,9)
    #rsi = range(60,85)
    return itertools.product(fast,slow,signal)


tker = 'ARKG'
timeFrame = 200
data = ind.load_stock(tker,timeFrame)

"""#evaluation 
max_profit = 0
fast = 0
slow = 0
sig = 0
rsi = 0
for i in parameteras_generator():
    a = method_MACD(tker, i[0],i[1],i[2], 80, data)
    a.run()
    if a.get_portfolio() > max_profit:
        max_profit = a.get_portfolio()
        #rsi = i[0]
        fast = i[0]
        slow = i[1]
        sig = i[2]

print('fast ', fast,  'slow ',  slow, 'signal ', sig, 'rsi ', rsi, 'profit: ', max_profit )
#print('rsi ', rsi, 'profit: ', max_profit )
"""
a = method_MACD(tker,2, 19, 2, 81, data)
a.run()
a.get_portfolio()
a.get_portfolio_ref()
a.get_transaction_log()
