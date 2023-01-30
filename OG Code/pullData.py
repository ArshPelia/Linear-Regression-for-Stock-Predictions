import requests

def get_stock_info(symbol):
    API_KEY = "3MREQ8VOLM7JK6GN"
    URL = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"

    response = requests.get(URL)
    stock_info = response.json()

    return stock_info["Global Quote"]

symbol = input("Enter stock symbol: ")
stock_info = get_stock_info(symbol)

print(f"Latest information for {symbol}:")
print(f"Open: {stock_info['02. open']}")
print(f"High: {stock_info['03. high']}")
print(f"Low: {stock_info['04. low']}")
print(f"Price: {stock_info['05. price']}")
print(f"Volume: {stock_info['06. volume']}")
print(f"Latest trading day: {stock_info['07. latest trading day']}")
print(f"Previous close: {stock_info['08. previous close']}")
print(f"Change: {stock_info['09. change']}")
print(f"Change percent: {stock_info['10. change percent']}")
print(f"Last update: {stock_info['11. last update']}")



open = stock_info['02. open']
high = stock_info['03. high']
low = stock_info['04. low']
price = stock_info['05. price']
volume = stock_info['06. volume']
latest_trading_day = stock_info['07. latest trading day']
previous_close = stock_info['08. previous close']
change = stock_info['09. change']
change_percent = stock_info['10. change percent']
