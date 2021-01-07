#from datetime import datetime
import datetime
import financial as f 
import pandas as pd 
from abc import abstractmethod, ABC
import matplotlib as plt
import indicators as ind 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import csv

#calculate buy and sell info, returns 
class BackTesting(ABC):

    def __init__(self, tker, feed, buy, sell, cash=10000,debug=0):
        self.__tker = tker
        self.__feed = feed
        self.method_buy = buy 
        self.method_sell = sell 
        self.debug = debug
        self.__buy = []
        self.__sell = []
        self.buy_index = []
        self.sell_index = []
        self.__result = []
        self.__cash = cash
        self.__cash_ini = cash
        self.__portfolio = 0 
        self.__share = 0
        self.__transaction = pd.DataFrame()
        self.__bars = []
        self.__daily_profit = None
        self.__profit = None
        self.long = True
        self.stop_loss = 0
        self.log= pd.DataFrame(columns=['Time', 'transaction', 'share', 'price', 'cash', 'holdings'])
  
    def run(self):
        stock_n = None
        row_list = []
        index_list = []
        i = 0
        for index, row in self.__feed.iterrows():
            row_list.append(list(row))
            index_list.append(index)
            stock_n = pd.DataFrame(row_list,columns=self.__feed.columns, index=index_list)
            if i > 5:
                if self.long is True: 
                    if not self.method_buy(stock_n) is None: #long position 
                        self.__buy.append(index)
                        self.buy_index.append(i)
                        result = self.method_buy(stock_n)
                        self.long = result[0]
                        self.stop_loss = result[1]
                        share = result[2]
                        self.market_buy(index,share,row['close'])
                elif self.long is False: 
                    if not self.method_sell(stock_n) is None: # short position
                        self.__sell.append(index)
                        self.sell_index.append(i)
                        self.long, _, share, _ = self.method_sell(stock_n)
                        self.market_sell(index,share,row['close'])
                        
            i +=1
        #execute orders based on time marks 
        #self.get_returns()
        #create transaction log
        self.log_transaction()
        #calulate profit 
        #self.get_returns_trend()

    def get_buy(self):
        return self.__buy

    def get_sell(self):
        return self.__sell

    def get_buy_index(self):
        return self.buy_index

    def get_sell_index(self):
        return self.sell_index

    def get_returns(self):
         return round(self.__share*self.__feed['close'].iloc[-1] + self.__cash - self.__cash_ini, 2)

    
    def get_portfolio(self):
        self.__portfolio = self.__share*self.__feed['close'].iloc[-1] + self.__cash
        print(f'[Info] Total portfolio:  {self.__portfolio:.2f}')
        print(f'[Info] Total return:  {(self.__portfolio - self.__cash_ini)/self.__cash_ini*100:.2f}')
        return (self.__portfolio - self.__cash_ini)/self.__cash_ini*100

        
    
    def market_buy(self, time, share, price):
        #share = int(self.__cash*0.1/price)
        assert (price < self.__cash),  "You are broken, Game over!"
        if share > 0:
            self.__share += share
            self.__cash -= price*share  
            bar = [time, 'Buy', share, price, self.__cash, self.__share,
                   self.__share*price + self.__cash]
            self.__bars.append(bar)
    
    def market_sell(self, time, share, price):
        #share = int(self.__share*0.2)
        if share > 0: # and share < self.__share:
            self.__share -= share
            self.__cash += price*share  
            bar = [time, 'Sell', share, price, self.__cash, self.__share, 
                   self.__share*price + self.__cash]
            self.__bars.append(bar)

    #log table
    #time       transaction    share     price     cash   holding_shares  
    def log_transaction(self):       
        columns = ['Time', 'transaction', 'share', 'price', 'cash', 'holdings','total invest']
        self.__transaction = pd.DataFrame(self.__bars, columns=columns)

    
    def get_transaction_log(self):
        #print('Info:Transaction Log')
        #print(self.__transaction)
        return self.__transaction
    
    def get_bid_result(self,period):
        result = []
        df = self.__transaction.copy()
        stock = self.__feed.copy()
        date = list(stock.index)
        for d in df['Time']:
            index = date.index(d)
            if index + period >= len(date):
                result.append('n/a')
            else:
                current = stock['close'].iloc[index]
                future = stock['close'].iloc[index + period]
                if df[df['Time']==d]['transaction'].iloc[0] == 'Buy':
                    if future > current:
                        result.append('WIN')
                    else:
                        result.append('LOSE')
                elif df[df['Time']==d]['transaction'].iloc[0] == 'Sell':
                    if future < current:
                        result.append('WIN')
                    else:
                        result.append('LOSE')
        self.__transaction['result'] = result
        print(self.__transaction)
        count = self.__transaction['result'].str.count('WIN').sum()
        print('win ', count, 'out of ', len(self.__transaction), 'win chance is ', round(count/len(self.__transaction)*100,2),'%')


                    


    #calculate daily
    """def get_returns_trend(self):
        dates = np.array(self.__feed[self.__timeFrame:].index)  
        price = self.__feed['close']
        cash = np.zeros(len(dates), dtype= float)
        cash.fill(self.__cash_ini)
        stock = np.zeros(len(dates), dtype= float)
        values = np.zeros(len(dates), dtype= float)
        t = self.__transaction.copy()
        start = 0
        for i in range(len(dates)):
            if dates[i] in list(t['Time']):
                if (t.loc[t['Time'] == dates[i]]['transaction'] == 'Buy').bool()   == True:
                    index = t[t['Time'] ==dates[i]].index[0] #row number 
                    cash[i:] = t['cash'].iloc[index]
                    stock[i:] =  t['holdings'].iloc[index]
                elif (t.loc[t['Time'] == dates[i]]['transaction'] == 'Sell').bool()   == True:
                    index = t[t['Time'] ==dates[i]].index[0] #row number 
                    cash[i:]= t['cash'].iloc[index]
                    stock[i:] =  t['holdings'].iloc[index]
                    
        values = cash + stock*price
        # calculate daily returns 
        dif = np.diff(values)
        dif = np.insert(dif, 0, 0., axis=0) # insert 0 at the top 
        profit = np.round(dif/values*100,2)
        self.__daily_profit = profit 
        #calculate accumulative returns 
        profit = np.round((values - self.__cash_ini)/self.__cash_ini*100,2)
        trend = list(zip(dates,price, cash, stock, values, profit))
        returns = pd.DataFrame(trend, columns = ['date', 'price','cash','holding','values','profit'])
        #print(returns)
        self.__profit = profit"""

    def plot_profit(self):
        p = plotter()
        p.plot_profit(self.__profit)

    def get_portfolio_ref(self):
        print('[Info] Stock Price change until today: ', 
               (self.__feed['close'].iloc[-1] - self.__feed['close'].iloc[0])/self.__feed['close'].iloc[0]*100)
    

