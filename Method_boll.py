from back_testing import BackTesting, plotter
import financial as f 
import pandas as pd 
import stockstats
import indicators as ind
import matplotlib.pyplot as plt
import datetime


class BOLL:
    def __init__(self, boll_period, feed):
        self.feed = feed
        self.boll_period = boll_period
        self.stock = self.calulate_stock()
 

    def calulate_stock(self):
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
        stock['boll_band'] = (stock['boll_ub'] - stock['boll_lb'])/stock['boll']*100
        #print(stock.tail(5))
        

        #print(stock['boll'].tail(3))
        #print(ind.up_trend(stock['boll'],window=2))
        #print(ind.down_trend(stock['boll'],window=1))

        return stock.round(2)

    def buy(self, stock=None):
        if stock is None:
            stock = self.stock
        #lower band down trend, mid band up, upper band up
        if self.lower_lb(stock):
            return True
        else:
            return False 

    def squeze(self,stock=None):
        if stock is None:
            stock = self.stock
        if ind.down_to_up_trend(stock['boll_band']):
            return True
        else:
            return False

    def stradedy_bb(self,stock=None):
        if stock is None:
            stock = self.stock
        if ind.up_trend(stock['boll']):
            if ind.down_to_up_trend(stock['boll_band'],right_window=2):
                return True
        else:
            return False

    def lower_lb(self,stock=None):
        if stock is None:
            stock = self.stock
        if stock['close'].iloc[-2] <  stock['boll_lb'].iloc[-2]:
            if stock['close'].iloc[-1] >= stock['boll_lb'].iloc[-1]:
                return True
        else:
            return False

    def lower_lb_with_ub_trend_up(self,stock=None):
        if stock is None:
            stock = self.stock
        if ind.up_trend(stock['boll_ub'],window=3):
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
    #tker = 'TSLA'
    timeFrame = 200
    i = 0
    for tker in ind.get_all_tickers():
        try:
            data = ind.load_stock(tker,200) 
            a = BOLL(tker,21, data, timeFrame)
            test = BackTesting(tker, a.stock, a.lower_lb_with_ub_trend_up, a.sell)
            test.run()
            #test.get_portfolio()
            #test.get_portfolio_ref()
            print(tker)
            print(test.get_transaction_log())
            i  += 1
        except Exception as exc:
            print(tker,'error: ',exc)
        if i > 20:
            break
    #test.get_bid_result(10)
    #d = plotter()
    #df = a.stock.copy()
    #record = test.get_transaction_log().copy()
    #d.plot_min(df, record, tker)
    #plt.plot(datetimes, df['close'])
    #plt.show()
