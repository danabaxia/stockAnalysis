import robin_stocks as r
import financial as f
import tradeStock as t
import time
import signal
import csv
from datetime import datetime

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

#scan 30 mins price change = (close -open)/open*100
def buyBy30min(tker):
    percent = f.get30minStockPriceChange(tker)
    if percent < -1.5:
        #calculate equity value to buy 
        print('trigger 1', tker)
        total_equity = t.getTotalEquity()
        #print('total equity', total_equity)
        cap = total_equity * 0.1
        invest = t.getTotalInvest()
        #print('total invest', invest)
        equity = t.getEquity(tker)
        #print('equity', equity)
        if total_equity/invest < 0.8 and equity < cap:
            print(equity/2)
            #s = r.orders.order_sell_fractional_by_price(tker,equity/2,timeInForce='gfd',priceType='None',extendedHours=False)
            #print('trigger2\n',s)
            return tker
        else: 
            print('no more money to put in')
    else: 
        print('30MIN',tker, percent)
    return "nothing happened"
#print(r.orders.order_buy_fractional_by_price('GOOGL', 50,timeInForce='gfd',priceType='ask_price',extendedHours=False))
#print(r.orders.order_sell_fractional_by_price('NKLA',3,timeInForce='gfd',priceType='ask_price',extendedHours=False))

#scan price change comapre to yesterday = (cuerent - yesterday_close) / yesterday_close
def buyByReturn(tker):
    percent = f.getTodayReturn(tker)
    if percent < -3.0:
        print('triger 3', tker)
        #calculate equity value to buy 
        total_equity = t.getTotalEquity()
        cap = 200
        invest = t.getTotalInvest()
        equity = t.getEquity(tker)
        #print(tker, total_equity, cap ,invest, equity)
        if total_equity/invest < 0.8 and equity < cap:
            #r.orders.order_buy_fractional_by_price(tker,50,timeInForce='gfd',priceType='None',extendedHours=False)
            print('trigger 4', tker)
            return True
    else: 
        print('DAY RETURN',tker, percent)
    return False


#compare price with average price in a period, e.g. 30 days
def buyByAverage(tker):
    try:
        ave = f.getPriceAverageByDay(tker, 30)
        current = f.getPriceCurrent(tker)
        print(tker, 'current', current, 'ave', ave)
        if current < ave:
            return tker
        else: 
            print(tker,'not meet the conditions,quit')
        time.sleep(3)
    except Exception as exc:
        print('failed to get average or current price for ', tker,'error:',exc)
        

def buyWhenUp(tker):
    try:
        money = 50
        percent = f.get1hourStockPriceChange(tker)
        print(tker,'1 hour change', percent)
        if percent > 1.0:
            print(tker,'is to buy')
            check = checkCap(tker,200)
            if check:
                return buyStock(tker,money)
    except Exception as exc:
        print('failed to get 1 hour  price change for ', tker,'error:',exc)

def sellByReturn(tker):
    try:
        percent = t.getEquityChange(tker)
        print(tker, 'percent', percent)
        try:
            value = t.getEquity(tker)
            if percent < -10:
                print(tker,'sell ',value)
                return sellStock(tker,f.round_half_down(value,2))
            elif percent > 10:
                print(tker, 'sell ', value*0.7)
                return sellStock(tker,f.round_half_down(value*0.7,2))
            else : 
                print(tker,'is not to sell')
        except Exception as exc:
            print('failed to get equity for ', tker,'error:',exc)
    except KeyError:
        print(tker,'does not exist in your profolio')
 

def checkCap(tker, cap):   
    total_equity = t.getTotalEquity()
    invest = t.getTotalInvest()
    if tker in t.getMyStockList():
        equity = t.getEquity(tker)
        print('total equity',total_equity, 'tker',tker, 'cap', cap,'invest', invest, 'equity',equity)
        if total_equity/invest < 0.8 and equity < cap:
            print('qualified to buy')
            return True
        else: 
            print('unqaulified to buy')
            return False
    else :
        if total_equity/invest < 0.8:
            print('qualified to buy')
            return True
        else:
            print('no more funds to invest')
            return False


def logRecord(tker,action,amount):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open('log.csv', 'a') as csvfile:
        fieldnames = ['time', 'tiker','action','amount']
        writer = csv.writer(csvfile)
        writer.writerow([now,tker, action, amount])





def buyStock(tker,value):
    flag = True
    buy = True
    count = 0
    while flag and count < 10:
        if buy:
            result = r.orders.order_buy_fractional_by_price(tker,value,timeInForce='gfd',extendedHours=False)
            print(result['id'])
        time.sleep(15)
        order = r.orders.get_stock_order_info(result['id'])
        print(order['state'])
        if order['state'] == 'filled':
            flag = False
            buy = False
            print('buy is complete')
            logRecord(tker,'buy',value)
            return tker
        elif order['state'] == 'cancelled':
            flag = True
            buy = True
            print('order has been cancelled')
        else: 
            flag = True
            buy = False
            print('checking state later')
        count +=1
        print('count',count)

def sellStock(tker,value):
    flag = True
    buy = True
    count = 0
    while flag and count < 10:
        if buy:
            result = r.orders.order_sell_fractional_by_price(tker,value,timeInForce='gfd',extendedHours=False)
            print(result['id'])
        time.sleep(15)
        order = r.orders.get_stock_order_info(result['id'])
        print(order['state'])
        if order['state'] == 'filled':
            flag = False
            print('buy is complete')
            logRecord(tker,'sell',value)
            return tker
        elif order['state'] == 'cancelled':
            buy = True
            print('order has been cancelled')
        else: 
            buy = False
            print('checking state later')
        count +=1
        print('count',count)