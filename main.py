import pandas as pd
import matplotlib.pyplot as plt
import calendar

df = pd.read_csv(
    "~/.config/dogg/data/food.csv",
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

unique_months = set(date.strftime("%Y-%m-01") for date in daily_calories.index)
first_day_of_month = pd.to_datetime(list(unique_months))

# Plotting
plt.figure(figsize=(14, 6))
plt.bar(daily_calories.index, daily_calories, color="skyblue", width=0.8)

# Get month names to display on x-axis ticks
month_names = [calendar.month_name[date.month] for date in first_day_of_month]
plt.xticks(first_day_of_month, month_names, rotation=45)

plt.xlabel("Date")
plt.ylabel("Total Calories")
plt.title("Total Calories Consumed (Daily) with Single Tick for Each Month")
plt.tight_layout()
plt.grid()
plt.show()
