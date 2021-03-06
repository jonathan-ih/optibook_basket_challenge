
from optibook.synchronous_client import Exchange
import time
import sys
import datetime

# Bid = buy
# ask = sell

sys.stdout = open('output.txt', 'w')
print("Running: {}".format(datetime.datetime.now()))

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful!")

def get_prices(trade):
    if trade == 'trade':
        # sell basket, buy google and amazon
        tech_basket = get_best_price('TECH_BASKET', 'ask')
        google = get_best_price('GOOGLE', 'bid')
        amazon = get_best_price('AMAZON', 'bid')
    elif trade == 'reverse_trade':
        # buy basket, sell google and amazon
        tech_basket = get_best_price('TECH_BASKET', 'bid')
        google = get_best_price('GOOGLE', 'ask')
        amazon = get_best_price('AMAZON', 'ask')
    elif trade == 'check_bid':
        tech_basket = get_best_price('TECH_BASKET', 'bid')
        google = get_best_price('GOOGLE', 'bid')
        amazon = get_best_price('AMAZON', 'bid')
    elif trade == 'check_ask':
        tech_basket = get_best_price('TECH_BASKET', 'ask')
        google = get_best_price('GOOGLE', 'ask')
        amazon = get_best_price('AMAZON', 'ask')
  #  print('Prices for "{}" were \n\tTECH_BASKET = {}'
  #          '\n\tGOOGLE = {}\n\tAMAZON = {}'.format(trade, tech_basket, google, amazon))
    return tech_basket, google, amazon
    

def basket_price_diff(basket_price, amazon_price, google_price):
    difference = basket_price - (amazon_price + google_price)
    #print('Basket price - individual price = {}'.format(difference))
    return difference
    
    
# TO DO check the volume available to buy
def get_best_price(instrument, side): 
    order_book = e.get_last_price_book(instrument)
    
    if side == 'ask':
        return order_book.asks[0].price 
    elif side == 'bid':
        return order_book.bids[0].price
    else:
        raise KeyError("{} is not a valid key".format(side))
                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
def trade():
    print('Selling basket, buying individual stock')
    e.insert_order('TECH_BASKET', price=get_best_price('TECH_BASKET', 'ask'),
                    volume=1, side='ask', order_type='ioc')
    e.insert_order('GOOGLE', price=get_best_price('GOOGLE', 'bid'),
                    volume=1, side='bid', order_type='ioc')
    e.insert_order('AMAZON', price=get_best_price('AMAZON', 'bid'),
                    volume=1, side='bid', order_type='ioc')

    
def reverse_trade():
    print('Buying basket, selling individual stock')
    e.insert_order('TECH_BASKET', price=get_best_price('TECH_BASKET', 'bid'),
                    volume=1, side='bid', order_type='ioc')
    e.insert_order('GOOGLE', price=get_best_price('GOOGLE', 'ask'),
                    volume=1, side='ask', order_type='ioc')
    e.insert_order('AMAZON', price=get_best_price('AMAZON', 'ask'),
                    volume=1, side='ask', order_type='ioc')
                    


e = Exchange()
a = e.connect()

instruments = ["GOOGLE", "AMAZON", "TECH_BASKET"]
trade_threshold = 0.1
reverse_threshold = 1e-6

#Do the trading
try:
    trade_loop = 0
    while (trade_loop < 3): 
        print('Trade loop {}'.format(trade_loop))
        basket_price0, google_price0, amazon_price0 = get_prices('check_ask')
        basket_price1, google_price1, amazon_price1 = get_prices('check_bid')
        diff = (basket_price0+google_price0+amazon_price0)-(basket_price1+google_price1+amazon_price1)
        print('Overall diff {}'.format(diff))
        
        while True:
            try:
                basket_price, google_price, amazon_price = get_prices('trade')
              
                if basket_price_diff(basket_price, amazon_price, google_price)>trade_threshold:
                    trade()
                    print('Profit & loss: {}'.format(e.get_pnl()))
                    break
            except:
                pass
        while True:
            try:
                basket_price, google_price, amazon_price = get_prices('reverse_trade')
               
                if basket_price_diff(basket_price, amazon_price, google_price)<reverse_threshold:
                    reverse_trade()
                    print('Profit & loss: {}'.format(e.get_pnl()))
                    break
            except:
                pass
             
        print('Traded!')
        
        # limit speed of trading
        # 1/25th of second pause
        # 6 trades total        TODO update with number of trades in loop
        time.sleep(6 * 0.040)
        trade_loop += 1
        
    sys.stdout.close()
except:
    print('Oh no!')
    print('Number of trades:', trade_loop)
    print(e.get_positions())
    for s, p in e.get_positions().items():
        if p > 0:
            e.insert_order(s, price=get_best_price(s, 'bid'), volume=p, side='ask', order_type='ioc')
        elif p < 0:
            e.insert_order(s, price=get_best_price(s, 'ask'), volume=-p, side='bid', order_type='ioc')  
    print(e.get_positions())
    sys.stdout.close()