#calculate buy and sell info, returns 
class ForwardTesting(ABC):

    def __init__(self, tker, feed, buy, sell, cash=10000,debug=0):
        self.__tker = tker
        self.__feed = feed
        self.method_buy = buy 
        self.method_sell = sell 
        self.debug = debug
        self.__buy = []
        self.__sell = []
        self.__result = []
        self.__cash = cash
        self.cash_ini = cash
        self.__portfolio = 0 
        self.__share = 0
        self.__transaction = pd.DataFrame()
        self.long = True

  
    def run(self):
        self.update_position()
        stock = self.__feed
        if self.long is True: 
            if not self.method_buy(stock) is None: #long position 
                result = self.method_buy(stock)
                self.long = result[0]
                price = result[1]
                share = result[2]
                index = result[3]
                self.market_buy(index,share,price)
        elif self.long is False: 
            if not self.method_sell(stock) is None: #short position
                result = self.method_sell(stock)
                self.long = result[0]
                price = result[1]
                share = result[2]
                index = result[3]
                self.market_sell(index,share,price)

        self.get_returns()
        
        print('[Info]long', self.long)

    def update_position(self):
        transaction = pd.read_csv('log/forward_test.csv')
        if len(transaction) > 0:
            if transaction['transaction'].iloc[-1] == 'Buy':
                self.long = False
            elif transaction['transaction'].iloc[-1] == 'Sell':
                self.long = True

                        


    def get_returns(self):
        transaction = pd.read_csv('log/forward_test.csv')
        if len(transaction) == 0:
            total = self.cash_ini
        else:
            share = transaction['share'].iloc[-1]
            cash = transaction['cash'].iloc[-1]
            price = self.__feed['close'].iloc[-1]
            total = cash + price*share 
            print('[Info] Transaction Log')
            print(transaction)
        print('[Info]Total', total)
        return total
        
    
    def market_buy(self, time, share, price):
        #share = int(self.__cash*0.1/price)
        assert (price < self.__cash),  "You are broken, Game over!"
        if share > 0:
            self.__share += share
            self.__cash -= price*share  
            bar = [time, 'Buy', share, price, self.__cash, self.__share,
                   self.__share*price + self.__cash]
            self.log_transaction(bar)
    
    def market_sell(self, time, share, price):
        #share = int(self.__share*0.2)
        if share > 0: # and share < self.__share:
            self.__share -= share
            self.__cash += price*share  
            bar = [time, 'Sell', share, price, self.__cash, self.__share, 
                   self.__share*price + self.__cash]
            self.log_transaction(bar)

    #log table
    #time       transaction    share     price     cash   holding_shares  
    def log_transaction(self,bar):       
        with open('log/forward_test.csv', 'a') as f:
            write = csv.writer(f)
            write.writerow(bar)




