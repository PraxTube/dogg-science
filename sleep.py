import os
from datetime import timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar

from const import START_DATE
from utils import moving_average


def convert_to_seconds(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return timedelta(hours=hours, minutes=minutes).seconds / 3600


def y_tick_labels(ticks):
    labels = []
    for tick in ticks:
        if tick >= 0:
            labels.append("{:02d}:00".format(int(tick)))
        else:
            labels.append("{:02d}:00".format(24 + int(tick)))
    return labels


def daily_sleep(dir_path):
    df = pd.read_csv(
        os.path.join(dir_path, "data/sleep.csv"),
        header=None,
        names=[
            "Timestamp",
            "Start",
            "End",
            "Col1",
            "Col2",
            "Col3",
            "Col4",
            "Sleep",
            "Dream",
        ],
    )

    # Convert 'Timestamp' column to datetime with considering timezone
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
    # Extract date from timestamp and create a new 'Date' column
    df["Date"] = df["Timestamp"].dt.tz_convert(None).dt.date
    df = df[df["Date"] >= pd.to_datetime(START_DATE).date()]

    df["Start"] = df["Start"].apply(convert_to_seconds)
    df["End"] = df["End"].apply(convert_to_seconds)

    df["Duration"] = (df["End"] - df["Start"]).abs()
    mask = df["End"] < df["Start"]
    df["Duration"] = np.where(mask, df["End"] + (24 - df["Start"]), df["Duration"])
    df = df[df["Duration"] > 4]

    return df


def plot(dir_path):
    df = daily_sleep(dir_path)
    # average = moving_average(daily_amount)

    fig, ax = plt.subplots()

    unique_months = set(date.strftime("%Y-%m-01") for date in df["Date"])
    first_day_of_month = pd.to_datetime(list(unique_months))
    month_names = [calendar.month_name[date.month] for date in first_day_of_month]
    plt.xticks(first_day_of_month, month_names)

    bottom_min = 25
    top_max = -25
    for index, row in df.iterrows():
        if row["Start"] > row["End"]:
            bottom = -24 + row["Start"]
            top = row["End"] - bottom
        else:
            bottom = row["Start"]
            top = row["End"]

        if bottom < bottom_min:
            bottom_min = bottom
        if top > top_max:
            top_max = top

        ax.bar(
            row["Date"],
            top,
            bottom=bottom,
            width=0.8,
            align="center",
            color="orange",
        )

    y_ticks = np.arange(bottom_min, top_max, step=1)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels(y_ticks))
    plt.ylim(bottom_min, top_max)

    plt.ylabel("Hour of day")
    plt.title("Daily sleep")
    plt.tight_layout()
    plt.grid()
    plt.savefig("sleep-plot.svg")


if __name__ == "__main__":
    plot("~/.config/dogg")
