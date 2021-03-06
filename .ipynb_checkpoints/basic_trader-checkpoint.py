
from optibook.synchronous_client import Exchange
import time

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
    
    return tech_basket, google, amazon
    

def basket_price_diff(basket_price, amazon_price, google_price):
    difference = basket_price - (amazon_price + google_price)
    print("Basket price - individual_difference)
    return difference
    
    
# TO DO check the volume available to buy
def get_best_price(instrument, side): ### Fix what happens when there is no stock available to buy
    order_book = e.get_last_price_book(instrument)
    if side == 'ask':
        return order_book.asks[0].price 
    elif side == 'bid':
        return order_book.bids[0].price
    else:
        raise KeyError("{} is not a valid key".format(side))
                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
def trade():
    # sell basket
    e.insert_order('TECH_BASKET', price=get_best_price('TECH_BASKET', 'ask'),
                    volume=1, side='bid', order_type='ioc')
    # buy google
    # buy amazon
    e.insert_order('GOOGLE', price=get_best_price('GOOGLE', 'bid'),
                    volume=1, side='ask', order_type='ioc')
    e.insert_order('AMAZON', price=get_best_price('AMAZON', 'bid'),
                    volume=1, side='ask', order_type='ioc')

    
def reverse_trade():
    # sell basket
    e.insert_order('TECH_BASKET', price=get_best_price('TECH_BASKET', 'bid'),
                    volume=1, side='ask', order_type='ioc')
    # buy google
    # buy amazon
    e.insert_order('GOOGLE', price=get_best_price('GOOGLE', 'ask'),
                    volume=1, side='bid', order_type='ioc')
    e.insert_order('AMAZON', price=get_best_price('AMAZON', 'ask'),
                    volume=1, side='bid', order_type='ioc')
                    


e = Exchange()
a = e.connect()

instruments = ["GOOGLE", "AMAZON", "TECH_BASKET"]
trade_threshold = 0.01
reverse_threshold = 1e-6

#Do the trading
try:
    while True: 
        while True:
            # look up prices TO DO
            try:
                basket_price, google_price, amazon_price = get_prices('trade')
                if basket_price_diff(basket_price, amazon_price, google_price)>trade_threshold:
                    trade()
                    print(e.get_pnl())
                    break
            except:
                pass
        while True:
            # look up prices TO DO
            basket_price, google_price, amazon_price = get_prices('reverse_trade')
            if basket_price_diff(basket_price, amazon_price, google_price)<reverse_threshold:
                reverse_trade()
                print(e.get_pnl())
                break
            
        print('Traded!')
        
        # limit speed of trading
        # 1/25th of second pause
        # 6 trades total        TODO update with number of trades in loop
        time.sleep(6 * 0.040)


except:
    print('Oh no!')
    print(e.get_positions())
    for s, p in e.get_positions().items():
        if p > 0:
            e.insert_order(s, price=0, volume=p, side='ask', order_type='ioc')
        elif p < 0:
            e.insert_order(s, price=0, volume=-p, side='bid', order_type='ioc')  
    print(e.get_positions())
    print('run away!')