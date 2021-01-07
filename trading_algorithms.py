import robin_stocks as r
import financial as f
import tradeStock as t
import time
import signal
import csv
from datetime import datetime
import csv
import concurrent.futures 
import indicators as ind



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
#ave_percent is int between 0-1
def buyByAverage(tker):
    try:
        ave_percent = 0.1
        ave = f.getPriceAverageByDay(tker, 30)
        current = f.getPriceCurrent(tker)
        print(tker, 'current', current, 'ave', ave)
        if current < ave*(1+ave_percent):
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
        if percent > 10.0:
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
            if percent < -7 and value > 50:
                print(tker,'sell ',value)
                return sellStock(tker,f.round_half_down(value,2))
            elif percent > 10 and value > 50:
                print(tker, 'sell ', value*0.7)
                return sellStock(tker,f.round_half_down(value*0.7,2))
            else : 
                print(tker,'is not to sell')
        except Exception as exc:
            print('failed to get equity for ', tker,'error:',exc)
    except KeyError:
        print(tker,'does not exist in your profolio')
    except: 
        print('connection error')
 

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

def checkCap_cypto(cap):
    equity = t.get_my_cypto_value()
    print('[Info] current invest ', equity)
    if equity < cap:
        print('invest under the cap') 
        return True
    else: 
        print('invest exceeds the cap') 
        return False


def logRecord(tker,action,amount):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open('log/log.csv', 'a') as csvfile:
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


#==========================
#read from csv for stocks
def read_stocks(f):
    up_stock=[]
    flat_stock=[]
    strong_stock=[]
    down=[]
    with open(f) as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            print(len(row))
    return readCSV
            

#read_stocks('my_stock.csv')

#buy stradegy 
#when price below 10% high of 30 day ave move, put it into watchlist
#then decide to buy when one hour change up to 1%
def method1(my_stock_list,watch_list,candidate_list):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor: 
            results = list(map(lambda x: executor.submit(buyByAverage,x), my_stock_list))
            for result in concurrent.futures.as_completed(results):   
                data = result.result()
                if data not in watch_list and data is not None:
                    print(result.result(),'add to watch list')
                    watch_list.append(result.result())
    except Exception as exc:
        print('buy evarage error: ', exc)
    #check price change to yesterday
    if len(watch_list) > 0:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor: 
                results = list(map(lambda x: executor.submit(buyByReturn,x), watch_list))
                for result in concurrent.futures.as_completed(results):
                    data = result.result()
                    if data not in candidate_list and data is not None:
                        print(result.result(),'add to watch list')
                        candidate_list.append(result.result())
        except Exception as exc:
            print('buywhenup error: ',exc)
    #check 1 hour change
    if len(candidate_list) > 0:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor: 
                results = list(map(lambda x: executor.submit(buyWhenUp,x), watch_list))
                for result in concurrent.futures.as_completed(results):
                    if result.result() in watch_list:
                        watch_list.remove(result.result())
                        my_stock_list.remove(result.result())
        except Exception as exc:
            print('buywhenup error: ',exc)
    return my_stock_list,watch_list


#cypto transaction 
def buyBTC(tker, value):
    flag = True
    buy = True
    count = 0
    while flag and count < 10:
        if buy:
            result = r.orders.order_buy_crypto_by_price(tker,value,priceType='mark_price',timeInForce='gtc')
            print(result['id'])
        time.sleep(15)
        order = r.get_crypto_order_info(result['id'])
        print(order)
        print(order['state'])
        if order['state'] == 'filled':
            flag = False
            buy = False
            price = order['rounded_executed_notional']
            print('bought ',price)
            logRecord_BTC(tker,'buy',price)
            return 'BUY'
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

def sellBTC(tker,value):
    flag = True
    buy = True
    count = 0
    equity = t.get_my_cypto_value()
    if value > equity: # if equity is less than sell amount 
        value = equity 
    while flag and count < 10:
        if buy:
            result = r.orders.order_sell_crypto_by_price(tker,value,priceType='ask_price',timeInForce='gtc')
            print(result['id'])
        time.sleep(15)
        order = r.orders.get_stock_order_info(result['id'])
        print(order['state'])
        if order['state'] == 'filled':
            flag = False
            price = order['rounded_executed_notional']
            print('sold ',price)
            logRecord_BTC(tker,'sell',price)
            return 'SELL'
        elif order['state'] == 'cancelled':
            buy = True
            print('order has been cancelled')
        else: 
            buy = False
            print('checking state later')
        count +=1
        print('count',count)

def logRecord_BTC(tker,action,amount):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    List = [now, tker, action, amount]
    with open('log/log_BTC.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(List)

if __name__ == "__main__":
    #t.login()
    #result = r.orders.order_sell_crypto_by_price('BTC', 10, priceType='bid_price',timeInForce='gtc')
    #id = result['id']
    #print(result)
    #print(id)
    #result = r.get_crypto_order_info('97e9ac10-b5f5-490b-a3c1-27b9ed8de2a4')
    #status = result['rounded_executed_notional']
    #print(result)
    #print(status)
    tker = 'BTC'
    price = 50
    logRecord_BTC(tker,'buy',price)