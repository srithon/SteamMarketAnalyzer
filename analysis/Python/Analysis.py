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
    # sub_plots = list()

    """
    def switch_figure_if_left_or_right(event):
        if event.key == 'right':
            new_fig = (plt.gcf().number + 1) % len(tuple_list)
            print(f'New figure: {new_fig}')
            plt.figure(new_fig)
        elif event.key == 'left':
            f = plt.gcf().number - 1
            if f < 0:
                f = len(tuple_list) + f
            print(f'New figure: {f}')
            plt.figure(f)
    """

    """
    def generate_or_get(index, override=False):
        if index in plt.get_fignums() and not override:
            plt.figure(index)
        else:
            fig = plt.figure(index)
            row = tuple_list[index]
            fig.canvas.set_window_title(row[0])
            plt.plot(row[4], row[2], label=row[0], linewidth=2)
            plt.ylim([0, 100])

            # plt.xticks(rotation=90)

            fig.autofmt_xdate()

            plt.xlabel('Time Recorded')
            plt.ylabel('Price (USD)')

            fig.canvas.mpl_connect('key_release_event', switch_figure_if_left_or_right)
    """

    current_index = 0

    def plot_index(index=current_index):
        nonlocal tuple_list
        row = tuple_list[index]
        plt.gcf().canvas.set_window_title(row[0])
        plt.plot(row[4], row[2], label=row[0], linewidth=2)

    def plot_before_or_after(event):
        nonlocal current_index
        if event.key == 'right':
            current_index = (current_index + 1) % len(tuple_list)
        elif event.key == 'left':
            current_index -= 1
            if current_index < 0:
                current_index = len(tuple_list) + current_index
        plt.clf()
        plot_index(current_index)
        plt.draw()
    # generate_or_get(plt.gcf().number, True)

    plot_index()
    plt.gcf().canvas.mpl_connect('key_release_event', plot_before_or_after)
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