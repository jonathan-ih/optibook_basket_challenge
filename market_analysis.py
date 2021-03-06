from optibook.synchronous_client import InfoOnly
import random
import time
import datetime
import pandas as pd
import numpy as np
from dataclasses import make_dataclass

def make_dataframe(tradeticks):
    columns=['Time', 'Price', 'Volume', 'Aggressor', 'Trade No']
    row_list = []
    for tick in tradeticks:
        data_dict = {"Time" : tick.timestamp.strftime('%Y%m%d'),
                    "Price" : tick.price,
                    "Volume" : tick.volume,
                    "Aggressor" : tick.aggressor_side,
                    "Trade No" : tick.trade_nr
        }
        row_list.append(data_dict)
    data = pd.DataFrame(row_list, columns = columns)
    return data

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

i = InfoOnly()
i.connect()

gather_time = 10
increment = 1

print("Initialising")
tb_tradeticks = i.poll_new_trade_ticks("TECH_BASKET")
amz_tradeticks = i.poll_new_trade_ticks("AMAZON")
ggl_tradeticks = i.poll_new_trade_ticks("GOOGLE")

print("Gathering data for {} seconds".format(gather_time))
time = 0
while time < gather_time:
    tb_book = i.get_last_price_book("TECH_BASKET")
    amz_book = i.get_last_price_book("AMAZON")
    ggl_book = i.get_last_price_book("GOOGLE")
    time += increment


tb_tradeticks = i.poll_new_trade_ticks("TECH_BASKET")
amz_tradeticks = i.poll_new_trade_ticks("AMAZON")
ggl_tradeticks = i.poll_new_trade_ticks("GOOGLE")

tb_data = make_dataframe(tb_tradeticks)
amz_data = make_dataframe(amz_tradeticks)
ggl_data = make_dataframe(ggl_tradeticks)
