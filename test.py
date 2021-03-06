from optibook.synchronous_client import Exchange

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful!")

def basket_price_diff(basket_price, amazon_price, google_price):
    return basket_price - (amazon_price + google_price)
    

e = Exchange()
a = e.connect()

# Intruments
instruments = ["GOOGLE", "AMAZON", "TECH_BASKET"]
threshold = 0.01

# Trading loop
while True:
    # Poll order books for current trading data
    for instr in instruments:
        book = e.get_last_price_book(instr)
        print(book.instrument_id)
        print(book.asks)
        print(book.bids)
    # Decide which trades to make
    if (book.asks[0].price < thresholds[instr]):
        result = e.insert_order(instr, price=, volume=21, side='bid', order_type='limit')
    # Execute trades
    
    # Only do one loop to start with
    print("Profit and loss: {:.2f}".format(e.get_pnl()))
    break
