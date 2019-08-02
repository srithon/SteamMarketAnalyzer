from enum import Enum

class Direction(Enum):
    UP, DOWN = range(2)

def weightingInterval(n):
    return 1 / (n + 1)

def weightedAverage(numbers):
    interval = weightingInterval(len(numbers))
    average = 0
    current_interval = 1 - interval
    for num in numbers:
        average += current_interval * num
        # print(f'Current Interval: {current_interval}')
        # print(f'Current Average: {average}')
        current_interval -= interval
    # print(f'Weighted Average: {average}')
    average = average / (len(numbers) / 2.0)
    # print(f'New Average: {average}')
    return average

def percentError(a, b):
    return ((a - b) / b) * 100

def fluctuationFirstToRest(list):
    if len(list) == 1:
        return 0
    return percentError(list[0], weightedAverage(list[1:]))

def fluctuation(list):
    fluc = fluctuationFirstToRest(list)
    return fluctuationDirection(fluc)

def fluctuationDirection(fluc):
    # print(f'Passed in fluctuation: {fluc}')
    if fluc > 15:
        return Direction.UP
    elif fluc < -15:
        return Direction.DOWN
    else:
        return None
