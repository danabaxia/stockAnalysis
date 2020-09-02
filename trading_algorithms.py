import robin_stocks as r

def in_and_out(ticker, value, price, limit, qt):
    if (price/value - 1.0) > limit:
        r.orders.order_sell_market(ticker, qt)
    elif (1.0 - price/value) > limit: 
        r.orders.order_buy_market(ticker, qt)