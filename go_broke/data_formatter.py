import numpy as np


def format_attributes(data, window, days_in_future):

    slice_start = 0
    slice_stop = window

    prices = np.ndarray(shape=(len(data) - days_in_future - window, window))
    future_prices = np.ndarray(shape=(len(data) - days_in_future - window, 1))

    while slice_stop + days_in_future < len(data):
        future_prices[slice_start] = data[slice_stop + days_in_future]
        prices[slice_start][:] = data[slice_start:slice_stop]
        slice_start += 1
        slice_stop += 1

    return prices, future_prices
