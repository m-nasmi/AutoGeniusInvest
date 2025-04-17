# filename: stock_rates.py

import yfinance as yf

# List of some major companies listed on LSE
companies = ['VOD.L', 'BP.L', 'HSBA.L', 'AZN.L', 'GSK.L']

for company in companies:
    ticker = yf.Ticker(company)
    data = ticker.history(period="1d")
    print(f"Company: {company}")
    print(f"Open: {data['Open'][0]}")
    print(f"High: {data['High'][0]}")
    print(f"Low: {data['Low'][0]}")
    print(f"Close: {data['Close'][0]}")
    print(f"Volume: {data['Volume'][0]}")
    print("------------------------")