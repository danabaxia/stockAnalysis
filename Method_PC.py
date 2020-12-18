from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import matplotlib.pyplot as plt


class BOLL:
    def __init__(self, tker, buy_change, sell_change,feed, timeFrame):
        self.feed = feed
        self.buy_change = buy_change
        self.sell_change = sell_change
        self.timeFrame = timeFrame
        self.stock = self.calulate_stock().tail(timeFrame)
        self.long = True
 

    def calulate_stock(self):
        stock = stockstats.StockDataFrame().retype(self.feed)
        #print(stock['boll'].tail(3))
        return stock.round(2)

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        if self.long:
            if (stock['close'].iloc[-1] - stock['close'].iloc[-2])/stock['close'].iloc[-2]*100 < -3:
                self.long = False
                return True
        else:
            return False 

    def sell(self, stock=None):
        if stock is None:
            stock = self.stock
        if not self.long:
            if (stock['close'].iloc[-1] - stock['close'].iloc[-2])/stock['close'].iloc[-2]*100 > 3:
                self.long = True
                return True
        else:
            return False 
        #pass

if __name__ == "__main__":
    tker = 'TDOC'
    timeFrame = 100
    data = ind.load_stock_30min(tker) 
    #data = ind.load_stock_from_to('TDOC','2020-08-01','2020-12-01')
    a = BOLL(tker,20, 3, data, timeFrame)
    test = BackTesting(tker, a.stock, a.buy, a.sell)
    test.run()
    test.get_portfolio()
    test.get_portfolio_ref()
    test.get_bid_result(10)

