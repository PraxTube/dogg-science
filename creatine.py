import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar

from const import START_DATE
from utils import moving_average


def daily_creatine(dir_path):
    df = pd.read_csv(
        os.path.join(dir_path, "data/creatine.csv"),
        header=None,
        names=["Timestamp", "Amount"],
    )

    # Convert 'Timestamp' column to datetime with considering timezone
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
    # Extract date from timestamp and create a new 'Date' column
    df["Date"] = df["Timestamp"].dt.tz_convert(None).dt.date
    df = df[df["Date"] >= pd.to_datetime(START_DATE).date()]

    daily_amount = df.groupby("Date")["Amount"].sum()
    return daily_amount


def plot(dir_path):
    daily_amount = daily_creatine(dir_path)
    average = moving_average(daily_amount)

    plt.figure(figsize=(14, 6))
    plt.bar(daily_amount.index, daily_amount, color="skyblue", width=0.8)
    plt.plot(average.index, average, color="red", label="Moving Average", linewidth=3)

    unique_months = set(date.strftime("%Y-%m-01") for date in daily_amount.index)
    first_day_of_month = pd.to_datetime(list(unique_months))
    month_names = [calendar.month_name[date.month] for date in first_day_of_month]
    plt.xticks(first_day_of_month, month_names)

    plt.ylabel("Daily creatine intake")
    plt.title("Rough estimated amount in g")
    plt.tight_layout()
    plt.grid()
    plt.savefig("creatine-plot.svg")
