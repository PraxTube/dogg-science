import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

from const import START_DATE


# Function to convert time strings to timedelta
def convert_to_timedelta(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return timedelta(hours=hours, minutes=minutes)


# Read CSV file and extract data using pandas
df = pd.read_csv(
    "~/.config/dogg/data/sleep.csv",
    header=None,
    names=[
        "Timestamp",
        "Start",
        "End",
        "Col1",
        "Col2",
        "Col3",
        "Col4",
        "Activity",
        "Notes",
    ],
)

# Convert date and time columns to datetime objects
df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
# Extract date from timestamp and create a new 'Date' column
df["Date"] = df["Timestamp"].dt.tz_convert(None).dt.date
df = df[df["Date"] >= pd.to_datetime(START_DATE).date()]
df["Start"] = df["Start"].apply(convert_to_timedelta)
df["End"] = df["End"].apply(convert_to_timedelta)

# Calculate sleep durations
df["Duration"] = abs((df["End"].dt.seconds() - df["Start"].dt.seconds())) / 3600
print(df["Duration"])
print(df["Duration"] > 4)
df = df[df["Duration"] > 4]
print(df)

# Plotting
fig, ax = plt.subplots()

for index, row in df.iterrows():
    if row["Start"] > row["End"]:
        bottom = -(timedelta(hours=24) - row["Start"]).seconds / 3600
        top = row["End"].seconds / 3600 - bottom

        ax.bar(
            row["Date"],
            top,
            bottom=bottom,
            width=0.8,
            align="center",
            color="blue",
        )
    else:
        ax.bar(
            row["Date"],
            row["Duration"],
            bottom=row["Start"].seconds / 3600,
            width=0.8,
            align="center",
            color="orange",
        )

y_min = min(df["Start"]).seconds
print(y_min)
# y_max = np.ceil(max(daily_calories) / 500) * 500
# ax.yticks(np.arange(y_min, y_max, step=500))
# ax.ylim(y_min - 100, y_max + 100)
ax.set_ylabel("Hours of Sleep")
ax.set_title("Duration Over Time")

plt.show()
