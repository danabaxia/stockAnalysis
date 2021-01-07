
import tradeStock as t
import robin_stocks as r
import financial as f 
import trading_algorithms as ta
import numpy as np
import signal
import concurrent.futures 
import time
import matplotlib.pyplot as plt
import indicators as ind
from Method_kd import KD
from long_algo import Long_algo 
from Method_BOLL_SMA import BOLL_SMA
from cypto_test import method_test_boll




def algo_trade(tker, data):
    try:
        tker = 'BTC'
        #data = ind.load_cypto_day_price()
        #data = ind.load_cypto_hour_price()
        timeFrame = 10
        bar = method_test_boll('BTC', data, timeFrame)
        time = bar.get_stock().index[-1]
        print(time)
        equity = t.get_my_cypto_value()
        print('[Info]My invest equity ', equity)
        #print(bar.get_stock().tail(3))
        print('\n')
        cap = 300
        empty = 30
        buy = 50
        sell = 50
        if equity < cap and bar.buy():
            print('[Info]buy triggered!')
            return ta.buyBTC(tker, buy)
        elif equity > sell and bar.sell():    
            print('[Info]sell triggered!')
            sell_money = 50
            return ta.sellBTC(tker, sell)
        else: 
            print(bar.stock[['close', 'volume','boll_ub','boll','rsi_14']].tail(3)) 
    except Exception as exc:
        print('failed to track ', tker,'error:',exc)

#user input robinhood account and password
#you may be asked to provide text message verify code
t.login()
clock = None
while True:
    tker = 'BTC'
    data = ind.load_cypto_30min_price()
    current_clock = data['date'].iloc[-1]
    print('clock', clock)
    print('current clock', current_clock)
    if not clock == current_clock: # if there is a new data generated based on the time 
        result = algo_trade(tker, data)
    else: 
        print('skip')
    clock = current_clock
    time.sleep(10)