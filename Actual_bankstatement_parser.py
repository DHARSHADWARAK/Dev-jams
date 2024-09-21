import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Read the Excel file without headers
df_raw = pd.read_excel('updated_transactions.xlsx', header=None)

# Function to extract header information
def extract_header_info(df):
    header_info = {}
    for index, row in df.iterrows():
        line = ' '.join(map(str, row.dropna()))
        if 'Statement From' in line:
            match = re.search(r'Statement From\s*:\s*(.*?)\s*To\s*:\s*(.*)', line)
            if match:
                header_info['Statement Period'] = {'From': match.group(1), 'To': match.group(2)}
        elif 'Account No' in line:
            match = re.search(r'Account No\s*:\s*(\d+)', line)
            if match:
                header_info['Account Number'] = match.group(1)
        elif 'Email' in line:
            match = re.search(r'Email\s*:\s*(.*)', line)
            if match:
                header_info['Email'] = match.group(1).strip()
        elif 'MR' in line or 'MRS' in line or 'MS' in line:
            name_match = re.search(r'(MR|MRS|MS)\s*(.*)', line)
            if name_match:
                header_info['Name'] = name_match.group(2).strip()
        elif 'Cust ID' in line:
            match = re.search(r'Cust ID\s*:\s*(\d+)', line)
            if match:
                header_info['Customer ID'] = match.group(1)
    return header_info

# Extract header information
header_info = extract_header_info(df_raw.head(15))
print("Extracted Header Information:")
for key, value in header_info.items():
    print(f"{key}: {value}")

# Function to find transaction data indices
def find_transaction_data_indices(df):
    transaction_start_idx = None
    transaction_end_idx = None
    for i in range(len(df)):
        row_values = df.iloc[i].astype(str).str.lower()
        if 'date' in row_values.values and 'narration' in row_values.values:
            transaction_start_idx = i + 1
        elif 'statement summary' in ' '.join(row_values):
            transaction_end_idx = i - 1
            break
    return transaction_start_idx, transaction_end_idx

# Find indices for transaction data
start_idx, end_idx = find_transaction_data_indices(df_raw)
print(f"Transaction data starts at row {start_idx}, ends at row {end_idx}")

# Extract transaction data
df = df_raw.iloc[start_idx:end_idx].reset_index(drop=True)

# Set the correct headers
df.columns = ['Date', 'Value Dt', 'Narration', 'Chq/Ref Number', 'Withdrawal Amt', 'Deposit Amt', 'Closing Balance']

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '')

# Convert 'withdrawal_amt' and 'deposit_amt' to numeric
df['withdrawal_amt'] = pd.to_numeric(df['withdrawal_amt'], errors='coerce').fillna(0)
df['deposit_amt'] = pd.to_numeric(df['deposit_amt'], errors='coerce').fillna(0)

# Function to calculate the amount as positive values
def calculate_amount(row):
    if row['withdrawal_amt'] > 0:
        return row['withdrawal_amt']
    elif row['deposit_amt'] > 0:
        return row['deposit_amt']
    else:
        return 0

# Function to determine transaction type
def calculate_transaction_type(row):
    if row['withdrawal_amt'] > 0:
        return 'withdrawal'
    elif row['deposit_amt'] > 0:
        return 'deposit'
    else:
        return 'unknown'

# Apply the functions
df['amount'] = df.apply(calculate_amount, axis=1)
df['transaction_type'] = df.apply(calculate_transaction_type, axis=1)

# Convert date columns to datetime
df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

# Clean narration text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['narration_clean'] = df['narration'].apply(clean_text)

# Define categories and keywords
categories = {
    'transfer': ['upi', 'imps', 'neft', 'rtgs', 'ib billpay', 'billpay'],
    'salary': ['salary', 'payroll', 'credit'],
    'shopping': ['amazon', 'flipkart', 'myntra', 'shopping', 'ecommerce', 'paytm'],
    'food': ['swiggy', 'zomato', 'food', 'restaurant', 'cafe', 'luluinternationalsho', 'bakery', 'gpay'],
    'entertainment': ['netflix', 'youtube', 'spotify', 'entertainment'],
    'utilities': ['electricity', 'water', 'gas', 'bill', 'recharge'],
    'fuel': ['petrol', 'diesel', 'fuel', 'hpcl', 'bpcl'],
    'others': []
}

# Function to categorize transactions
def categorize_transaction(narration):
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in narration:
                return category
    return 'others'

df['category'] = df['narration_clean'].apply(categorize_transaction)

# Identify uncategorized transactions
uncategorized = df[df['category'] == 'others']
print("Uncategorized Transactions:")
print(uncategorized['narration'].unique())

# Calculate total expenditure and income
total_expenditure = df[df['transaction_type'] == 'withdrawal']['amount'].sum()
total_income = df[df['transaction_type'] == 'deposit']['amount'].sum()

print(f"Total Expenditure: {total_expenditure}")
print(f"Total Income: {total_income}")

# Calculate spending by category (for withdrawals only)
category_spending = df[df['transaction_type'] == 'withdrawal'].groupby('category')['amount'].sum()
print("Spending by Category:")
print(category_spending)

# Plot spending by category
category_spending.plot(kind='bar')
plt.title('Spending by Category')
plt.xlabel('Category')
plt.ylabel('Total Amount')
plt.show()

# Add a 'month_year' column
df['month_year'] = df['date'].dt.to_period('M')

# Calculate monthly spending (for withdrawals only)
monthly_spending = df[df['transaction_type'] == 'withdrawal'].groupby('month_year')['amount'].sum()

# Plot monthly spending over time
monthly_spending.plot(kind='line', marker='o')
plt.title('Monthly Spending Over Time')
plt.xlabel('Month-Year')
plt.ylabel('Total Amount')
plt.show()

# Calculate average daily spending per month
# First, get daily spending
daily_spending = df[df['transaction_type'] == 'withdrawal'].groupby('date')['amount'].sum().reset_index()

# Add 'month_year' to daily_spending
daily_spending['month_year'] = daily_spending['date'].dt.to_period('M')

# Calculate average daily spending per month
avg_daily_spending_per_month = daily_spending.groupby('month_year')['amount'].mean()

print("Average Daily Spending per Month:")
print(avg_daily_spending_per_month)

# Plot average daily spending per month
avg_daily_spending_per_month.plot(kind='bar')
plt.title('Average Daily Spending per Month')
plt.xlabel('Month-Year')
plt.ylabel('Average Daily Spending')
plt.show()

# Get top expenses
top_expenses = df[df['transaction_type'] == 'withdrawal'].nlargest(10, 'amount')
print("Top Expenses:")
print(top_expenses[['date', 'narration', 'amount', 'category']])

# Calculate average daily spending overall
average_daily_spending = daily_spending['amount'].mean()
print(f"Average Daily Spending: {average_daily_spending}")

# Plot distribution of transaction amounts
df['amount'].hist(bins=20)
plt.title('Distribution of Transaction Amounts')
plt.xlabel('Amount')
plt.ylabel('Frequency')
plt.show()

# Save the cleaned DataFrame to an Excel file
df.to_excel('cleaned_bank_statement.xlsx', index=False)
