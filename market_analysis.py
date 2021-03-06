from optibook.synchronous_client import Exchange
import numpy as np 
import scipy

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful!")

e = Exchange()
a = e.connect()


tradeticks = e.get_trade_history("TECH_BASKET")

for tick in tradeticks:
    print("{}\t{}".format(tick.price, tick.volume))
