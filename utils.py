import pandas as pd


def moving_average(data):
    print(data)
    complete_date_range = pd.date_range(start=data.index.min(), end=data.index.max())
    data = data.reindex(complete_date_range, fill_value=0)

    cumulative_sum = data.cumsum()
    moving_average = cumulative_sum / range(1, len(cumulative_sum) + 1)
    return moving_average


def format_time(hours):
    total_seconds = int(hours * 3600)
    if hours < 0:
        total_seconds = int((24 + hours) * 3600)

    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    time_format = "{:02d}:{:02d}".format(hours, minutes)
    return time_format
