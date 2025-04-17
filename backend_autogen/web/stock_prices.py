# filename: stock_prices.py

import yfinance as yf

# List of ticker symbols for 10 UK companies
tickers = ['BP.L', 'BT-A.L', 'GSK.L', 'LLOY.L', 'NG.L', 'RDSB.L', 'RIO.L', 'TSCO.L', 'ULVR.L', 'VOD.L']

# Fetch the latest stock prices
data = yf.download(tickers, period="1d", interval="1d", group_by='ticker')

# Print the latest stock prices
for ticker in tickers:
    print(f"{ticker}: {data[ticker]['Close'][0]}")