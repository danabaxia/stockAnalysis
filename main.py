
import tradeStock as t
import robin_stocks as r
import financial as f 
import trading_algorithms as a
import numpy as np
import signal
import concurrent.futures 
import time
import matplotlib.pyplot as plt
import indicators as ind
from Method_kd import KD
from long_algo import Long_algo as la 
from Method_BOLL_SMA import BOLL_SMA


#user input robinhood account and password
#you may be asked to provide text message verify code
account = input('Enter account:\n')
password = input('Enter password:\n')

r.login(account,password)
def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

def algo_buy(tker):
    try:
        data = ind.load_stock_30min(tker)
        timeFrame = 20
        bar = BOLL_SMA(tker,data,timeFrame)
        if bar.buy():
            print(tker,'is to buy')
            money = 50
            check = a.checkCap(tker,200)
            if check:
                return a.buyStock(tker,money)
    except Exception as exc:
        print('failed to track ', tker,'error:',exc)
#this is for test purpose             
def algo_buy_test(tker):
    try:
        data = ind.load_stock_30min(tker)
        timeFrame = 20
        bar = BOLL_SMA(tker,data,timeFrame)
        if bar.buy():
            print(tker,'is to buy')
            return tker
        else:
            pass
    except Exception as exc:
        print('failed to track ', tker,'error:',exc)

while True:
    #watch_list = ['PENN','MT','CRM','NIO']
    """watch_list  = ['SQ', 'AAPL','BABA','PYPL','LIT','TAN','ARKK','AGNC','EVRI','NIO','XPEV',
                   'TSLA','TAN','RVLV','ZM','LIT','NVDA','SUN']"""
    watch_list = ['TAN','AMD','AAPL','UPS','ARKG','TSLA','NIO','BABA','LIT']
    long_list = []
    for tk in watch_list:
        data = ind.load_stock(tk, 200)
        timeFrame = 20
        a = la(tk,data,timeFrame)
        if a.buy():
            long_list.append(tk)
    print('[Info]:Long_list:',long_list)

    while f.isMarketOpen():
        #scan the long list of history price, check if any stock in long position
        #if in long position, put it into watch list with 


        if len(long_list) > 0:
            #print('stock list',my_stock_list)
            print('[Info]:Long_list:',long_list)
            #sell loss
            """try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor: 
                    results = list(map(lambda x: executor.submit(a.sellByReturn, x), my_stock_list))
                    for result in concurrent.futures.as_completed(results):
                        if result.result() in my_stock_list:
                            print('sell', result.result())
                            my_stock_list.remove(result.result())
            except Exception as exc:
                print('error:', exc)"""
            
            """try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor: 
                    results = list(map(lambda x: executor.submit(a.buyByAverage,x), my_stock_list))
                    for result in concurrent.futures.as_completed(results):   
                        data = result.result()
                        if data not in watch_list and data is not None:
                            print(result.result(),'add to watch list')
                            watch_list.append(result.result())
            except Exception as exc:
                print('buy evarage error: ', exc)"""
          
            #This section is buy action
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor: 
                    results = list(map(lambda x: executor.submit(algo_buy_test,x), watch_list))
                    for result in concurrent.futures.as_completed(results):
                        if result.result() in watch_list:
                            long_list.remove(result.result())
            except Exception as exc:
                    print('error: ',exc)
            
            
            time.sleep(60)

    print('still alive')
    time.sleep(60)





