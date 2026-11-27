
import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Electricity Consumption Analyzer",
    page_icon="⚡",
    layout="wide"
)

COLUMNS = [
    "Date", "Time",
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3"
]

DATA_PATH = "data/household_power_consumption.txt"


@st.cache_data
def load_data():

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
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df.dropna(
        subset=["Datetime", "Global_active_power"],
        inplace=True
    )

    df["Energy_kWh"] = df["Global_active_power"] / 60

    df.sort_values("Datetime", inplace=True)

    return df


# Dashboard heading
st.title("⚡ Household Electricity Consumption Analyzer")

st.write(
    "Analyze household electricity usage, "
    "identify consumption patterns, and estimate electricity costs."
)

st.divider()

# Check dataset
if not os.path.exists(DATA_PATH):
    st.error("Dataset not found. Check the data folder.")
    st.stop()

with st.spinner("Loading electricity consumption dataset..."):
    df = load_data()

# Sidebar
st.sidebar.header("Dashboard Settings")

tariff = st.sidebar.number_input(
    "Electricity rate (₹ per kWh)",
    min_value=0.0,
    value=8.0,
    step=0.5
)

min_date = df["Datetime"].min().date()
max_date = df["Datetime"].max().date()

selected_dates = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_dates) != 2:
    st.info("Please select both a start date and an end date.")
    st.stop()

start_date, end_date = selected_dates

filtered_df = df[
    (df["Datetime"].dt.date >= start_date) &
    (df["Datetime"].dt.date <= end_date)
].copy()

if filtered_df.empty:
    st.warning("No records available for this date range.")
    st.stop()

# Calculate metrics
total_energy = filtered_df["Energy_kWh"].sum()
average_power = filtered_df["Global_active_power"].mean()
peak_power = filtered_df["Global_active_power"].max()
estimated_bill = total_energy * tariff

# Summary metrics
st.subheader("Consumption Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Energy", f"{total_energy:,.2f} kWh")
col2.metric("Average Power", f"{average_power:.2f} kW")
col3.metric("Peak Power", f"{peak_power:.2f} kW")
col4.metric("Estimated Bill", f"₹{estimated_bill:,.2f}")

st.divider()

# Daily consumption
st.subheader("Daily Electricity Consumption")

daily_usage = (
    filtered_df.groupby(filtered_df["Datetime"].dt.date)["Energy_kWh"]
    .sum()
    .reset_index()
)

daily_usage.columns = ["Date", "Consumption (kWh)"]

st.line_chart(
    daily_usage,
    x="Date",
    y="Consumption (kWh)"
)

# Monthly consumption
st.subheader("Monthly Electricity Consumption")

monthly_df = filtered_df.copy()
monthly_df["Month"] = monthly_df["Datetime"].dt.to_period("M").astype(str)

monthly_usage = (
    monthly_df.groupby("Month")["Energy_kWh"]
    .sum()
    .reset_index()
)

monthly_usage.columns = ["Month", "Consumption (kWh)"]

st.bar_chart(
    monthly_usage,
    x="Month",
    y="Consumption (kWh)"
)

# Hourly consumption
st.subheader("Hourly Consumption Pattern")

filtered_df["Hour"] = filtered_df["Datetime"].dt.hour

hourly_usage = (
    filtered_df.groupby("Hour")["Global_active_power"]
    .mean()
    .reset_index()
)

hourly_usage.columns = ["Hour", "Average Power (kW)"]

st.line_chart(
    hourly_usage,
    x="Hour",
    y="Average Power (kW)"
)

# Appliance-wise consumption analysis
st.divider()

st.subheader("Appliance-wise Electricity Consumption")

st.write(
    "Analyze electricity usage across different household areas "
    "using the three sub-metering measurements."
)

appliance_usage = pd.DataFrame({
    "Household Area": [
        "Kitchen",
        "Laundry",
        "Water Heater & AC"
    ],
    "Consumption (kWh)": [
        filtered_df["Sub_metering_1"].sum() / 1000,
        filtered_df["Sub_metering_2"].sum() / 1000,
        filtered_df["Sub_metering_3"].sum() / 1000
    ]
})

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(
        appliance_usage,
        x="Household Area",
        y="Consumption (kWh)"
    )

with col2:
    st.dataframe(
        appliance_usage,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "Sub-metering values are recorded in Wh per minute "
    "and converted into kWh. These categories represent "
    "the dataset's measured household areas."
)


# Detailed data
st.subheader("Electricity Consumption Records")

st.dataframe(
    filtered_df[
        ["Datetime", "Global_active_power",
         "Voltage", "Global_intensity", "Energy_kWh"]
    ].head(100),
    use_container_width=True
)

# Download report
csv_data = daily_usage.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Daily Consumption Report",
    data=csv_data,
    file_name="daily_electricity_report.csv",
    mime="text/csv"
)

st.success("Electricity consumption dashboard loaded successfully!")

st.caption(
    "Note: Electricity cost is an estimate based on the tariff "
    "selected in the sidebar."
)
