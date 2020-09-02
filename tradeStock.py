import robin_stocks as r
import trading_algorithms as m
import pandas as pd
import matplotlib.pyplot as plt
import time 
import signal 

#get all hodling stocks with holding values 
def getMyStockList():
    stock_list = {}
    my_stocks_info = r.build_holdings()
    print(my_stocks_info)
    for key in my_stocks_info.keys():
        stock_list[key] = float(my_stocks_info[key]['price'])
    return stock_list

def getMyStockHoldings():
    my_stock_info = r.build_holdings()
    p = pd.DataFrame.from_dict(my_stock_info, orient='index')
    print(p)

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

r.login('danabaxia@gmail.com','Hjb1314!@#$')

###read all the holdings
print(getMyStockHoldings())
#print(type(my_stocks_list['SPXU']))

"""

#=================================================================
###mian function start from here with ^ + C as interruption å
signal.signal(signal.SIGINT, keyboardInterruptHandler)
while True:
    for ticker in my_stocks_list.keys():
        price = r.stocks.get_latest_price(ticker)
        print(ticker, float(price[0]))
        #m.in_and_out(ticker, float(my_stocks_list[ticker]), float(price[0]), 0.03, 1)
    pass
"""