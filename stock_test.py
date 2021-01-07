from back_testing import BackTesting
import pandas as pd
import matplotlib.pyplot as plt
import indicators as ind
import stockstats 
from Method_boll import BOLL


class stock_test1:
    def __init__(self, data):
        self.data = data
        self.stock = self.cal_stock()

    def cal_stock(self):
        stock = stockstats.StockDataFrame.retype(data)
        stock['close_10_sma']
        stock['close_30_sma']
        stock['close_60_sma']
        stock['macdh']
        stock['rsi_14']
        stock = BOLL(30,stock).stock 
        print(stock[['boll_ub','boll']].tail(5))
        return stock

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock

        """if ind.three_line(stock['close_10_sma'],stock['close_30_sma'], stock['close_60_sma'],window=1):
            if ind.is_bottom(stock['macdh']):
                result = [False, stock['close'].iloc[-1], 1, stock.index[-1]]
                return result """
        #if not ind.long_line(stock['close_10_sma'],stock['close_30_sma'], stock['close_60_sma'],window=2):
        if stock['boll_ub'].iloc[-1] < stock['close'].iloc[-1] and stock['rsi_14'].iloc[-1] <  80: 
            result = [False, stock['close'].iloc[-1], 1, stock.index[-1]]
            return result 


    def sell(self, stock=None):
        if stock is None:
            stock = self.stock

        if stock['close'].iloc[-1] < stock['boll'].iloc[-1]: 
            result =  [True, stock['close'].iloc[-1], 1, stock.index[-1]]
            return result





#tickers = ind.get_all_tickers()['tiker']
#for tker in tickers:
if __name__ == "__main__":
    tker = 'TAN'
    data = ind.load_stock_30min(tker)
    a = stock_test1(data)
    stock = a.stock.copy().tail(100)
    test = BackTesting(tker, a.stock.tail(100), a.buy, a.sell,cash=1000000)
    test.run()
    print(test.get_transaction_log())
    print(tker, test.get_returns())

    """buy = test.get_buy()
    sell = test.get_sell()
    fig,(ax1,ax2) = plt.subplots(2,figsize=(12,4))
    ax1.plot(stock['close'])
    ax1.plot(stock['close_10_sma'])
    ax1.plot(stock['close_30_sma'])
    ax1.plot(stock['close_60_sma'])
    ax1.scatter(buy, stock['close'][buy],label = 'buy', marker = '^', color = 'green')
    ax1.scatter(sell, stock['close'][sell],label = 'sell', marker = 'v', color = 'red')
    ax2.plot(stock['macdh'])
    fig.suptitle(tker)
    plt.show()"""