def moving_average(data):
    cumulative_sum = data.cumsum()
    moving_average = cumulative_sum / range(1, len(cumulative_sum) + 1)
    return moving_average
