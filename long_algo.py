from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import matplotlib.pyplot as plt
import datetime

#This method uses SMA20 as enter long signal
#boll lower band as buy signal 
class Long_algo:
    def __init__(self, tker, feed, timeFrame):
        self.feed = feed
        self.tker = tker
        self.timeFrame = timeFrame
        self.stock = self.calculate_stock().tail(timeFrame)
 

    def calculate_stock(self):
        stock = stockstats.StockDataFrame().retype(self.feed)
        stock['close_20_sma']
        #print(stock['boll'].tail(3))
        #print(ind.up_trend(stock['boll'],window=2))
        #print(ind.down_trend(stock['boll'],window=1))

        return stock.round(2)
        

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        #lower band down trend, mid band up, upper band up
        if self.sma(stock):
            return True
        else:
            return False 

    def sma(self,stock=None):
        if stock is None:
            stock = self.stock
        if ind.up_trend(stock['close_20_sma'],window=3):
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
    tker = 'SNOW'
    data = ind.load_stock(tker,300) 
    timeFrame = 100
    #data = ind.load_stock_from_to('TDOC','2020-08-01','2020-12-01')
    a = Long_algo(tker,data, timeFrame)
    test = BackTesting(tker, a.stock, a.buy, a.sell)
    test.run()
    test.get_portfolio()
    test.get_portfolio_ref()
    print(test.get_transaction_log())
    #test.get_bid_result(10)
    d = plotter()
    df = a.stock.copy()
    record = test.get_transaction_log().copy()
    #d.plot_min(df, record, tker)