# filename: stock_scraper.py

import yfinance as yf

def get_stock_data(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data.append({
            'name': info['shortName'],
            'last_price': info['regularMarketPreviousClose'],
        })
    return data

def main():
    # List of tickers for top UK stocks
    tickers = ['LLOY.L', 'BP.L', 'VOD.L', 'GSK.L', 'AZN.L', 'HSBA.L', 'BATS.L', 'RDSA.L', 'RIO.L', 'ULVR.L']
    data = get_stock_data(tickers)
    data = sorted(data, key=lambda x: x['last_price'], reverse=True)
    for i, d in enumerate(data):
        print(f"{i+1}. {d['name']}: {d['last_price']}")

if __name__ == "__main__":
    main()