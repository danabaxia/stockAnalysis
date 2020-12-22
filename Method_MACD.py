from back_testing import BackTesting,plotter
import stockstats
import indicators as ind

class MACD:
    def __init__(self, tker, fast, slow, signal, rsi, feed, timeFrame):
        self.feed = feed
        self.fast = fast 
        self.slow = slow
        self.signal = signal
        self.timeFrame = timeFrame
        self.stock = self.calulate_stock().tail(timeFrame) 
        self.rsi = rsi

    def calulate_stock(self):
        stockstats.StockDataFrame.MACD_EMA_SHORT = self.fast
        stockstats.StockDataFrame.MACD_EMA_LONG = self.slow
        stockstats.StockDataFrame.MACD_EMA_SIGNAL = self.signal
        stock = stockstats.StockDataFrame.retype(self.feed)
        #macdh = talib.MACD(stock['close'], fastperiod=self.fast, 
        #                   slowperiod=self.slow,signalperiod=self.signal)[2]
        #stock['macdh_b']=ind.get_binary(macdh) #macdh binary 
        stock['macdh']
        print(stock['macdh'])
        #print(stock.head(50))
        return stock.round(2)

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        if stock['macdh'].iloc[-1] > 0 and  stock['macdh'].iloc[-2] < 0:
            if ind.up_trend(stock['macdh'],window=5): 
                return True
        else:
            return False 

    def sell(self, stock=None):
        if stock is None:
            stock = self.stock
        #print('close',stock['close'].iloc[-1], 'sma30', stock['close_30_sma'].iloc[-1])
        #if  stock['rsi'].iloc[-1] > 70 and stock['rsi'].iloc[-2] > stock['rsi'].iloc[-1]:
        #if stock['rsi'].iloc[-1] > self.rsi: 
        #    return True
        #else:
        #    return False
        pass


if __name__ == "__main__":
    tker = 'AAPL'
    timeFrame = 100
    data = ind.load_stock_30min(tker)
    a = MACD(tker, 12, 26, 9, 81, data, timeFrame)
    test = BackTesting(tker, a.stock, a.buy, a.sell)
    test.run()
    test.get_portfolio()
    test.get_portfolio_ref()
    test.get_transaction_log()
    test.get_bid_result(10)

    df = a.stock.copy()
    record = test.get_transaction_log().copy()
    d = plotter()
    d.plot_min(df, record, tker)
