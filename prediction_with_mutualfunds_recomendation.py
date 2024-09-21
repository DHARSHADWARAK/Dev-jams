import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
import os
from matplotlib.ticker import FuncFormatter

# Suppress SettingWithCopyWarning
pd.options.mode.chained_assignment = None  # default='warn'

def load_data(file_path, date_col='date', balance_col='closing_balance'):
    """
    Load and preprocess the Excel data.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist in the current directory.")
        exit()

    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        exit()

    # Check if required columns exist
    if date_col not in df.columns or balance_col not in df.columns:
        print(f"Error: The Excel file must contain '{date_col}' and '{balance_col}' columns.")
        exit()

    # Attempt to convert date column to datetime with multiple formats
    date_formats = ['%Y-%m-%d', '%d/%m/%y', '%d/%m/%Y']  # Add more formats if necessary
    for fmt in date_formats:
        try:
            df[date_col] = pd.to_datetime(df[date_col], format=fmt, dayfirst=True)
            print(f"Date conversion successful using format: {fmt}")
            break
        except (ValueError, TypeError):
            continue
    else:
        # If none of the formats match, try inferring the format
        try:
            df[date_col] = pd.to_datetime(df[date_col], infer_datetime_format=True, dayfirst=True)
            print("Date conversion successful using inferred format.")
        except Exception as e:
            print(f"Error converting '{date_col}' to datetime with inferred format: {e}")
            exit()

    return df

def check_negative_balances(df, balance_col='closing_balance'):
    """
    Check for negative closing balances and warn the user.
    """
    negative_balances = df[df[balance_col] < 0]
    if not negative_balances.empty:
        print("\nWarning: There are negative closing balance entries in the data:")
        print(negative_balances)
    else:
        print("\nAll closing balance entries are non-negative.")

def aggregate_monthly_last(df, date_col='date', balance_col='closing_balance'):
    """
    Aggregate daily data to get the last closing balance of each month.
    """
    df['year_month'] = df[date_col].dt.to_period('M')
    monthly_last = df.groupby('year_month')[balance_col].last().reset_index()
    monthly_last['year_month'] = monthly_last['year_month'].dt.to_timestamp()
    return monthly_last

def aggregate_monthly_average(df, date_col='date', balance_col='closing_balance'):
    """
    Aggregate daily data to get the average closing balance of each month.
    """
    df['year_month'] = df[date_col].dt.to_period('M')
    monthly_avg = df.groupby('year_month')[balance_col].mean().reset_index()
    monthly_avg['year_month'] = monthly_avg['year_month'].dt.to_timestamp()
    return monthly_avg

def prepare_prophet_df(monthly_df, balance_col='closing_balance'):
    """
    Prepare the DataFrame for Prophet forecasting.
    """
    prophet_df = monthly_df.rename(columns={'year_month': 'ds', balance_col: 'y'})
    return prophet_df[['ds', 'y']]

def train_prophet_model(prophet_df):
    """
    Train the Prophet model.
    """
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode='additive',
        changepoint_prior_scale=0.1  # Increased flexibility for trend changes
    )
    model.fit(prophet_df)
    return model

def forecast_min_balance(model, periods=36):
    """
    Forecast closing balance for the next 'periods' months.
    """
    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)
    return forecast

def format_indian_currency(amount):
    """
    Format numbers into Indian currency format.
    """
    if amount >= 1e7:
        return f"{amount / 1e7:.2f}Cr"
    elif amount >= 1e5:
        return f"{amount / 1e5:.2f}L"
    elif amount >= 1e3:
        return f"{amount / 1e3:.2f}K"
    else:
        return f"₹{amount:.2f}"

def plot_forecast(monthly_df, forecast, title='Closing Balance Forecast'):
    """
    Plot the historical and forecasted closing balances.
    """
    # Apply floor to ensure non-negative values
    forecast['yhat'] = forecast['yhat'].apply(lambda x: max(x, 0))
    forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x: max(x, 0))
    forecast['yhat_upper'] = forecast['yhat_upper'].apply(lambda x: max(x, 0))

    plt.figure(figsize=(14, 7))
    plt.plot(monthly_df['year_month'], monthly_df['closing_balance'], label='Historical Closing Balance', color='blue')
    plt.plot(forecast['ds'], forecast['yhat'], label='Forecasted Closing Balance', color='red')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='pink', alpha=0.3, label='Confidence Interval')
    plt.xlabel('Date')
    plt.ylabel('Closing Balance (INR)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Define formatter for y-axis
    def indian_currency_formatter(x, pos):
        return format_indian_currency(x)

    plt.gca().yaxis.set_major_formatter(FuncFormatter(indian_currency_formatter))

    plt.show()

def display_forecast(forecast, periods=36):
    """
    Display the forecasted closing balances in a readable format.
    """
    forecast_future = forecast.tail(periods)
    # Apply floor to ensure non-negative values
    forecast_future['yhat'] = forecast_future['yhat'].apply(lambda x: max(x, 0))
    forecast_future['yhat_lower'] = forecast_future['yhat_lower'].apply(lambda x: max(x, 0))
    forecast_future['yhat_upper'] = forecast_future['yhat_upper'].apply(lambda x: max(x, 0))

    display_df = forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    display_df = display_df.rename(columns={
        'ds': 'Date',
        'yhat': 'Predicted_Closing_Balance',
        'yhat_lower': 'Lower_Confidence_Interval',
        'yhat_upper': 'Upper_Confidence_Interval'
    })
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m')

    # Apply formatting for display only
    display_df['Predicted_Closing_Balance'] = display_df['Predicted_Closing_Balance'].apply(format_indian_currency)
    display_df['Lower_Confidence_Interval'] = display_df['Lower_Confidence_Interval'].apply(format_indian_currency)
    display_df['Upper_Confidence_Interval'] = display_df['Upper_Confidence_Interval'].apply(format_indian_currency)

    print("\nPredicted Closing Balances for the Next 3 Years (Monthly):")
    print(display_df.to_string(index=False))

def save_forecast_to_excel(forecast, periods=36, output_file='forecast_closing_balance.xlsx'):
    """
    Save the forecasted closing balances to an Excel file.
    """
    forecast_future = forecast.tail(periods)
    save_df = forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    save_df = save_df.rename(columns={
        'ds': 'Date',
        'yhat': 'Predicted_Closing_Balance',
        'yhat_lower': 'Lower_Confidence_Interval',
        'yhat_upper': 'Upper_Confidence_Interval'
    })
    save_df['Date'] = save_df['Date'].dt.strftime('%Y-%m')

    # Save to Excel without formatting
    try:
        save_df.to_excel(output_file, index=False)
        print(f"\nForecast successfully saved to '{output_file}'.")
    except Exception as e:
        print(f"Error saving forecast to Excel: {e}")

def visualize_aggregated_data(monthly_df):
    """
    Plot the historical monthly closing balances.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_df['year_month'], monthly_df['closing_balance'], marker='o', linestyle='-')
    plt.title('Historical Monthly Closing Balances')
    plt.xlabel('Date')
    plt.ylabel('Closing Balance (INR)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def remove_outliers(monthly_df, balance_col='closing_balance', lower_quantile=0.01, upper_quantile=0.99):
    """
    Remove outliers from the monthly closing balance data.
    """
    lower = monthly_df[balance_col].quantile(lower_quantile)
    upper = monthly_df[balance_col].quantile(upper_quantile)
    filtered_df = monthly_df[(monthly_df[balance_col] >= lower) & (monthly_df[balance_col] <= upper)]
    return filtered_df

def calculate_average_monthly_expense(df, date_col='date', withdrawal_col='withdrawal_amt'):
    """
    Calculate the average monthly expense based on withdrawal amounts.
    """
    df['year_month'] = df[date_col].dt.to_period('M')
    monthly_expense = df.groupby('year_month')[withdrawal_col].sum().reset_index()
    average_expense = monthly_expense['withdrawal_amt'].mean()
    return average_expense

def determine_investable_amount(current_balance, average_expense):
    """
    Determine the amount available for investment.
    Investable Amount = Current Balance - (Average Expense + 10% of Average Expense)
    """
    investable = current_balance - (average_expense + 0.10 * average_expense)
    investable = max(investable, 0)  # Ensure non-negative
    return investable

def get_user_age():
    """
    Prompt the user to input their age and validate it.
    """
    while True:
        try:
            age = int(input("\nEnter your age: ").strip())
            if age < 0:
                print("Age cannot be negative. Please enter a valid age.")
                continue
            return age
        except ValueError:
            print("Invalid input. Please enter a numeric age.")

def get_investment_strategy(age):
    """
    Determine risk tolerance and investment percentages based on age.
    """
    if 20 <= age < 30:
        risk_tolerance = 'High'
        investment_percent = 0.10  # 10-15% of salary; we'll take 12.5%
    elif 30 <= age < 40:
        risk_tolerance = 'Moderate-High'
        investment_percent = 0.175  # 15-20%; take average 17.5%
    elif 40 <= age < 50:
        risk_tolerance = 'Moderate'
        investment_percent = 0.225  # 20-25%; take average 22.5%
    elif 50 <= age < 60:
        risk_tolerance = 'Low-Moderate'
        investment_percent = 0.275  # 25-30%; take average 27.5%
    else:
        risk_tolerance = 'Low'
        investment_percent = 0.225  # 20-25%; take average 22.5%
    
    return risk_tolerance, investment_percent

def get_risk_allocation(risk_tolerance):
    """
    Allocate investment percentages based on risk tolerance.
    """
    if risk_tolerance == 'High':
        return {'Equities': 0.75, 'Debt': 0.25}
    elif risk_tolerance == 'Moderate-High':
        return {'Equities': 0.65, 'Debt': 0.35}
    elif risk_tolerance == 'Moderate':
        return {'Equities': 0.55, 'Debt': 0.45}
    elif risk_tolerance == 'Low-Moderate':
        return {'Equities': 0.40, 'Debt': 0.60}
    else:  # Low
        return {'Equities': 0.20, 'Debt': 0.80}

def load_mutual_funds(file_path):
    """
    Load mutual funds data from an Excel file with three sheets: High, Medium, Low risk.
    """
    if not os.path.exists(file_path):
        print(f"\nError: The mutual funds file '{file_path}' does not exist.")
        return None
    
    try:
        mutual_funds = pd.read_excel(file_path, sheet_name=['High Risk', 'Medium Risk', 'Low Risk'], engine='openpyxl')
        print("\nMutual funds data loaded successfully.")
        return mutual_funds
    except Exception as e:
        print(f"\nError reading the mutual funds Excel file: {e}")
        return None

def suggest_mutual_fund(risk_category):
    """
    Suggest mutual funds based on the risk category.
    """
    # Hardcoded data for each risk category
    funds_data = {
        'High': [
            {'Fund Name': 'Fund A (High Risk Category)', '1-Year Return': 12.3, '3-Year Return (Annualized)': 8.5, '5-Year Return (Annualized)': 10.7, 'Max (Since Inception)': 15.2},
            {'Fund Name': 'Fund B (High Risk Category)', '1-Year Return': 15.6, '3-Year Return (Annualized)': 10.3, '5-Year Return (Annualized)': 12.8, 'Max (Since Inception)': 17.5},
            {'Fund Name': 'Fund C (High Risk Category)', '1-Year Return': 18.2, '3-Year Return (Annualized)': 12.1, '5-Year Return (Annualized)': 14.5, 'Max (Since Inception)': 19.3},
            {'Fund Name': 'Fund D (High Risk Category)', '1-Year Return': 20.1, '3-Year Return (Annualized)': 15.0, '5-Year Return (Annualized)': 16.2, 'Max (Since Inception)': 21.4},
            {'Fund Name': 'Fund E (High Risk Category)', '1-Year Return': 22.0, '3-Year Return (Annualized)': 17.2, '5-Year Return (Annualized)': 18.3, 'Max (Since Inception)': 23.6},
        ],
        'Medium': [
            {'Fund Name': 'Fund A (Medium Risk Category)', '1-Year Return': 8.5, '3-Year Return (Annualized)': 6.3, '5-Year Return (Annualized)': 7.2, 'Max (Since Inception)': 10.0},
            {'Fund Name': 'Fund B (Medium Risk Category)', '1-Year Return': 10.2, '3-Year Return (Annualized)': 8.0, '5-Year Return (Annualized)': 9.0, 'Max (Since Inception)': 12.3},
            {'Fund Name': 'Fund C (Medium Risk Category)', '1-Year Return': 12.1, '3-Year Return (Annualized)': 9.5, '5-Year Return (Annualized)': 10.3, 'Max (Since Inception)': 14.2},
            {'Fund Name': 'Fund D (Medium Risk Category)', '1-Year Return': 14.0, '3-Year Return (Annualized)': 11.2, '5-Year Return (Annualized)': 12.4, 'Max (Since Inception)': 16.0},
            {'Fund Name': 'Fund E (Medium Risk Category)', '1-Year Return': 15.8, '3-Year Return (Annualized)': 13.0, '5-Year Return (Annualized)': 14.5, 'Max (Since Inception)': 18.0},
        ],
        'Low': [
            {'Fund Name': 'Fund A (Low Risk Category)', '1-Year Return': 5.3, '3-Year Return (Annualized)': 4.0, '5-Year Return (Annualized)': 5.2, 'Max (Since Inception)': 6.5},
            {'Fund Name': 'Fund B (Low Risk Category)', '1-Year Return': 6.1, '3-Year Return (Annualized)': 5.3, '5-Year Return (Annualized)': 6.1, 'Max (Since Inception)': 7.5},
            {'Fund Name': 'Fund C (Low Risk Category)', '1-Year Return': 7.0, '3-Year Return (Annualized)': 6.2, '5-Year Return (Annualized)': 7.0, 'Max (Since Inception)': 8.3},
            {'Fund Name': 'Fund D (Low Risk Category)', '1-Year Return': 7.8, '3-Year Return (Annualized)': 7.0, '5-Year Return (Annualized)': 7.8, 'Max (Since Inception)': 9.5},
            {'Fund Name': 'Fund E (Low Risk Category)', '1-Year Return': 8.5, '3-Year Return (Annualized)': 7.8, '5-Year Return (Annualized)': 8.6, 'Max (Since Inception)': 10.5},
        ]
    }
    
    # Validate the risk category input
    risk_category = risk_category.capitalize()
    if risk_category not in funds_data:
        print("Invalid risk category. Please choose from High, Medium, or Low.")
        return None
    
    # Convert the suggested funds to a DataFrame and return
    suggested_funds = pd.DataFrame(funds_data[risk_category])
    return suggested_funds


def create_investment_plan(age, investable_amount, mutual_funds):
    """
    Create a tailored investment plan based on age and investable amount.
    """
    risk_tolerance, investment_percent = get_investment_strategy(age)
    allocation = get_risk_allocation(risk_tolerance)
    
    total_investment = investable_amount * investment_percent
    equity_investment = total_investment * allocation['Equities']
    debt_investment = total_investment * allocation['Debt']
    
    print(f"\n=== Investment Strategy ===")
    print(f"Age: {age}")
    print(f"Risk Tolerance: {risk_tolerance}")
    print(f"Total Investable Amount: {format_indian_currency(total_investment)}")
    print(f"Equities Allocation ({allocation['Equities']*100}%): {format_indian_currency(equity_investment)}")
    print(f"Debt Allocation ({allocation['Debt']*100}%): {format_indian_currency(debt_investment)}")
    
    # Suggest Mutual Funds
    print("\n=== Suggested Mutual Funds ===")
    # Equities - High Risk
    print("\n-- Equities (High Risk) --")
    equity_funds = suggest_mutual_fund('High')
    if equity_funds is not None:
        print(equity_funds[['Fund Name', '1-Year Return', '3-Year Return (Annualized)', '5-Year Return (Annualized)', 'Max (Since Inception)']].to_string(index=False))
    
    # Debt - Low Risk
    print("\n-- Debt (Low Risk) --")
    debt_funds = suggest_mutual_fund('Low')
    if debt_funds is not None:
        print(debt_funds[['Fund Name', '1-Year Return', '3-Year Return (Annualized)', '5-Year Return (Annualized)', 'Max (Since Inception)']].to_string(index=False))

def main():
    # Step 1: Load the Data
    file_path = 'Financial_expenses_synthetic.xlsx'  # Change if necessary
    date_column = 'date'
    balance_column = 'closing_balance'
    withdrawal_column = 'withdrawal_amt'

    df = load_data(file_path, date_col=date_column, balance_col=balance_column)

    # Step 2: Check for Negative Balances
    check_negative_balances(df, balance_col=balance_column)

    # Step 3: Aggregate Daily Data to Monthly Data
    monthly_df = aggregate_monthly_last(df, date_col=date_column, balance_col=balance_column)
    # Alternatively, use aggregate_monthly_average if preferred

    # Step 4: Remove Outliers (Optional but Recommended)
    monthly_df = remove_outliers(monthly_df, balance_col='closing_balance')

    # Step 5: Visualize Aggregated Data
    visualize_aggregated_data(monthly_df)

    # Step 6: Prepare Data for Prophet
    prophet_df = prepare_prophet_df(monthly_df, balance_col='closing_balance')

    # Step 7: Train the Prophet Model
    model = train_prophet_model(prophet_df)

    # Step 8: Forecast Closing Balance for Next 36 Months
    forecast = forecast_min_balance(model, periods=36)

    # Step 9: Display the Forecasted Values
    display_forecast(forecast, periods=36)

    # Step 10: Save the Forecasted Values to Excel
    save_forecast_to_excel(forecast, periods=36, output_file='forecast_closing_balance.xlsx')

    # Step 11: Plot the Forecast
    plot_forecast(monthly_df, forecast, title='Closing Balance Forecast for Next 3 Years')

    average_expense = calculate_average_monthly_expense(df, date_col=date_column, withdrawal_col=withdrawal_column)
    print(f"\nAverage Monthly Expense: {format_indian_currency(average_expense)}")

    # Step 13: Determine Current Balance from the Latest Forecast
    current_balance = forecast.iloc[-1]['yhat']  # Latest predicted closing balance
    print(f"Current (Forecasted) Closing Balance: {format_indian_currency(current_balance)}")

    # Step 14: Determine Investable Amount
    investable_amount = determine_investable_amount(current_balance, average_expense)
    print(f"Investable Amount: {format_indian_currency(investable_amount)}")

    if investable_amount <= 0:
        print("No investable amount available based on the current balance and expenses.")
        return

    # Step 15: Get User's Age
    age = get_user_age()

    # Step 16: Load Mutual Funds Data
    mutual_funds_file = '/content/Mutual_Funds_Performance.xlsx'  # Change if necessary
    mutual_funds = load_mutual_funds(mutual_funds_file)
    if mutual_funds is None:
        print("Cannot proceed without mutual funds data.")
        return

    # Step 17: Create Investment Plan
    create_investment_plan(age, investable_amount, mutual_funds)

if __name__ == "__main__":
    main()
