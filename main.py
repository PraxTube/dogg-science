import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar


def daily_cals():
    df = pd.read_csv(
        os.path.join(sys.argv[1], "data/food.csv"),
        header=None,
        names=["Timestamp", "Column1", "Column2", "Meal", "Boolean", "Kcal"],
    )

    # Convert 'Timestamp' column to datetime with considering timezone
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
    # Extract date from timestamp and create a new 'Date' column
    df["Date"] = df["Timestamp"].dt.tz_convert(None).dt.date
    # Group by 'Date' and calculate total calories for each day
    raw_daily_calories = df.groupby("Date")["Kcal"].sum()

    # Find the index where the calories are non-zero
    start_index = raw_daily_calories[raw_daily_calories != 0].index[0]
    # Filter the dataset to start from the first non-zero calories
    daily_calories = raw_daily_calories[start_index:]
    return daily_calories


def average_cals():
    cumulative_sum = daily_cals().cumsum()
    moving_average = cumulative_sum / range(1, len(cumulative_sum) + 1)
    return moving_average


def plot():
    daily_calories = daily_cals()
    moving_average = average_cals()
    unique_months = set(date.strftime("%Y-%m-01") for date in daily_calories.index)
    first_day_of_month = pd.to_datetime(list(unique_months))

    # Plotting
    plt.figure(figsize=(14, 6))
    plt.bar(daily_calories.index, daily_calories, color="skyblue", width=0.8)

    # Plot the moving average as a line
    plt.plot(moving_average.index, moving_average, color='red', label='Moving Average', linewidth=3)

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


def main():
    plot()


if __name__ == "__main__":
    main()
