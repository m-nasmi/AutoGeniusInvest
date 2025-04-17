# filename: top_10_stocks.py

import requests
import pandas as pd

def get_stock_data(symbol):
    api_key = 'YOUR_API_KEY'
    base_url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    datatype = 'json'

    params = {
        'function': function,
        'symbol': symbol,
        'apikey': api_key,
        'datatype': datatype
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    df = pd.DataFrame(data['Time Series (Daily)']).T
    df = df.sort_index(ascending=False)

    return df

# Replace 'MSFT' with the symbol of the stock you are interested in
df = get_stock_data('MSFT')
print(df)