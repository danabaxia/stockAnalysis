import financial as f
import tradeStock as t
import numpy as np
import robin_stocks as r
import signal
import concurrent.futures
import time
import trading_algorithms as a
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import csv




#r.login('danabaxia@gmail.com','Hjb1314!@#$')
#tker = '%5EGSPC'

"""stock_list = []
candidate = {'tker':[],'below 25':[]}
stock_exchanges = ['NYSE','Nasdaq','NYSE Arca','Nasdaq Global Select','New York Stock Exchange','NASDAQ Capital Market','NYSE American','NASDAQ Global Market','NasdaqCM','NasdaqGM','NasdaqGS']
data = f.readStockFromCSV()"""

"""def isfloat(string):
    try:
        float(string)
        return True
    except:
        return False

for i in range(len(data)):
    if i == 0:
        next
    if isfloat(data[i][2]):
        if float(data[i][2]) > 5 and float(data[i][2]) <50:
            if data[i][-1] in stock_exchanges:
                stock_list.append(data[i][0])"""

#print(stock_list)

"""
def sort_stock(tker):
    try:
        data = f.requestHistoryStockPrice_s(tker)
        below = 0
        count = 0
        for daily in data:
            date = daily['date']
            price = daily['close']
            ave = f.getPriceAverageFrom(tker,date,30)
            print(date,price,ave)
            if float(price) < float(ave):
                below += 1
            count += 1
            if count > 100:
                break
        print(tker, below)
        if below <= 25:
            candidate['tker'].append(tker)
            candidate['below 25'].append(below)
    except Exception as exc:
        print("error: ", exc)


for tker in stock_list:
    try:
        sort_stock(tker)
    except Exception as exc:
        print('error', exc)
 
"""

"""f =pd.DataFrame(stock_list)
f.to_csv("output.csv")"""


"""tker = 'NIO'
result = {'date':[],'price':[],'average_15':[],'average_30':[]}
data = f.requestHistoryStockPrice_s(tker)
count = 0
below = 0
for daily in data: 
    date = daily['date']
    price = daily['close']
    ave_15 = f.getPriceAverageFrom(tker,date,15)
    ave_30 = f.getPriceAverageFrom(tker,date,30)
    result['date'].append(date)
    result['price'].append(price)
    result['average_15'].append(ave_15)
    result['average_30'].append(ave_30)
    if float(price) < float(ave_30):
        below += 1
    count += 1
    if count > 100:
        break
result_pd = pd.DataFrame(result)
result_pd = result_pd.iloc[::-1]
print(result_pd)
print(below)



ax = plt.gca()
result_pd.plot(kind='line',x='date',y='price', ax=ax)
result_pd.plot(kind='line',x='date',y='average_15', ax=ax)
result_pd.plot(kind='line',x='date',y='average_30', ax=ax)



plt.show()"""



