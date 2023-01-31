import tkinter
import customtkinter  # <- import the CustomTkinter module
import requests, re, csv, joblib
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("500x300")
root_tk.title("CustomTkinter Test")

def get_stock_info(symbol):
    API_KEY = "3MREQ8VOLM7JK6GN"
    URL = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"

    response = requests.get(URL)
    stock_info = response.json()

    return stock_info["Global Quote"]

# symbol = input("Enter stock symbol: ")
def EvaluateStock(symbol):
    stock_info = get_stock_info(symbol)

    # print(f"Latest information for {symbol}:")
    # print(f"Open: {stock_info['02. open']}")
    # print(f"High: {stock_info['03. high']}")
    # print(f"Low: {stock_info['04. low']}")
    # print(f"Price: {stock_info['05. price']}")
    # print(f"Volume: {stock_info['06. volume']}")
    # print(f"Latest trading day: {stock_info['07. latest trading day']}")
    # print(f"Previous close: {stock_info['08. previous close']}")
    # print(f"Change: {stock_info['09. change']}")
    # print(f"Change percent: {stock_info['10. change percent']}")


    open = float(stock_info['02. open'])
    high = float(stock_info['03. high'])
    low = float(stock_info['04. low'])
    price = float(stock_info['05. price'])
    volume = float(stock_info['06. volume'])
    previous_close = float(stock_info['08. previous close'])

    # latest_trading_day = stock_info['07. latest trading day']
    # change = stock_info['09. change']
    # change_percent = stock_info['10. change percent']

    model = joblib.load('model.joblib')
    stock_prediction = model.predict([[open, high, low, volume, previous_close]])
    print("Predicted stock price: ", stock_prediction)

    # make predictions for the next 7 days
    x = np.array([open, high, low, volume, previous_close])
    y = np.zeros(7)
    for i in range(7):
        y[i] = model.predict([x])[0]
        x[-1] = y[i]
    
    # plot the predictions
    plt.plot(range(7), y, label="Prediction")
    plt.plot([0, 6], [price, price], label="Today's Price")
    plt.xlabel("Days")
    plt.ylabel("Stock Price")
    plt.title("Stock Price Prediction")
    plt.legend()
    plt.show()


def button_function():
    stock_name = stock_entry.get()
    # print("Stock name entered: ", stock_name)
    stock_Info = get_stock_info(stock_name)
    EvaluateStock(stock_name)


customtkinter.set_appearance_mode("Dark") # Other: "Light", "System" (only macOS)
# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=root_tk, text='Execute' , corner_radius=10, command=button_function)
button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

label = customtkinter.CTkLabel(master=root_tk,
                               text="Stock Symbol: ",
                               width=120,
                               height=25,
                               text_color="Black",
                               corner_radius=8)
label.place(relx=0.2, rely=0.2, anchor=tkinter.CENTER)

stock_entry = customtkinter.CTkEntry(master=root_tk,
                               width=200,
                               height=25,
                               corner_radius=10)
stock_entry.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

def main():
    root_tk.mainloop()

main()