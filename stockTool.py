import yfinance as yf
import tkinter as tk
import time
import datetime
import pandas as pd

today = str(datetime.date.today()) + " 00:00:00-04:00"
onlydate =  str(datetime.date.today())
yesterday = str(datetime.date.today()-datetime.timedelta(days=1))+" 00:00:00-04:00"
currentTime = str(datetime.datetime.now()).split(" ")[1].split(".")[0]
weekday = datetime.date.weekday(datetime.date.today())
print(currentTime)
root = tk.Tk()
root.geometry("800x600")
root.config(bg="white")
root.title("Stock Analysis Tool")
homeFrame = tk.Frame(root)
homeFrame.config(bg="white")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
title = tk.Label(homeFrame, text="Stock Analysis Tool")
title.grid(row=2, column=2, columnspan=4, sticky="nsew")
title.config(font=("Arial", 30), bg="white")



def buildLeftTickers():
    tickers = ("^DJI", "^IXIC", "^GSPC")
    mapToName = {"^DJI":"Dow Jones", "^IXIC":"NASDAQ", "^GSPC":"S&P 500"}
    position = 0
    tickerFrame = tk.Frame(homeFrame)
    tickerFrame.grid(row=1, column=0, columnspan=2, sticky="n")
    tickerFrame.config(bg="white")
    if(currentTime>"08:30:00" and weekday<5):
        leftHeader = tk.Label(homeFrame, text=f"Today's changes {onlydate}")
        leftHeader.grid(row=0, column=0, columnspan=2)
        leftHeader.config(font=("Arial",12), bg="white")
        for i in tickers:
            stock = yf.Ticker(i)
            stockData = stock.history(period="1d")
            stockDayChange = round(((float(stockData["Close"][today])/float(stockData["Open"][today]))-1)*100, 2)
            label = tk.Label(tickerFrame, text=f"{mapToName.get(i)} ")
            label.config(bg="white")
            valChange = tk.Label(tickerFrame, text=f"{stockDayChange}%")
            valChange.config(bg="white")
            buildTickerHelper(position=position, label=label, valChange=valChange, stockDayChange=stockDayChange)
            position+=1
    elif(not (weekday==0 or weekday==6)):
        leftHeader = tk.Label(homeFrame, text=f"Yesterdays's changes {str(datetime.date.today()-datetime.timedelta(days=1))}")
        leftHeader.config(bg="white")
        leftHeader.grid(row=0,column=0, sticky="n")
        leftHeader.config(font=("Arial",11))
        leftSubtitle = tk.Label(homeFrame, text="Market still closed")
        leftSubtitle.grid(column=0, row=0, sticky="s")
        leftSubtitle.config(font=("Arial",9))
        leftSubtitle.config(fg="red", bg="white")
        for i in tickers:
            stock = yf.Ticker(i)
            stockData = stock.history(period="2d")
            label = tk.Label(tickerFrame, text=f"{mapToName.get(i)}  ")
            label.config(bg="white")
            stockDayChange = round(((float(stockData["Close"][yesterday])/float(stockData["Open"][yesterday]))-1)*100, 2)
            valChange = tk.Label(tickerFrame, text=f"{stockDayChange}%")
            valChange.config(bg="white")
            buildTickerHelper(position=position, label=label, valChange=valChange, stockDayChange=stockDayChange)
            position+=1
    else:
        if(weekday==0):
            leftHeader = tk.Label(homeFrame, text=f"Friday's changes {str(datetime.date.today()-datetime.timedelta(days=3))}")
            friday = str(datetime.date.today()-datetime.timedelta(days=3))+" 00:00:00-04:00"
        else:  
            leftHeader = tk.Label(homeFrame, text=f"Friday's changes {str(datetime.date.today()-datetime.timedelta(days=2))}")
            friday = str(datetime.date.today()-datetime.timedelta(days=2))+" 00:00:00-04:00"
        leftHeader.config(bg="white")
        leftHeader.grid(row=0,column=0, sticky="n", columnspan=2)
        position = 2
        leftHeader.config(font=("Arial",11))
        leftSubtitle = tk.Label(homeFrame, text="Market still closed")
        leftSubtitle.grid(column=0, row=0, sticky="s")
        leftSubtitle.config(font=("Arial",9))
        leftSubtitle.config(fg="red", bg="white")
        for i in tickers:
            stock = yf.Ticker(i)
            stockData = stock.history(period="2d")
            label = tk.Label(tickerFrame, text=f"{mapToName.get(i)}  ")
            label.config(bg="white")
            stockDayChange = round(((float(stockData["Close"][friday])/float(stockData["Open"][friday]))-1)*100, 2)
            valChange = tk.Label(tickerFrame, text=f"{stockDayChange}%")
            valChange.config(bg="white")
            buildTickerHelper(position=position, label=label, valChange=valChange, stockDayChange=stockDayChange)
            position+=1

def buildTickerHelper(position, label, valChange, stockDayChange):
    label.grid(row=position, column=0)
    valChange.grid(row=position, column=1, sticky="e")

    if(stockDayChange<0):
        valChange.config(fg="red")
    elif(stockDayChange>0):
        valChange.config(fg="green")

    
