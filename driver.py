import yfinance as yf
import tkinter as tk
import time
import datetime
import pandas as pd

today = str(datetime.date.today()) + " 00:00:00-04:00"
onlydate =  str(datetime.date.today())
root = tk.Tk()
#frame = tk.Frame(root, borderwidth=5, relief="ridge", width=500, height=300)
root.geometry("800x600")
root.title("Stock Analysis Tool")
title = tk.Label(root, text="Stock Analysis Tool")
title.place(relx=0.5,rely=0.2,anchor="center")
title.config(font=("Arial", 30))

#button = tk.Button(gui, text="Start program", bd=10)
#button.place(relx=0.5, rely=0.5,anchor="center")
tickers = ("^DJI", "^IXIC", "^GSPC")
mapToName = {"^DJI":"Dow Jones", "^IXIC":"NASDAQ", "^GSPC":"S&P 500"}
leftHeader = tk.Label(root, text=f"Today's changes {onlydate}")
leftHeader.place(relx=0,rely=0)
leftHeader.config(font=("Arial",12))
position = .05

for i in tickers:
    stock = yf.Ticker(i)
    stockData = stock.history(period="2d")
    stockDayChange = round(((float(stockData["Close"][today])/float(stockData["Open"][today]))-1)*100, 2)
    label = tk.Label(root, text=f"{mapToName.get(i)} has moved {stockDayChange}%")
    label.place(relx=.01,rely=position)
    position+=.04


root.mainloop()