#draw price trend and mark buy and sell points
class plotter():
    def __init__(self):
        super().__init__()
        self.years = mdates.YearLocator()   # every year
        self.months = mdates.MonthLocator()  # every month
        self.days = mdates.DayLocator() # every day 
        self.hours = mdates.HourLocator() # every hour 
        self.autoLocator = mdates.AutoDateLocator()
        self.minutes = mdates.MinuteLocator() # every minute 
        self.years_fmt = mdates.DateFormatter('%Y')
        self.months_fmt = mdates.DateFormatter('%m-%d')


        

    def plot_price(self,x,y):
        plt.plot(x,y)
        plt.show()

    def plot_day(self, df, record, label):
        datetimes = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in df.index]
        fig, (ax1, ax2) = plt.subplots(2, figsize=(12,4))
        ax1.xaxis.set_major_locator(self.months)
        ax1.xaxis.set_major_formatter(self.months_fmt)
        ax1.xaxis.set_minor_locator(self.days)
        ax1.grid(True)
        ax1.set_ylabel(label)
        ax1.plot( datetimes, df['boll_band'])

        ax2.grid(True)
        ax2.set_ylabel('Price')
        ax2.plot(datetimes, df['close'], label='price')
        ax2.plot(datetimes, df['boll_ub'], label='boll_ub')
        ax2.plot(datetimes, df['boll'], label='boll')
        ax2.plot(datetimes, df['boll_lb'], label='boll_lb')
        plt.legend()
        
        fig.autofmt_xdate()
        fig.suptitle(label)
        x = record['Time'].loc[record['transaction'] == 'Buy']
        y = df['boll_band'].loc[x]
        ax1.scatter(x, y, label = 'test', marker = '^', color = 'green')
        x = record['Time'].loc[record['transaction'] == 'Sell']
        y = df['boll_band'].loc[x]
        ax1.scatter(x, y, label = 'sell', marker = 'v', color='red')
        plt.show()

    def plot_min(self, df, record, label):
        fig, (ax1, ax2) = plt.subplots(2, figsize=(12,4))
        ax1.plot(df['close'])
        ax2.plot(df['boll_band'])
    
        x = record['Time'].loc[record['transaction'] == 'Buy']
        y = df['close'].loc[x]
        ax1.scatter(x, y, label = 'buy', marker = '^', color = 'green')
        x = record['Time'].loc[record['transaction'] == 'Sell']
        y = df['close'].loc[x]
        ax1.scatter(x, y, label = 'sell', marker = 'v', color='red')
        fig.suptitle(label)
        plt.legend()
        plt.show()

    def plot_result(self, df, record): 
        fig, ax = plt.subplots(figsize=(12,4))
        ax.plot(df['close'])
        x = record['Time'].loc[record['transaction'] == 'Buy']
        y = df['close'].loc[x]
        ax.scatter(x, y, label = 'buy', marker = '^', color = 'green')
        x = record['Time'].loc[record['transaction'] == 'Sell']
        y = df['close'].loc[x]
        ax.scatter(x, y, label = 'sell', marker = 'v', color='red')
        plt.legend()
        plt.show()

    

    def buy(self):
        pass

    def sell(self):
        pass

