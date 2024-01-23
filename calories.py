import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar

from const import START_DATE
from utils import moving_average


def daily_cals(dir_path):
    df = pd.read_csv(
        os.path.join(dir_path, "data/food.csv"),
        header=None,
        names=["Timestamp", "Column1", "Column2", "Meal", "Boolean", "Kcal"],
    )

    # Convert 'Timestamp' column to datetime with considering timezone
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
    # Extract date from timestamp and create a new 'Date' column
    df["Date"] = df["Timestamp"].dt.tz_convert(None).dt.date
    df = df[df["Date"] >= pd.to_datetime(START_DATE).date()]

    daily_calories = df.groupby("Date")["Kcal"].sum()
    return daily_calories


def plot(dir_path):
    daily_calories = daily_cals(dir_path)
    average = moving_average(daily_calories)
    unique_months = set(date.strftime("%Y-%m-01") for date in daily_calories.index)
    first_day_of_month = pd.to_datetime(list(unique_months))

    # Plotting
    plt.figure(figsize=(14, 6))
    plt.bar(daily_calories.index, daily_calories, color="skyblue", width=0.8)

    # Plot the moving average as a line
    plt.plot(average.index, average, color="red", label="Moving Average", linewidth=3)

    # Get month names to display on x-axis ticks
    month_names = [calendar.month_name[date.month] for date in first_day_of_month]
    plt.xticks(first_day_of_month, month_names)

    y_min = np.floor(min(daily_calories) / 500) * 500
    y_max = np.ceil(max(daily_calories) / 500) * 500
    plt.yticks(np.arange(y_min, y_max, step=500))
    plt.ylim(y_min - 100, y_max + 100)

    plt.ylabel("Total Calories in kcal")
    plt.title("Daily calories")
    plt.tight_layout()
    plt.grid()
    plt.savefig("food-plot.svg")
