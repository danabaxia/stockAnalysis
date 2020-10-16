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
tker = 'TWOU'
X = f.request1hourStockPrice(tker)
d = pd.DataFrame(X)
d = d.loc[:,['date','close']]
Y = d.to_numpy()
d1 = d.loc[:,['close']]
Y = np.flip(Y,axis=0)
Y1 = d1.to_numpy()
Y1 = np.flip(Y1)
#future price
Y2 = np.delete(Y1,0,0) 
#last price
Y3 = np.delete(Y1,-1,0)
#print(Y2.shape)
#print(Y3.shape)
Y4 = (Y2 - Y3)/Y3*100
#print(Y1)
#print(Y4)
#print(Y2)
Y5 = np.stack((Y4,Y2),axis=1).reshape((199,2))
#print(np.array(Y5,dtype=float))
print(Y5)
flag = False
equity = 0
num = 0
cash = 1000
cost = 0
index = 0
fund = 1000
for i in range(0,199):
    if Y5[i][0] < -1 and cash > Y5[i][1]*2:
        num = num + 2
        cash = cash - Y5[i][1]*2
        cost = cost + Y5[i][1]*2
        index = i
        flag = False
        print('index',index,'drop',Y5[i][0],'[num',num,'cash',cash,'cost',cost)
    equity = num*Y5[i][1]
    #print('equity',equity)
    if (equity - cost)/cost*100 > 10:
        print('equity',equity,'cost',cost)
        num = num - num//3
        cash = cash + num//3*Y5[i][1]
        print('return index', i, 'num',num,'cash',cash)

equity = Y5[-1][1]*num
print('hold profit', (fund//Y5[0][1]*Y5[-1][1]-fund)/fund*100)
print('num', num, 'equity',equity, 'cash', cash, 'profit', (equity + cash - fund)/fund*100)
