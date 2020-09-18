import financial as f
import tradeStock as t
import numpy as np
import robin_stocks as r
import signal
import concurrent.futures
import time
import trading_algorithms as a


r.login('danabaxia@gmail.com','Hjb1314!@#$')
"""
#====================================================
#tker = 'BRKB'
my_stock_list = ['AAPL','TSLA', 'FB','TAN','NIO','MSFT','TDOC','GOOGL','TWOU','SBUX','NVDA']
r.login('danabaxia@gmail.com','Hjb1314!@#$')

for tker in my_stock_list:
    priceChange = {}
    for data in f.request1hourStockPrice(tker):
        c = float((data['close']- data['open'])/data['open']*100)
        priceChange[data['date']] = c
        if c > 0.7:
            print(tker,data['date'],c, data['volume'])
#print(f.getPriceAverage(tker, 30))

#for tker in t.getMyStockList():
#    print(tker, 'price average', f.getPriceAverage(tker,20), 'current', f.getPriceCurrent(tker))

#print(np.average(priceChange))
#print(t.getMyStockHoldings())
"""
"""
#day = 60
#print(day)
data = f.requestHistoryStockPrice(tker)
sample = {}
for item in data:
    if item['changePercent'] < -3:
        print(item['date'], item['changePercent'])

#plt.plot(priceChange)
#plt.show()
#=========================================
"""
def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


#my_stock_list = ['AMD','FB','NIO','TDOC','TSLA','MSFT']

while True:
    watch_list = []
    my_stock_list = ['TSLA', 'FB','TAN','NIO','MSFT','TDOC','GOOGL','SBUX','AMD','TQQQ','O','AGNC','PDD','CLOU','NKLA']
    while not f.isMarketOpen():
        signal.signal(signal.SIGINT, keyboardInterruptHandler)
        if len(my_stock_list) > 0:
            print('stock list',my_stock_list)
            print('watch list', watch_list)
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor: 
                results = list(map(lambda x: executor.submit(a.sellByReturn, x), my_stock_list))
                for result in concurrent.futures.as_completed(results):
                    if result.result() in my_stock_list:
                        print('sell', result.result())
                        my_stock_list.remove(result.result())
            
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor: 
                results = list(map(lambda x: executor.submit(a.buyByAverage,x), my_stock_list))
                for result in concurrent.futures.as_completed(results):   
                    if result.result() not in watch_list and result.result() is not None:
                        print(result.result(),'add to watch list')
                        watch_list.append(result.result())
            
            #check watch list to buy
            if len(watch_list) > 0:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor: 
                    results = list(map(lambda x: executor.submit(a.buyWhenUp,x), watch_list))
                    for result in concurrent.futures.as_completed(results):
                        if result.result() in watch_list:
                            print(result.result(), 'buy complete')
                            watch_list.remove(result.result())
                            my_stock_list.remove(result.result())
            