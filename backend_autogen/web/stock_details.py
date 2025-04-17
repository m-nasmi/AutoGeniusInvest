# filename: stock_details.py

import yfinance as yf

# Define the ticker symbols
tickers = ['MSFT', 'AAPL', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'NFLX', 'BABA', 'INTC', 'CSCO']

# Fetch the data
data = {ticker: yf.Ticker(ticker).info for ticker in tickers}

# Print the data
for ticker, info in data.items():
    print(f"\n{ticker} Stock Details:")
    print(f"Previous Close: {info['previousClose']}")
    print(f"Open: {info['open']}")
    print(f"Volume: {info['volume']}")
    print(f"Market Cap: {info['marketCap']}")
    print(f"Forward PE: {info['forwardPE']}")
    print(f"Dividend Yield: {info['dividendYield']}")