import yfinance as yf
import tkinter as tk
import time
import datetime
import pandas as pd

today = str(datetime.date.today()) + " 00:00:00-04:00"
onlydate =  str(datetime.date.today())
yesterday = str(datetime.date.today()-datetime.timedelta(days=1))+" 00:00:00-04:00"
currentTime = str(datetime.datetime.now()).split(" ")[1]
print("current time is ",currentTime)
root = tk.Tk()
root.geometry("800x600")
root.title("Stock Analysis Tool")
title = tk.Label(root, text="Stock Analysis Tool")
title.place(relx=0.5,rely=0.2,anchor="center")
title.config(font=("Arial", 30))

#button = tk.Button(gui, text="Start program", bd=10)
#button.place(relx=0.5, rely=0.5,anchor="center")

def buildLeftTickers():
    tickers = ("^DJI", "^IXIC", "^GSPC")
    mapToName = {"^DJI":"Dow Jones", "^IXIC":"NASDAQ", "^GSPC":"S&P 500"}
    global curren
    if(currentTime>"08:30:00"):
        leftHeader = tk.Label(root, text=f"Today's changes {onlydate}")
        leftHeader.place(relx=0,rely=0)
        leftHeader.config(font=("Arial",12))
        position = .05
        for i in tickers:
            stock = yf.Ticker(i)
            stockData = stock.history(period="1d")
            print(stockData)
            stockDayChange = round(((float(stockData["Close"][today])/float(stockData["Open"][today]))-1)*100, 2)
            label = tk.Label(root, text=f"{mapToName.get(i)} ")
            label.place(relx=.01,rely=position)
            valChange = tk.Label(root, text=f"{stockDayChange}%")
            valChange.place(relx=0.15,rely=position)
            if(stockDayChange<0):
                valChange.config(fg="red")
            elif(stockDayChange>0):
                valChange.config(fg="green")
            position+=.04
    else:
        leftHeader = tk.Label(root, text=f"Yesterdays's changes {str(datetime.date.today()-datetime.timedelta(days=1))}")
        leftHeader.place(relx=0,rely=0)
        leftHeader.config(font=("Arial",11))
        leftSubtitle = tk.Label(root, text="Market still closed")
        leftSubtitle.place(relx=0.03,rely=0.04)
        leftSubtitle.config(font=("Arial",9))
        leftSubtitle.config(fg="red")
        position = .08
        for i in tickers:
            stock = yf.Ticker(i)
            stockData = stock.history(period="2d")
            #print(stockData)
            label = tk.Label(root, text=f"{mapToName.get(i)}  ")
            label.place(relx=.01,rely=position)
            stockDayChange = round(((float(stockData["Close"][yesterday])/float(stockData["Open"][yesterday]))-1)*100, 2)
            valChange = tk.Label(root, text=f"{stockDayChange}%")
            valChange.place(relx=0.15,rely=position)
            if(stockDayChange<0):
                valChange.config(fg="red")
            elif(stockDayChange>0):
                valChange.config(fg="green")
            position+=.04
def buildButtons():
    return

def start():

    root.mainloop()

