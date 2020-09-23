#build structure of the functions
import financial as f
import tradeStock as t
import robin_stocks as r
import trading_algorithms as a
import pandas as pd
import time


r.login('danabaxia@gmail.com','Hjb1314!@#$')

tker = 'AAPL'
print(f.getPriceAverageByDay(tker,20))


