import yfinance as yf

# Define the ticker symbol
ticker_symbol = 'AAPL'

# Fetch the stock data
stock = yf.Ticker(ticker_symbol)

# Get the historical market data
hist = stock.history(period='1d')

# Get the latest market data
latest_data = stock.info

# Extract required information
price = latest_data['currentPrice']
open_price = hist['Open'].iloc[-1]
high_price = hist['High'].iloc[-1]
low_price = hist['Low'].iloc[-1]
market_cap = latest_data['marketCap']
pe_ratio = latest_data['forwardPE']
dividend_yield = latest_data['dividendYield']

# Print the results
print(f"Price: ${price}")
print(f"Open: ${open_price}")
print(f"High: ${high_price}")
print(f"Low: ${low_price}")
print(f"Market Cap: ${market_cap}")
print(f"P/E Ratio: {pe_ratio}")
print(f"Dividend Yield: {dividend_yield * 100 if dividend_yield else 'N/A'}%")
