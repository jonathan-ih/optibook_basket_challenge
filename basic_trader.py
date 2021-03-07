
from optibook.synchronous_client import Exchange
import time
import sys
import datetime

# Bid = buy
# ask = sell

#sys.stdout = open('output.txt', 'w')
print("Running: {}".format(datetime.datetime.now()))

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful!")

e = Exchange()
a = e.connect()

instruments = ["GOOGLE", "AMAZON", "TECH_BASKET"]

def get_prices(trade):
    '''if trade == 'trade':
        # sell basket, buy google and amazon
        tech_basket = get_best_price('TECH_BASKET', 'ask')
        google = get_best_price('GOOGLE', 'bid')
        amazon = get_best_price('AMAZON', 'bid')
    elif trade == 'reverse_trade':
        # buy basket, sell google and amazon
        tech_basket = get_best_price('TECH_BASKET', 'bid')
        google = get_best_price('GOOGLE', 'ask')
        amazon = get_best_price('AMAZON', 'ask')'''
    if trade == 'trade':
        # sell basket, buy google and amazon
        tech_basket = get_best_price('TECH_BASKET', 'bid')
        google = get_best_price('GOOGLE', 'ask')
        amazon = get_best_price('AMAZON', 'ask')
    elif trade == 'reverse_trade':
        # buy basket, sell google and amazon
        tech_basket = get_best_price('TECH_BASKET', 'ask')
        google = get_best_price('GOOGLE', 'bid')
        amazon = get_best_price('AMAZON', 'bid')    
    elif trade == 'check_bid':
        tech_basket = get_best_price('TECH_BASKET', 'bid')
        google = get_best_price('GOOGLE', 'bid')
        amazon = get_best_price('AMAZON', 'bid')
    elif trade == 'check_ask':
        tech_basket = get_best_price('TECH_BASKET', 'ask')
        google = get_best_price('GOOGLE', 'ask')
        amazon = get_best_price('AMAZON', 'ask')
    return tech_basket, google, amazon
    

def basket_price_diff(basket_price, amazon_price, google_price):
    difference = basket_price - (amazon_price + google_price)
    return difference
    
    
# TO DO check the volume available to buy
def get_best_price(instrument, side): 
    order_book = e.get_last_price_book(instrument)
    
    if side == 'ask':
        asks = order_book.asks
        if asks:
            return asks[0].price 
        else: 
            return None
            
    elif side == 'bid':
        bids = order_book.bids
        if bids:
            return bids[0].price
        else:
            return None
    else:
        raise KeyError("{} is not a valid key".format(side))
                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
def trade(basket_price, google_price, amazon_price):
    #print('Selling basket, buying individual stock')
    #e.insert_order('TECH_BASKET', price=get_best_price('TECH_BASKET', 'ask'),
    #                volume=1, side='ask', order_type='ioc')
    e.insert_order('TECH_BASKET', basket_price,
                    volume=1, side='ask', order_type='ioc')
    e.insert_order('GOOGLE', google_price,
                    volume=1, side='bid', order_type='ioc')
    e.insert_order('AMAZON', amazon_price,
                    volume=1, side='bid', order_type='ioc')

    
def reverse_trade(basket_price, amazon_price, google_price):
    #print('Buying basket, selling individual stock')
    #e.insert_order('TECH_BASKET', price=get_best_price('TECH_BASKET', 'bid'),
    #                volume=1, side='bid', order_type='ioc')
    #e.insert_order('GOOGLE', price=get_best_price('GOOGLE', 'ask'),
    #                volume=1, side='ask', order_type='ioc')
    #e.insert_order('AMAZON', price=get_best_price('AMAZON', 'ask'),
    #                volume=1, side='ask', order_type='ioc')
    e.insert_order('TECH_BASKET', basket_price,
                    volume=1, side='bid', order_type='ioc')
    e.insert_order('GOOGLE', google_price,
                    volume=1, side='ask', order_type='ioc')
    e.insert_order('AMAZON', amazon_price,
                    volume=1, side='ask', order_type='ioc')    
         
         
def get_buy_prices():
    # Get the lowest (ask) price for each instrument
    # The lowest price someone is selling the stock for
    google_price = get_best_price('GOOGLE', 'ask')
    amazon_price = get_best_price('AMAZON', 'ask')
    basket_price = get_best_price('TECH_BASKET', 'ask')
    return google_price, amazon_price, basket_price
    
