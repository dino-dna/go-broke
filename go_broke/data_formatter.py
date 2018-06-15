import numpy as np


def format_attributes(data, window, days_in_future):

    slice_start = 0
    slice_stop = window

    input = np.ndarray(shape=(len(data) - days_in_future - window, window))
    label = np.ndarray(shape=(len(data) - days_in_future - window, 1))

    while slice_stop + days_in_future < len(data):
        label[slice_start] = data[slice_stop + days_in_future]
        input[slice_start][:] = data[slice_start:slice_stop]
        slice_start += 1
        slice_stop += 1

    return input, label