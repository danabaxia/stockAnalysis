
import tradeStock as t
import robin_stocks as r
import financial as f 
import trading_algorithms as a
import numpy as np
import signal
import concurrent.futures 
import time
import matplotlib.pyplot as plt
import indicators as i



r.login('danabaxia@gmail.com','Hjb1314!@#$')

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


while True:
    #watch_list = ['PENN','MT','CRM','NIO']
    watch_list  = ['SQ', 'AAPL','BABA','PYPL','LIT','TAN','ARKK','AGNC','EVRI','NIO','XPEV',
                   'TSLA','TAN','RVLV','ZM','LIT','NVDA','SUN']
    dividend_list = ['T','AGNC']
    while f.isMarketOpen():
        if len(watch_list) > 0:
            #print('stock list',my_stock_list)
            print('watch list', watch_list)
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
            #check watch list to buy
            if len(watch_list) > 0:
                try:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor: 
                        results = list(map(lambda x: executor.submit(i.algo_buy,x), watch_list))
                        for result in concurrent.futures.as_completed(results):
                            if result.result() in watch_list:
                                watch_list.remove(result.result())
                                #my_stock_list.remove(result.result())
                except Exception as exc:
                    print('buywhenup error: ',exc)
            time.sleep(60)

    print('still alive')
    print(watch_list)
    time.sleep(60)





