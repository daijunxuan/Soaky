import pandas as pd

# Load datasets
crude_oil_df = pd.read_csv('/Users/oscarzhou/Downloads/CLF_data.csv')
delta_df = pd.read_csv('/Users/oscarzhou/Downloads/DAL_data.csv')
us_market_df = pd.read_csv('/Users/oscarzhou/Downloads/averag.csv')

# Convert the 'Date' column to datetime objects
crude_oil_df['Date'] = pd.to_datetime(crude_oil_df['Date'])
delta_df['Date'] = pd.to_datetime(delta_df['Date'])
us_market_df['Date'] = pd.to_datetime(us_market_df['Date'])

# Merge the datasets on the 'Date' column
SY = pd.merge(crude_oil_df, delta_df, on='Date', suffixes=('_crude', '_delta'))

# Define the initial investment amount
initial_investment = 10000

# Rolling Window Strategy
def rolling_window_strategy(df, initial_investment, window_size, num_std_dev):
    cash = initial_investment
    shares = 0
    invested_amount = 0  # Track the amount invested in the current position

    for i in range(window_size, len(df)):
        current_price = df.iloc[i]['Adj Close_delta']
        rolling_mean = df.iloc[i]['RollingMean_delta']
        rolling_std = df.iloc[i]['RollingStd_delta']

        # Buy logic: Two conditions
        # Condition 1: Price below rolling mean minus standard deviation
        # Condition 2: Price has increased from the previous day
        if current_price < rolling_mean - num_std_dev * rolling_std and current_price > df.iloc[i - 1]['Adj Close_delta']:
            if cash > 0:
                shares_bought = cash / current_price
                shares += shares_bought
                invested_amount = shares_bought * current_price
                cash -= invested_amount

        # Sell logic: Two conditions
        # Condition 1: Price above rolling mean plus standard deviation
        # Condition 2: Price has decreased from the previous day or investment value has dropped below 95% of invested amount
        if (current_price > rolling_mean + num_std_dev * rolling_std and current_price < df.iloc[i - 1]['Adj Close_delta']) or \
           (invested_amount > 0 and current_price * shares < 0.95 * invested_amount):
            cash += shares * current_price
            shares = 0
            invested_amount = 0  # Reset the invested amount after selling

    # Final value (convert shares back to cash)
    final_value = cash + shares * df.iloc[-1]['Adj Close_delta']
    return final_value

# Calculate the maximum window size
max_window_size = len(SY) - 1
print(f"Maximum window size: {max_window_size}")

# Optimize the rolling window size
best_window_size = None
best_final_value = initial_investment

for window_size in range(2, max_window_size + 1):  # Test window sizes up to the maximum
    SY['RollingMean_delta'] = SY['Adj Close_delta'].rolling(window=window_size).mean()
    SY['RollingStd_delta'] = SY['Adj Close_delta'].rolling(window=window_size).std()
    temp_SY = SY.dropna()

    if not temp_SY.empty:
        final_value = rolling_window_strategy(temp_SY, initial_investment, window_size, 1)
        if final_value > best_final_value:
            best_final_value = final_value
            best_window_size = window_size

        print(f"Window size {window_size}: Final value {final_value}")

print(f'Best rolling window size: {best_window_size}')
print(f'Final value with best rolling window size: {best_final_value}')
