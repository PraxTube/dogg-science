import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar

from utils import moving_average


START_DATE = "2023-11-01"


def daily_eat_counts(dir_path):
    df = pd.read_csv(
        os.path.join(dir_path, "data/food.csv"),
        header=None,
        names=["Timestamp", "Column1", "Column2", "Meal", "Boolean", "Kcal"],
    )

    # Convert 'Timestamp' column to datetime with considering timezone
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
    # Extract date from timestamp and create a new 'Date' column
    df["Date"] = df["Timestamp"].dt.tz_convert(None).dt.date
    # Group by 'Date' and calculate total calories for each day
    df = df[df["Date"] >= pd.to_datetime(START_DATE).date()]
    daily_eating_counts = df.groupby("Date").size()
    return daily_eating_counts


def plot(dir_path):
    daily_counts = daily_eat_counts(dir_path)
    average = moving_average(daily_counts)
    unique_months = set(date.strftime("%Y-%m-01") for date in daily_counts.index)
    first_day_of_month = pd.to_datetime(list(unique_months))

    # Plotting
    plt.figure(figsize=(14, 6))
    plt.bar(daily_counts.index, daily_counts, color="skyblue", width=0.8)

    # Plot the moving average as a line
    plt.plot(average.index, average, color='red', label='Moving Average', linewidth=3)

    # Get month names to display on x-axis ticks
    month_names = [calendar.month_name[date.month] for date in first_day_of_month]
    plt.xticks(first_day_of_month, month_names)

    plt.ylabel("Number of times eaten a day")
    plt.title("Daily eating counts")
    plt.tight_layout()
    plt.grid()
    plt.savefig("eat-counts-plot.svg")