def buildButtons():
    bd = 5
    bg = "lightgray"

    findButton = tk.Button(homeFrame, text="Find Stock", bd=bd, bg=bg, height=3, width=10, font=("Arial", 12), command=findStock)
    findButton.grid(column=2, row=3, sticky="ew")

    watchListButton = tk.Button(homeFrame, text="Watchlist", bd=bd, bg=bg, height=3, width=10, font=("Arial", 12), command=findStock)
    watchListButton.grid(column=5, row=3, sticky="ew")

    compareButton = tk.Button(homeFrame, text="Compare \nStocks", bd=bd, bg=bg, height=3, width=10, font=("Arial", 12), command=findStock)
    compareButton.grid(column=2, row=5, sticky="ew")

    browseTopButton = tk.Button(homeFrame, text="Browse Top", bd=bd, bg=bg, height=3, width=10, font=("Arial", 12), command=findStock)
    browseTopButton.grid(column=5, row=5, sticky="ew")


def buildTopwatchlist():
    file = open("watchlist.txt")
    tickers = file.readlines()
    watchlistLabel = tk.Label(homeFrame, text="From your watchlist")
    watchlistLabel.grid(row=0, column=7, sticky="nsew")
    watchlistLabel.config(font=("Arial", 15), bg="white")
    for i, tckr in enumerate(tickers):
        tickers[i] = tckr.strip()
    print(currentTime>"8:30:00")
    if(currentTime>"8:30:00" and weekday<5):
        buildWatchListHelper(tickers=tickers, day=today)
    elif(weekday==6 or weekday==0):
        if(weekday==6):
            friday = str(datetime.date.today()-datetime.timedelta(days=2))+" 00:00:00-04:00"
        if(weekday==0):
            friday = str(datetime.date.today()-datetime.timedelta(days=3))+" 00:00:00-04:00"
        buildWatchListHelper(tickers=tickers, day=friday)
    else:
        buildWatchListHelper(tickers=tickers, day=yesterday)

def buildWatchListHelper(tickers, day):
    print(day)
    biggestGainers = [["",0], ["",0], ["",0]]
    biggestLosers = [["",0], ["",0], ["",0]]
    for i in tickers:
        stock = yf.Ticker(i)
        name = stock.info.get("shortName")
        stockData = stock.history("1d")
        stockDayChange = round(((float(stockData["Close"][day])/float(stockData["Open"][day]))-1)*100, 2)
        for i in range(0, 3):
            if(stockDayChange>biggestGainers[i][1]):
                temp = biggestGainers[i]
                biggestGainers[i]=[name, stockDayChange]
                if(i<2):
                    biggestGainers[i+1]=temp
            elif(stockDayChange<biggestLosers[i][1]):
                temp = biggestLosers[i]
                biggestLosers[i]=[name, stockDayChange]
                if(i<2):
                    biggestLosers[i+1]=temp
    winnersFrame = tk.Frame(homeFrame, bg="white")
    for i, x in enumerate(biggestGainers):
        if(x[1]>0):
            templabel = tk.Label(winnersFrame, bg="white", text=f"{x[0]} - {x[1]}%")
            templabel.grid(row=i, sticky="nsew")
    winnersLabel = tk.Label(homeFrame, text="Biggest gains", font=("Arial", 14))
    winnersLabel.grid(row=1, column=7, sticky="nsew")
    winnersFrame.grid(row=2, column=7, sticky="nsew")

    losersFrame = tk.Frame(homeFrame, bg="white")
    for i, x in enumerate(biggestLosers):
        if(x[1]<0):
            templabel = tk.Label(losersFrame, bg="white", text=f"{x[0]} - {x[1]}%")
            templabel.grid(row=i, sticky="nsew")
    losersLabel = tk.Label(homeFrame, text="Biggest losses", font=("Arial", 14))
    losersLabel.grid(row=3, column=7, sticky="nsew")
    losersFrame.grid(row=4, column=7, sticky="nsew")


def findStock():
    homeFrame.grid_forget()
    time.sleep(1)
    homeFrame.grid(row=0, column=0, sticky="nsew")

def weightsConfigure(rowNums, columnNums):
    for i in range(6):
        homeFrame.grid_rowconfigure(i, weight=rowNums[i])
    for i in range(8):
        homeFrame.grid_columnconfigure(i, weight=columnNums[i])

def start():
    homeFrame.grid(row=0,column=0, sticky="nsew")
    # for i in range(1, 6):
    #     label = tk.Label(homeFrame, text=f"{i}")
    #     label.config(bg="white")
    #     label.grid(row=i, column=0)
    # for i in range(1, 8):
    #     label = tk.Label(homeFrame, text=f"{i}")
    #     label.config(bg="white")
    #     label.grid(row=0, column=i)

    weightsConfigure([1, 1, 3, 3, 3, 3], [2, 2, 2, 4, 4, 2, 2, 11])

    root.mainloop()

