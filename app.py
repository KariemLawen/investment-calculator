import streamlit as st
import pandas as pd

# Get user input for the annual return and initial investment
annual_return_percent = st.number_input("Enter the annual return as a decimal (e.g., 0.2 for 20%):", value=0.2)
annual_return = annual_return_percent  # Convert the percentage to decimal

initial_investment = st.number_input("Enter the initial investment (e.g., 1500000 for 1.5 million):", value=1500000)

# Initialize variables
x = initial_investment  # User's own money
y = initial_investment  # Borrowed money with 1x margin (same as own money)
total_years = 50  # Calculate for 50 years (1 to 50)

adjusted_equity_results_corrected = {}
no_borrow_equity_results_corrected = {}

# Loop to calculate growth and borrowing for 50 years with the corrected update for x and y
for year in range(1, total_years + 1):
    # Apply the formula using user-defined annual return and subtract 6% interest on borrowed money
    x = x * (1 + annual_return) + y * (annual_return - 0.06)
    
    # Update y directly to x
    y = x
    
    # Store the results for x (user's equity) and y (borrowed money)
    adjusted_equity_results_corrected[year] = x

# Loop to calculate growth without borrowing (just compounding)
for year in range(1, total_years + 1):
    # Compounding growth: (1 + annual_return)^years * initial investment
    no_borrow_equity_results_corrected[year] = initial_investment * (1 + annual_return) ** year

# Prepare the results for cumulative value and yearly gains
comparison_adjusted_results_shekels_corrected = {}

# Calculate for each year and also compute yearly gains
for year in range(1, total_years + 1):
    with_borrow_current_value = int(adjusted_equity_results_corrected[year] - initial_investment)
    without_borrow_current_value = int(no_borrow_equity_results_corrected[year] - initial_investment)
    
    # Calculate the money made in this specific year (difference from previous year)
    if year > 1:
        with_borrow_yearly_gain = with_borrow_current_value - comparison_adjusted_results_shekels_corrected[year - 1]["With Borrowing Raw"]
        without_borrow_yearly_gain = without_borrow_current_value - comparison_adjusted_results_shekels_corrected[year - 1]["Without Borrowing Raw"]
    else:
        with_borrow_yearly_gain = with_borrow_current_value
        without_borrow_yearly_gain = without_borrow_current_value
    
    # Store raw numeric values for the current year to avoid calculation errors
    comparison_adjusted_results_shekels_corrected[year] = {
        "With Borrowing Raw": with_borrow_current_value,
        "Without Borrowing Raw": without_borrow_current_value,
        "With Borrowing (Yearly Profit)": with_borrow_yearly_gain,
        "Without Borrowing (Yearly Profit)": without_borrow_yearly_gain,
        "With Borrowing (Cumulative)": f"{with_borrow_current_value:,}",
        "Without Borrowing (Cumulative)": f"{without_borrow_current_value:,}"
    }

# First Table: Yearly Profit
yearly_profit_data = [
    [year,
     f"{comparison_adjusted_results_shekels_corrected[year]['With Borrowing (Yearly Profit)']:,}",
     f"{comparison_adjusted_results_shekels_corrected[year]['Without Borrowing (Yearly Profit)']:,}"]
    for year in range(1, total_years + 1)
]

# Second Table: Cumulative Values
cumulative_value_data = [
    [year,
     comparison_adjusted_results_shekels_corrected[year]["With Borrowing (Cumulative)"],
     comparison_adjusted_results_shekels_corrected[year]["Without Borrowing (Cumulative)"]]
    for year in range(1, total_years + 1)
]

# Create DataFrames for both tables
df_yearly_profit = pd.DataFrame(yearly_profit_data, columns=["Year", "With Borrowing (Yearly Profit)", "Without Borrowing (Yearly Profit)"])
df_cumulative_value = pd.DataFrame(cumulative_value_data, columns=["Year", "With Borrowing (Cumulative)", "Without Borrowing (Cumulative)"])

# Display both tables in Streamlit
st.write("### Yearly Profit Table")
st.table(df_yearly_profit)

st.write("### Cumulative Value Table")
st.table(df_cumulative_value)
