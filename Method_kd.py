from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import itertools


class KD:
    def __init__(self, tker, kd_period, rsi_period, feed, timeFrame):
        self.tker = tker
        self.feed = feed
        self.period = kd_period 
        self.rsi_p = rsi_period
        self.timeFrame = timeFrame
        self.stock = self.calulate_stock().tail(timeFrame)
        print(self.stock)

    def calulate_stock(self):
        stock = stockstats.StockDataFrame.retype(self.feed)
        stock['kdjk_' + str(self.period)]
        stock['kdjd_' + str(self.period)]
        stock['kdjk_' + str(self.period) +'_xu_kdjd_' + str(self.period)]
        stock['kdjd_' + str(self.period) +'_xu_kdjk_' + str(self.period)]
        stock['rsi_'+ str(self.rsi_p)]
        stock['kdjd_' + str(self.period)]
        return stock.round(2)

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        if stock['kdjk_' + str(self.period) +'_xu_kdjd_' + str(self.period)].iloc[-1]:
            return True
        elif stock['rsi_'+ str(self.rsi_p)].iloc[-1] < 30:
            return True
        else:
            return False 
        pass

    def sell(self, stock):
        #print('close',stock['close'].iloc[-1], 'sma30', stock['close_30_sma'].iloc[-1])
        #if  stock['rsi'].iloc[-1] > 70 and stock['rsi'].iloc[-2] > stock['rsi'].iloc[-1]:
        #if stock['rsi_'+ str(self.rsi_p)].iloc[-1] > 80: 
        #if stock['kdjd_' + str(self.period) +'_xu_kdjk_' + str(self.period)].iloc[-1]:
        
        #if stock['kdjd_' + str(self.period) +'_xu_kdjk_' + str(self.period)].iloc[-1]:
        #    return True
        #else:
        #    return False
        pass    



if __name__ == "__main__":
    tker = 'AAPL'
    timeFrame = 100
    data = ind.load_stock_30min(tker)
    #data = ind.load_stock_from_to(tker, '2020-08-06', '2020-12-04')

    a = KD(tker, 10, 16, data, timeFrame)
    test = BackTesting(tker, a.stock, a.buy, a.sell)
    test.run()
    test.get_portfolio()
    test.get_portfolio_ref()
    test.get_transaction_log()
    d = plotter()
    df = a.stock.copy()
    record = test.get_transaction_log().copy()
    print(record)
    d.plot_min(df, record, tker)



