import pandas as pd

# Load the datasets
dal_data = pd.read_csv('/Users/oscarzhou/Downloads/DAL_data.csv')
clf_data = pd.read_csv('/Users/oscarzhou/Downloads/CLF_data.csv')


# Ensure the dates are datetime objects and set them as the index
dal_data['Date'] = pd.to_datetime(dal_data['Date'])
dal_data.set_index('Date', inplace=True)
clf_data['Date'] = pd.to_datetime(clf_data['Date'])
clf_data.set_index('Date', inplace=True)

# Calculate the total return for the buy-and-hold strategy over the period for DAL
dal_initial_price = dal_data['Adj Close'].iloc[0]  # Initial price
dal_final_price = dal_data['Adj Close'].iloc[-1]  # Final price
dal_total_return = (dal_final_price - dal_initial_price) / dal_initial_price

# Calculate the total return for the buy-and-hold strategy over the period for CLF
clf_initial_price = clf_data['Adj Close'].iloc[0]  # Initial price
clf_final_price = clf_data['Adj Close'].iloc[-1]  # Final price
clf_total_return = (clf_final_price - clf_initial_price) / clf_initial_price

# Money market return calculation, compounded annually at 5.27% interest over the period
years = dal_data.index[-1].year - dal_data.index[0].year
money_market_return = (1 + 0.0527) ** years - 1

# Compare the total returns and print them
print(f"DAL Total Return over {years} years: {dal_total_return * 100:.2f}%")
print(f"CLF Total Return over {years} years: {clf_total_return * 100:.2f}%")
print(f"Money Market Total Return over {years} years: {money_market_return * 100:.2f}%")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assuming you've loaded the DAL and CLF datasets and set 'Date' as a datetime index

# Calculate the daily return rate for the money market account
money_market_annual_rate = 0.0527
money_market_daily_rate = (1 + money_market_annual_rate)**(1/365) - 1

# Create a Series of the daily rate that is the same length as the DAL or CLF data
money_market_daily_returns = pd.Series([money_market_daily_rate] * len(dal_data), index=dal_data.index)

# Calculate the cumulative return, assuming $1 initial investment
money_market_cumulative_return = (1 + money_market_daily_returns).cumprod()

# Plotting the cumulative returns
dal_data['Cumulative Return'] = (1 + dal_data['Adj Close'].pct_change()).cumprod()
clf_data['Cumulative Return'] = (1 + clf_data['Adj Close'].pct_change()).cumprod()

plt.figure(figsize=(14, 7))
plt.plot(dal_data.index, dal_data['Cumulative Return'], label='DAL Buy-and-Hold')
plt.plot(clf_data.index, clf_data['Cumulative Return'], label='CLF Buy-and-Hold')
plt.plot(money_market_cumulative_return.index, money_market_cumulative_return, label='Money Market Account')

plt.title('Investment Strategy Performance Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.show()
