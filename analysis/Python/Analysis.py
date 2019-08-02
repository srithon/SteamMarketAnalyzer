from Trend import *
from enum import Enum

from matplotlib import pyplot as plt

class Action(Enum):
    BUY, SELL, IGNORE = range(3)

def suggested_action(prices, fluctuation=None):
    direction = fluctuationDirection(fluctuation) if fluctuation is not None else fluctuation(prices)
    if direction == None:
        return Action.IGNORE
    elif direction == Direction.UP:
        return Action.SELL
    else:
        return Action.BUY

def check_volume(volume):
    return volume > 8

def check_price(price):
    return price < 80 and price > 25

"""
Passed in as
( item_name, fluctuation, prices, volume, times, action )

GOAL
Be able to switch between different plots

"""
def plot_items(tuple_list=None):
    plt.style.use('fivethirtyeight')
    figures = list()

    for tup in tuple_list:
        fig = plt.figure(tup[0])
        
        plt.plot(tup[4], tup[2], label=tup[0], linewidth=2)

        plt.ylim([0, 100])

        # plt.xticks(rotation=90)

        fig.autofmt_xdate()

        plt.xlabel('Time Recorded')
        plt.ylabel('Price (USD)')

        figures.append(fig)
    
    plt.show()

"""
suggestedAction volume (x:xs)
        | volume < 8 = Ignore
        | otherwise =
            case direction of 
                Nothing -> Ignore
                Just Up -> Sell
                Just Down -> Buy
            where direction = fluctuation (x:xs)
"""