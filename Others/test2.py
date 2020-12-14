#build structure of the functions
import financial as f
import tradeStock as t
import robin_stocks as r
import trading_algorithms as a
import pandas as pd
import time
import json
import csv
import numpy as np


#r.login('danabaxia@gmail.com','Hjb1314!@#$')



"""stock_list = []
stock_exchanges = ['NYSE','Nasdaq','NYSE Arca','Nasdaq Global Select','New York Stock Exchange','NASDAQ Capital Market','NYSE American','NASDAQ Global Market','NasdaqCM','NasdaqGM','NasdaqGS']
data = f.readStockFromCSV()

def isfloat(string):
    try:
        float(string)
        return True
    except:
        return False

for i in range(len(data)):
    if i == 0:
        next
    if isfloat(data[i][2]):
        if float(data[i][2]) > 10 and float(data[i][2]) <500:
            if data[i][-1] in stock_exchanges:
                stock_list.append(data[i][0])"""


"""
#sort out good stock

good_candidate = []
for tker in stock_list:
    try:
        price = f.getPriceCurrent(tker)
        eva_30 = f.getPriceAverageByDay(tker,30)
        rate = float(f.requestStockRate(tker))
        if price < eva_30 and rate >= 3:
            good_candidate.append([tker,price, eva_30,rate])
            print(tker, 'price', price, 'average move', eva_30, 'rate', rate)
    except Exception as exc:
        print(tker, 'error: ',exc)

f.saveListToCSV(good_candidate,['tker','price','30_average','rate'], True)"""


#this is to test the efficiency of the method over a stock 
tker = 'AAPL'
X = f.requestHistoryStockPrice_s(tker)
d = pd.DataFrame(X)
d = d.loc[:,['date','close']]
print(d)