def get_sell_prices():
    # Get the highest (bid) price for each instrument
    # The highest price someone is willing to pay for the stock
    google_price = get_best_price('GOOGLE', 'bid')
    amazon_price = get_best_price('AMAZON', 'bid')
    basket_price = get_best_price('TECH_BASKET', 'bid')
    return google_price, amazon_price, basket_price
    
def clear_initial_positions():
    while True:
        buy_google, buy_amazon, buy_basket = get_buy_prices()
        sell_google, sell_amazon, sell_basket = get_sell_prices()
        
        # Check to see if any of the instruments have no asks or bids
        # If they do, pass to the next iteration and wait until they do
        if (not (buy_google and buy_amazon and buy_basket and
            sell_google and sell_amazon and sell_basket)):
            continue
        else:
            buy_prices = {'GOOGLE' : buy_google,
                          'AMAZON' : buy_amazon,
                          'TECH_BASKET' : buy_basket}
            sell_prices = {'GOOGLE' : sell_google,
                          'AMAZON' : sell_amazon,
                          'TECH_BASKET' : sell_basket}
            break
        
    positions = e.get_positions()
    for inst in instruments:
        if (positions[inst] > 0):
            order = e.insert_order(inst, price=sell_prices[inst], volume=positions[inst], side='ask', order_type='ioc')
        elif (positions[inst] < 0):
            order = e.insert_order(inst, price=buy_prices[inst], volume=-positions[inst], side='bid', order_type='ioc')

################################################################################

# Clear any initial positions
print("Starting positions: {}".format(e.get_positions()))
while (e.get_positions()['GOOGLE'] != 0 or e.get_positions()['AMAZON'] != 0 or e.get_positions()['TECH_BASKET'] != 0):
    clear_initial_positions()
    print("Starting positions: {}".format(e.get_positions()))



while True:
    buy_google, buy_amazon, buy_basket = get_buy_prices()
    sell_google, sell_amazon, sell_basket = get_sell_prices()
    
    # Check to see if any of the instruments have no asks or bids
    # If they do, pass to the next iteration and wait until they do
    if (not (buy_google and buy_amazon and buy_basket and
        sell_google and sell_amazon and sell_basket)):
        continue
    
    individual_cost_to_buy = buy_google + buy_amazon
    individual_cost_to_sell = sell_google + sell_amazon
    basket_cost_to_buy = buy_basket
    basket_cost_to_sell = sell_basket
    
    if (individual_cost_to_buy < basket_cost_to_buy or 
        individual_cost_to_sell < basket_cost_to_sell):
        # Cheaper to buy individual stocks than basket
        # OR Make more money by selling baskets than selling individually
        # Buy individual stocks and sell basket
        e.insert_order('TECH_BASKET', price=sell_basket, volume=1, side='ask', order_type='ioc')      # Place on ask side of order book to match highest bid
        e.insert_order('GOOGLE', price=buy_google, volume=1, side='bid', order_type='ioc')            # Place on bid side of order book to match lowest ask
        e.insert_order('AMAZON', price=buy_amazon, volume=1, side='bid', order_type='ioc')            # Place on bid side of order book to match lowest ask
        
        
    elif (individual_cost_to_buy > basket_cost_to_buy or
          individual_cost_to_sell < basket_cost_to_sell):
        # Cheaper to buy baskets than individual stocks
        # OR Make more money by selling individually than selling baskets
        # Buy baskets and sell individual stocks
        e.insert_order('TECH_BASKET', price=buy_basket, volume=1, side='bid', order_type='ioc')       # Place on bid side of order book to match lowest ask
        e.insert_order('GOOGLE', price=sell_google, volume=1, side='ask', order_type='ioc')           # Place on ask side of order book to match highest bid
        e.insert_order('AMAZON', price=sell_amazon, volume=1, side='ask', order_type='ioc')           # Place on ask side of order book to match highest bid
        
    time.sleep(3 * 0.04)
    
    # If there are no discrepencies between the price of the individual
    # stocks and the price of the baskets then seek to bring our current 
    # position to zero. Can't be done by simply buying basket and selling 
    # individualy at market price as this will produce a loss equal to the
    # bid-ask spread of the instruments. To bring positions to zero without
    # loss, must sell for more than it was bought for, or buy it for less
    # than we sold it for.
    # Alternatively, wait for the discrepency to go the other way and 
    # do as above, or buy and sell for the same price.
    # Choices:
    #       1. buy and sell in the middle of the bid-ask spread so we are 
    #          the best trade for both buying and selling. As long as the 
    #          orders are for the same price we will lose no money.
    #       2. buy and sell at other (possibly different) values to try to 
    #          drive the market ourselves
    # Choose 1 for now
    
    # TODO Currently not all orders complete (no one wants to buy/sell) so 
    # positions no longer of the form 
    #    {'GOOGLE' : +x,
    #     'AMAZON' : +x,
    #     'TECH_BASKET' : -x}
    # If the signs change the program can attempt to buy/sell a negative number
    # Fix by checking to see if order is completed, not double posting orders
    
    positions = e.get_positions()
    if (positions['TECH_BASKET'] > 0):
        # Sell excess tech basket then buy individual stocks (note -ve sign on volume)
        e.insert_order('TECH_BASKET', price=((buy_basket + sell_basket) / 2), volume=positions["TECH_BASKET"], side='ask', order_type='ioc')
        e.insert_order('GOOGLE', price=((buy_google + sell_google) / 2), volume=-positions["GOOGLE"], side='bid', order_type='ioc')
        e.insert_order('AMAZON', price=((buy_amazon + sell_amazon) / 2), volume=-positions["AMAZON"], side='bid', order_type='ioc')
    elif (positions['TECH_BASKET'] < 0):
        # Sell excess individual stock then buy basket (note -ve sign on volume)
        e.insert_order('GOOGLE', price=((buy_google + sell_google) / 2), volume=positions["GOOGLE"], side='ask', order_type='ioc')
        e.insert_order('AMAZON', price=((buy_amazon + sell_amazon) / 2), volume=positions["AMAZON"], side='ask', order_type='ioc')
        e.insert_order('TECH_BASKET', price=((buy_basket + sell_basket) / 2), volume=-positions["TECH_BASKET"], side='bid', order_type='ioc')
    else:
        # No positions to close
        pass

    print("{}\t{}".format(e.get_pnl(), e.get_positions()))
    time.sleep(3 * 0.04)

