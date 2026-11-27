# Household Electricity Consumption Analysis

## Project Overview

Household Electricity Consumption Analysis is a Python-based data analytics project that analyzes household electricity usage using historical power consumption data.

The project processes electricity readings, identifies consumption patterns, generates visualizations, and provides an interactive Streamlit dashboard.

## Objectives

- Analyze household electricity consumption.
- Calculate daily and monthly energy usage.
- Identify peak electricity consumption periods.
- Study hourly consumption patterns.
- Analyze household sub-metering values.
- Estimate electricity costs using a user-defined tariff.
- Generate downloadable consumption reports.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

## Dataset

**Dataset:** Household Power Consumption

The dataset contains electricity measurements recorded at one-minute intervals from December 2006 to November 2010.

The original dataset contains measurements such as:

- Date and Time
- Global Active Power
- Global Reactive Power
- Voltage
- Global Intensity
- Sub Metering 1
- Sub Metering 2
- Sub Metering 3

Dataset source: https://www.kaggle.com/datasets/uciml/electric-power-consumption-data-set

## Project Structure

```text
Household-Electricity-Consumption-Analysis/
│
├── data/
│   └── household_power_consumption.txt
│
├── outputs/
│   ├── daily_usage.csv
│   ├── monthly_usage.csv
│   ├── daily_consumption.png
│   └── monthly_consumption.png
│
├── screenshots/
│
├── app.py
├── analysis.py
├── requirements.txt
└── README.md
```

## Features

1. Dataset loading and preprocessing.
2. Missing-value handling.
3. Daily electricity consumption analysis.
4. Monthly electricity consumption analysis.
5. Hourly electricity consumption visualization.
6. Household sub-metering analysis.
7. Electricity bill estimation.
8. Interactive dashboard.
9. CSV report download.

## Installation

Clone the repository:

```bash
git clone https://github.com/jampaniprathyusha12-creator/Household-Electricity-Consumption-Analysis.git
```

Move into the project folder:

```bash
cd Household-Electricity-Consumption-Analysis
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the downloaded dataset inside the `data` folder.

## Run the Analysis

```bash
python analysis.py
```

## Run the Dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Limitations

- Electricity costs are estimates based on the selected tariff.
- The dataset represents historical household electricity usage.
- Sub-metering values represent measured household areas, not exact individual appliance consumption.
- The project focuses on descriptive analysis rather than future consumption prediction.

## Future Improvements

- Electricity consumption forecasting using Machine Learning.
- Anomaly detection for unusual electricity usage.
- Personalized energy-saving recommendations.
- Comparison of consumption across different periods.
- More detailed interactive visualizations.

## Conclusion

This project demonstrates how Python-based data analytics can transform raw electricity measurements into meaningful consumption insights. The interactive dashboard makes it easier to explore usage patterns, understand household energy consumption, and estimate electricity costs.