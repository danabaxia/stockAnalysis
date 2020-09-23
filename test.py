import financial as f
import tradeStock as t
import numpy as np
import robin_stocks as r
import signal
import concurrent.futures
import time
import trading_algorithms as a



r.login('danabaxia@gmail.com','Hjb1314!@#$')

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


my_stock_list = ['DIS','AMZN','AAPL','TSLA', 'FB','TAN','NIO','MSFT','TDOC','GOOGL','SBUX','AMD','TQQQ','O','AGNC','PDD','CLOU','NKLA','PYPL','TWOU','V']

for tker in my_stock_list:
    print(tker,'ave',f.getPriceAverage(tker,30),'current',f.getPriceCurrent(tker))