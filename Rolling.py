import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Make sure to replace the file paths with the actual locations of your data files
dal_path = '/Users/oscarzhou/Downloads/DAL_data.csv'
clf_path = '/Users/oscarzhou/Downloads/CLF_data.csv' 

# Load the DAL and CLF data
dal_data = pd.read_csv(dal_path, parse_dates=['Date'], index_col='Date')
clf_data = pd.read_csv(clf_path, parse_dates=['Date'], index_col='Date')

# Now, dal_data and clf_data are defined and can be used for further analysis

# Calculate the 100-day SMA for DAL
dal_data['SMA_100'] = dal_data['Adj Close'].rolling(window=100).mean()

# Calculate the 100-day SMA for CLF
clf_data['SMA_100'] = clf_data['Adj Close'].rolling(window=100).mean()

# Assuming dal_data and clf_data are already loaded and SMA_100 is calculated

# Calculate the short-term moving average (e.g., 20-day)
dal_data['SMA_20'] = dal_data['Adj Close'].rolling(window=20).mean()
clf_data['SMA_20'] = clf_data['Adj Close'].rolling(window=20).mean()

# Identify buy/sell signals for DAL
dal_data['Signal'] = 0
dal_data['Signal'][20:] = np.where(dal_data['SMA_20'][20:] > dal_data['SMA_100'][20:], 1, 0)
dal_data['Positions'] = dal_data['Signal'].diff()

# Plotting the DAL and CLF with buy and sell signals
plt.figure(figsize=(14, 7))

# Plot DAL Adjusted Close and SMA lines
plt.plot(dal_data.index, dal_data['Adj Close'], label='DAL Adjusted Close', alpha=0.5)
plt.plot(dal_data.index, dal_data['SMA_20'], label='DAL 20-Day SMA', alpha=0.9)
plt.plot(dal_data.index, dal_data['SMA_100'], label='DAL 100-Day SMA', alpha=0.9)

# Plot CLF Adjusted Close and SMA line
plt.plot(clf_data.index, clf_data['Adj Close'], label='CLF Adjusted Close', alpha=0.5)
plt.plot(clf_data.index, clf_data['SMA_100'], label='CLF 100-Day SMA', alpha=0.9)

# Highlight buy signals with green up arrow
plt.plot(dal_data[dal_data['Positions'] == 1].index, dal_data['Adj Close'][dal_data['Positions'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Highlight sell signals with red down arrow
plt.plot(dal_data[dal_data['Positions'] == -1].index, dal_data['Adj Close'][dal_data['Positions'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

# Formatting plot
plt.title('DAL and CLF with Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Adjusted Close')
plt.legend()
plt.show()
