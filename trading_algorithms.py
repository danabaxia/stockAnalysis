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
    ave = f.getPriceAverage(tker, 30)
    current = f.getPriceCurrent(tker)
    #current = 100
    print(tker, 'current', current, 'ave', ave)
    if current < ave:
        return tker
    else: print(tker,'not meet the conditions,quit')
    time.sleep(3)


def buyWhenUp(tker):
    money = 50
    percent = f.get1hourStockPriceChange(tker)
    print(tker,'1 hour change', percent)
    if percent > 1.5:
        print(tker,'is to buy')
        check = checkCap(tker,200)
        if check:
            r.orders.order_buy_fractional_by_price(tker,money,timeInForce='gfd',priceType='ask_price',extendedHours=False)
            print('buy', tker)
            logRecord(tker,'buy',money)
            return tker
    time.sleep(3)




def sellByReturn(tker):
    try:
        percent = t.getEquityChange(tker)
        print(tker, 'percent', percent)

        if percent < -15 and t.getEquity(tker) > 10:
            r.orders.order_sell_fractional_by_price(tker,t.getEquity(tker)*0.7,timeInForce='gfd',priceType='bid_price',extendedHours=False)
            print(tker,'sell 70%')
            logRecord(tker,'Sell', t.getEquity(tker)*0.7)
            return tker
        elif percent < -10 and t.getEquity(tker) > 10:
            r.orders.order_sell_fractional_by_price(tker,t.getEquity(tker)*0.5,timeInForce='gfd',priceType='bid_price',extendedHours=False)
            print(tker,'sell 50%')
            logRecord(tker,'Sell',t.getEquity(tker)*0.5)
            return tker
        elif percent > 10 and t.getEquity(tker) > 10: #collect profit 
            r.orders.order_sell_fractional_by_price(tker,t.getEquity(tker)*0.5,timeInForce='gfd',priceType='bid_price',extendedHours=False)
            logRecord(tker,'Sell',t.getEquity(tker)*0.5)
            print(tker,'sell 50%')
            return tker
        else : 
            print(tker,'is not to sell')
    except KeyError:
        print(tker,'does not exist in your profolio')
 

def checkCap(tker, cap):
    total_equity = t.getTotalEquity()
    invest = t.getTotalInvest()
    equity = t.getEquity(tker)
    print('profolio',tker, total_equity, cap ,invest, equity)
    if total_equity/invest < 0.8 and equity < cap:
        print('qualified to buy')
        return True
    else: 
        print('unqaulified to buy')
        return False


def logRecord(tker,action,amount):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open('log.csv', 'a') as csvfile:
        fieldnames = ['time', 'tiker','action','amount']
        writer = csv.writer(csvfile)
        writer.writerow([now,tker, action, amount])




