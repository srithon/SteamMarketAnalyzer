from Trend import *
from enum import Enum

from matplotlib import pyplot as plt

import math

price_upper_thresh = 150
price_lower_thresh = 45
volume_thresh = 6

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
    return volume > volume_thresh

def check_price(price):
    return price < price_upper_thresh and price > price_lower_thresh

"""
Passed in as
( item_name, fluctuation, prices, volume, times, action )

GOAL
Be able to switch between different plots

"""
def plot_items(tuple_list=None):
    plt.style.use('fivethirtyeight')
    # sub_plots = list()

    current_index = 0

    # TODO FIX SUBPlOT SWITCHING

    fig, subplots = plt.subplots(2)

    def plot_index(index=current_index):
        nonlocal tuple_list
        nonlocal fig
        nonlocal subplots

        row = tuple_list[index]        

        fig.canvas.set_window_title(row[0])
        # plt.xticks(rotation=45)

        subplots[0].title.set_text('Volume')
        subplots[1].title.set_text('Price')
        # subplots[1].margins(0.05)
        
        min, max = min_and_max(row[2])
        dist_from_min_and_max = ((max - min) * 0.75)
        min -= dist_from_min_and_max
        if min < 0:
            min = 0
        subplots[1].set_ylim([min, max + dist_from_min_and_max])
        
        subplots[1].plot(row[4], row[2], label=row[0], linewidth=2, marker='o', clip_on=False)
        # subplots[0].set_ymargin(1.0)
        
        subplots[1].text(0.3, 1.0, f'{row[-1]}: {row[1]:.3f}', horizontalalignment='center', 
        verticalalignment='center', transform=subplots[1].transAxes)

        subplots[0].plot(row[4], row[3], linewidth=2, marker='o', clip_on=True)
        # subplots[0].set_ylim(bottom=-0.50)
        subplots[0].set_ymargin(1.0)

        fig.autofmt_xdate()

        plt.tight_layout(h_pad=2.5)

    def plot_before_or_after(event):
        nonlocal current_index
        if event.key == 'right':
            current_index = (current_index + 1) % len(tuple_list)
        elif event.key == 'left':
            current_index -= 1
            if current_index < 0:
                current_index = len(tuple_list) + current_index
        subplots[0].clear()
        subplots[1].clear()
        plot_index(current_index)
        plt.draw()
    # generate_or_get(plt.gcf().number, True)

    plot_index()
    plt.gcf().canvas.mpl_connect('key_release_event', plot_before_or_after)
    plt.show()

def min_and_max(iterable):
    min = math.inf
    max = -math.inf
    
    for a in iterable:
        if a > max:
            max = a
        elif a < min:
            min = a
    
    return (min, max)

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