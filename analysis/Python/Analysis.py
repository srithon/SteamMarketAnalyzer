from Trend import *
from enum import Enum

class Action(Enum):
    BUY, SELL, IGNORE = range(3)

def suggested_action(volume, prices):
    if (volume < 8):
        return Action.IGNORE
    else:
        direction = fluctuation(prices)
        if direction == None:
            return Action.IGNORE
        elif direction == Direction.UP:
            return Action.SELL
        else:
            return Action.BUY

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