#trade_threshold = 1.0#0.2
#reverse_threshold = 1e-6
#
##Do the trading
#try:
#    trade_loop = 0
#    print('Trying to do the thing')
#    while (trade_loop < 3): 
#        '''print('Trade loop {}'.format(trade_loop))
#        basket_price0, google_price0, amazon_price0 = get_prices('check_ask')
#        basket_price1, google_price1, amazon_price1 = get_prices('check_bid')
#        diff = (basket_price0+google_price0+amazon_price0)-(basket_price1+google_price1+amazon_price1)
#        print('Overall diff {}'.format(diff))'''
#        
#        while True:
#            try:
#                basket_price, google_price, amazon_price = get_prices('trade')
#              
#                if basket_price_diff(basket_price, amazon_price, google_price)>trade_threshold:
#                    #print('trying to trade b: {}, a: {}, g:{}'.format(basket_price, amazon_price, google_price))
#                    trade(basket_price-0.1, amazon_price+0.1, google_price+0.1) # add some change to make us competitive?
#                    print('Profit & loss: {}'.format(e.get_pnl()))
#                    print('traded b: {}, a: {}, g:{}'.format(basket_price, amazon_price, google_price))
#                    break
#            except:
#                pass
#        while True:
#            try:
#                basket_price, google_price, amazon_price = get_prices('reverse_trade')
#               
#                if basket_price_diff(basket_price, amazon_price, google_price)<reverse_threshold:
#                    reverse_trade(basket_price, amazon_price, google_price)
#                    print('Profit & loss: {}'.format(e.get_pnl()))
#                    break
#            except:
#                pass
#             
#        print('Traded!')
#        
#        # limit speed of trading
#        # 1/25th of second pause
#        # 6 trades total        TODO update with number of trades in loop
#        time.sleep(6 * 0.040)
#        trade_loop += 1
#        
#    #sys.stdout.close()
#except:
#    print('Oh no!')
#    print(sys.exc_info()[0])
#    print('Number of trades:', trade_loop)
#    print(e.get_positions())
#    for s, p in e.get_positions().items():
#        if p > 0:
#            e.insert_order(s, price=get_best_price(s, 'bid'), volume=p, side='ask', order_type='ioc')
#        elif p < 0:
#            e.insert_order(s, price=get_best_price(s, 'ask'), volume=-p, side='bid', order_type='ioc')  
#    print(e.get_positions())
#    #sys.stdout.close()