
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/household_power_consumption.txt"

COLUMNS = [
    "Date",
    "Time",
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3"
]

def load_data():

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(
        DATA_PATH,
        sep=",",
        header=None,
        names=COLUMNS,
        na_values=["?"],
        low_memory=False
    )

    df["Datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce"
    )

    numeric_columns = COLUMNS[2:]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df.dropna(subset=["Datetime"], inplace=True)
    df.sort_values("Datetime", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df

def analyze_consumption(df):

    # Convert one-minute power readings into energy (kWh)
    df["Energy_kWh"] = df["Global_active_power"] / 60

    # Remove rows with missing power readings for analysis
    valid_data = df.dropna(subset=["Global_active_power"]).copy()

    # Daily consumption
    daily_usage = (
        valid_data.groupby(valid_data["Datetime"].dt.date)["Energy_kWh"]
        .sum()
        .reset_index()
    )

    daily_usage.columns = ["Date", "Daily_Consumption_kWh"]

    # Monthly consumption
    valid_data["Month"] = valid_data["Datetime"].dt.to_period("M")

    monthly_usage = (
        valid_data.groupby("Month")["Energy_kWh"]
        .sum()
        .reset_index()
    )

    monthly_usage["Month"] = monthly_usage["Month"].astype(str)
    monthly_usage.columns = ["Month", "Monthly_Consumption_kWh"]

    # Overall statistics
    total_consumption = valid_data["Energy_kWh"].sum()
    average_power = valid_data["Global_active_power"].mean()
    peak_power = valid_data["Global_active_power"].max()

    # Peak consumption day
    peak_day = daily_usage.loc[
        daily_usage["Daily_Consumption_kWh"].idxmax()
    ]

    # Estimated cost using an example tariff of ₹8 per kWh
    estimated_bill = total_consumption * 8

    # Save results
    os.makedirs("outputs", exist_ok=True)

    daily_usage.to_csv("outputs/daily_usage.csv", index=False)
    monthly_usage.to_csv("outputs/monthly_usage.csv", index=False)

    print("\nELECTRICITY CONSUMPTION ANALYSIS")
    print("-" * 45)
    print(f"Total Consumption: {total_consumption:.2f} kWh")
    print(f"Average Power: {average_power:.2f} kW")
    print(f"Peak Power: {peak_power:.2f} kW")
    print(f"Highest Consumption Day: {peak_day['Date']}")
    print(
        f"Consumption on Peak Day: "
        f"{peak_day['Daily_Consumption_kWh']:.2f} kWh"
    )
    print(f"Estimated Bill (₹8/kWh): ₹{estimated_bill:.2f}")

    print("\nMONTHLY CONSUMPTION:")
    print(monthly_usage.to_string(index=False))

    print("\nDaily and monthly reports saved in outputs folder.")

def create_visualizations(df):

    os.makedirs("outputs", exist_ok=True)

    # Prepare valid consumption data
    valid_data = df.dropna(subset=["Global_active_power"]).copy()

    valid_data["Energy_kWh"] = (
        valid_data["Global_active_power"] / 60
    )

    # Daily consumption
    daily_usage = (
        valid_data.groupby(valid_data["Datetime"].dt.date)["Energy_kWh"]
        .sum()
        .reset_index()
    )

    daily_usage.columns = ["Date", "Consumption"]

    # Monthly consumption
    valid_data["Month"] = valid_data["Datetime"].dt.to_period("M")

    monthly_usage = (
        valid_data.groupby("Month")["Energy_kWh"]
        .sum()
        .reset_index()
    )

    monthly_usage["Month"] = monthly_usage["Month"].astype(str)

    sns.set_theme(style="whitegrid")

    # Graph 1: Daily consumption
    plt.figure(figsize=(14, 6))
    plt.plot(
        daily_usage["Date"],
        daily_usage["Consumption"],
        linewidth=1
    )

    plt.title("Daily Household Electricity Consumption")
    plt.xlabel("Date")
    plt.ylabel("Energy Consumption (kWh)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/daily_consumption.png", dpi=300)
    plt.close()

    # Graph 2: Monthly consumption
    plt.figure(figsize=(14, 6))
    sns.barplot(
        data=monthly_usage,
        x="Month",
        y="Energy_kWh",
        color="steelblue"
    )

    plt.title("Monthly Household Electricity Consumption")
    plt.xlabel("Month")
    plt.ylabel("Energy Consumption (kWh)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("outputs/monthly_consumption.png", dpi=300)
    plt.close()

    print("\nVISUALIZATIONS CREATED SUCCESSFULLY")
    print("1. outputs/daily_consumption.png")
    print("2. outputs/monthly_consumption.png")




if __name__ == "__main__":

    data = load_data()
    analyze_consumption(data)
    create_visualizations(data)

    print("\nDATASET LOADED SUCCESSFULLY")
    print("-" * 40)

    print("Total Records:", len(data))
    print("Total Columns:", len(data.columns))

    print("\nFirst 5 Records:")
    print(data.head())

    print("\nMissing Values:")
    print(data.isnull().sum())

    print("\nDataset Information:")
    print(data.info())
