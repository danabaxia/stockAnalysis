import pandas as pd
import indicators as ind
import matplotlib.pyplot as plt
import talib
import stockstats

class VOSC:
    def __init__(self, feed):
        self.feed = feed
        self.tker = tker
        self.stock = self.calculate_stock()
    
    def calculate_stock(self):
        stock = stockstats.StockDataFrame().retype(self.feed)
        shortlen = 5
        longlen = 10
        short = talib.EMA(self.feed['volume'], shortlen)
        long = talib.EMA(self.feed['volume'], longlen)
        osc = 100*(short - long) / long 
        stock['VOSC'] = osc
        return stock


if __name__ == "__main__":
    tker = 'AMD'
    data = ind.load_stock(tker, 200) 
    print(data)
    a = VOSC(data)
    plt.plot(a.stock['VOSC'])
    plt.show()
    