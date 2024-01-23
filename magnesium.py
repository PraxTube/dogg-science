import os

import pandas as pd
import matplotlib.pyplot as plt
import calendar

from const import START_DATE
from utils import moving_average


def magnesium_pills(dir_path):
    df = pd.read_csv(
        os.path.join(dir_path, "data/magnesium.csv"),
        header=None,
        names=["Timestamp", "Pills"],
    )

    # Convert 'Timestamp' column to datetime with considering timezone
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
    # Extract date from timestamp and create a new 'Date' column
    df["Date"] = df["Timestamp"].dt.tz_convert(None).dt.date
    df = df[df["Date"] >= pd.to_datetime(START_DATE).date()]

    pills = df.groupby("Date")["Pills"].sum()
    return pills


def plot(dir_path):
    pills = magnesium_pills(dir_path)
    average = moving_average(pills)
    unique_months = set(date.strftime("%Y-%m-01") for date in pills.index)
    first_day_of_month = pd.to_datetime(list(unique_months))

    # Plotting
    plt.figure(figsize=(14, 6))
    plt.bar(pills.index, pills, color="skyblue", width=0.8)

    # Plot the moving average as a line
    plt.plot(average.index, average, color="red", label="Moving Average", linewidth=3)

    # Get month names to display on x-axis ticks
    month_names = [calendar.month_name[date.month] for date in first_day_of_month]
    plt.xticks(first_day_of_month, month_names)

    plt.ylabel("Number of 120mg Magnesiumglycinat pills")
    plt.title(
        "Daily magnesium pill intake\nNOTE, some pills (around January) are actually\n150mg Magnesiumcitrat, I didn't notice that"
    )
    plt.tight_layout()
    plt.grid()
    plt.savefig("magnesium-plot.svg")
