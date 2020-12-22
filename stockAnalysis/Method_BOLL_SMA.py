from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import matplotlib.pyplot as plt
import datetime

#This method uses SMA20 as enter long signal
#boll lower band as buy signal 
class BOLL_SMA:
    def __init__(self, tker, boll_period, window, feed, timeFrame):
        self.feed = feed
        self.tker = tker
        self.boll_period = boll_period
        self.window = window
        self.timeFrame = timeFrame
        self.stock = self.calculate_stock().tail(timeFrame)
        self.long = self.calculate_long()
 

    def calculate_stock(self):
        #change class attributes before calculation 
        stockstats.StockDataFrame.BOLL_PERIOD = self.boll_period
        stock = stockstats.StockDataFrame().retype(self.feed)
        stock['boll'] 
        #stock._get_boll(stockstats.StockDataFrame())
        stock['boll_ub']
        stock['boll_lb']
        #print('period',stockstats.StockDataFrame.BOLL_PERIOD)
        #print(stock['boll_lb'].tail(3))
        stock['close_30_sma']
        #boll limit  
        stock['boll_bb'] = (stock['close'] - stock['boll_lb'])/(stock['boll_ub']-stock['boll_lb'])*100
        stock['boll_band'] = (stock['boll_ub'] - stock['boll_lb'])/stock['close_'+str(self.boll_period)+'_sma']
        #print(stock.tail(1))
        

        #print(stock['boll'].tail(3))
        #print(ind.up_trend(stock['boll'],window=2))
        #print(ind.down_trend(stock['boll'],window=1))

        return stock.round(2)

    def calculate_long(self):
        data = ind.load_stock(self.tker,200)
        return stockstats.StockDataFrame().retype(data)
        


    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        #lower band down trend, mid band up, upper band up
        if self.lower_lb(stock):
            return True
        else:
            return False 

    def lower_lb(self,stock=None, long=None):
        if stock is None:
            stock = self.stock
        if long is None:
            stock_l = self.long
        print(self.tker, stock['boll'].iloc[-1], stock['close'].iloc[-1], stock['boll_lb'].iloc[-1])
        #if ind.up_trend(stock_l['boll'], window=3):
        if stock['close'].iloc[-2] <  stock['boll_lb'].iloc[-2]:
            if stock['close'].iloc[-1] >= stock['boll_lb'].iloc[-1]:
                return True
        else:
            return False

    def higher_ub(self,stock=None):
        if stock is None:
            stock = self.stock
        if stock['close'].iloc[-1] >  stock['boll_ub'].iloc[-1]:
            return True
        else:
            return False


    def sell(self, stock=None):
        if stock is None:
            stock = self.stock
        #if ind.up_to_down_trend(stock['boll_band'],right_window=1): 
        #    return True
        #else:
        #    return False
        #pass

if __name__ == "__main__":
    tker = 'AMD'
    data = ind.load_stock_30min(tker) 
    timeFrame = len(data)
    #data = ind.load_stock_from_to('TDOC','2020-08-01','2020-12-01')
    a = BOLL_SMA(tker,20, 3, data, timeFrame)
    test = BackTesting(tker, a.stock, a.buy, a.sell)
    test.run()
    test.get_portfolio()
    test.get_portfolio_ref()
    print(test.get_transaction_log())
    #test.get_bid_result(10)
    d = plotter()
    df = a.stock.copy()
    record = test.get_transaction_log().copy()
    d.plot_min(df, record, tker)
    #plt.plot(datetimes, df['close'])
    #plt.show()
