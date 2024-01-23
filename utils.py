import pandas as pd


def moving_average(data):
    complete_date_range = pd.date_range(start=data.index.min(), end=data.index.max())
    data = data.reindex(complete_date_range, fill_value=0)

    cumulative_sum = data.cumsum()
    moving_average = cumulative_sum / range(1, len(cumulative_sum) + 1)
    return moving_average
