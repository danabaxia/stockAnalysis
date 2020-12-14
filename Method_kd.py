from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import talib
from talib.abstract import *
from talib import MA_Type
import itertools



class method_KD(BackTesting):
    def __init__(self, tker, kd_period, rsi_period, feed):
        self.feed = feed
        self.period = kd_period 
        self.rsi_p = rsi_period
        self.stock = self.calulate_stock() 
        super().__init__(tker,self.stock)
 

    def calulate_stock(self):
        stock = stockstats.StockDataFrame.retype(self.feed)
        stock['kdjk_' + str(self.period)]
        stock['kdjd_' + str(self.period)]
        stock['kdjk_' + str(self.period) +'_xu_kdjd_' + str(self.period)]
        stock['kdjd_' + str(self.period) +'_xu_kdjk_' + str(self.period)]
        stock['rsi_'+ str(self.rsi_p)]
        #print(stock['rsi_14'])
        #print(stock['kdjd_' + str(self.period) +'_xu_kdjk_' + str(self.period)])
        return stock.round(2)

    def buy(self,stock):
        if stock['kdjk_' + str(self.period) +'_xu_kdjd_' + str(self.period)].iloc[-1]:
            return True
        elif stock['rsi_'+ str(self.rsi_p)].iloc[-1] < 30:
            return True
        else:
            return False 
        pass

    def sell(self,stock):
        #print('close',stock['close'].iloc[-1], 'sma30', stock['close_30_sma'].iloc[-1])
        #if  stock['rsi'].iloc[-1] > 70 and stock['rsi'].iloc[-2] > stock['rsi'].iloc[-1]:
        if stock['rsi_'+ str(self.rsi_p)].iloc[-1] > 90: 
        #if stock['kdjd_' + str(self.period) +'_xu_kdjk_' + str(self.period)].iloc[-1]:
            return True
        else:
            return False
        pass


#generator combinatons 
def parameteras_generator():
    #period = range(5,100)
    rsi = range(2,20)
    return itertools.product(rsi)


tker = 'ARKG'
timeFrame = 200
data = ind.load_stock(tker,timeFrame)

"""#evaluation 
max_profit = 0
period = 0
rsi = 0
for i in parameteras_generator():
    a = method_KD(tker, 9, i[0], data)
    a.run()
    if a.get_portfolio() > max_profit:
        max_profit = a.get_portfolio()
        rsi = i[0]

#print('kd period ', period, 'profit: ', max_profit )
print('rsi period ', rsi, 'profit ', max_profit)"""

a = method_KD(tker,9, 16, data)
a.run()
a.get_portfolio()
a.get_portfolio_ref()
a.get_transaction_log()
a.plot_profit()



