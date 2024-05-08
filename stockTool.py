import yfinance as yf
import tkinter as tk
import time
import datetime
import pandas as pd

root = tk.Tk()
root.geometry("800x600")
root.config(bg="white")
root.title("Stock Analysis Tool")
homeFrame = tk.Frame(root)
homeFrame.config(bg="white")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
title = tk.Label(homeFrame, text="Stock Analysis Tool")
title.grid(row=1, column=2, columnspan=5, sticky="nsew")
title.config(font=("Arial", 30), bg="white")
foundTickers = dict()

#building logic
lastMarketDay = datetime.date.today()
def setLastMarketDay() -> datetime.date:
    date=datetime.date.today()
    ticker=yf.Ticker("AAPL").history(start=date-datetime.timedelta(days=10))
    while(not (str(date)+" 00:00:00-04:00" in ticker["Close"].keys())):
        date=date-datetime.timedelta(days=1)
    global lastMarketDay
    lastMarketDay=str(date)+" 00:00:00-04:00"
    print(f"LAST MARKET DAY IS {lastMarketDay}")
    


def buildLeftTickers():
    tickers = ("^DJI", "^IXIC", "^GSPC")
    mapToName = {"^DJI":"Dow Jones", "^IXIC":"NASDAQ", "^GSPC":"S&P 500"}
    position = 0
    tickerFrame = tk.Frame(homeFrame)
    tickerFrame.grid(row=1, column=0, columnspan=2, sticky="n")
    tickerFrame.config(bg="white")
    leftHeader = tk.Label(homeFrame, text=f"Market changes {lastMarketDay.split(" ")[0]}")
    leftHeader.grid(row=0, column=0, columnspan=2)
    leftHeader.config(font=("Arial",12), bg="white")
    for i in tickers:
        stock = yf.Ticker(i)
        stockData = stock.history(period="1d")
        stockDayChange = round(((float(stockData["Close"][lastMarketDay])/float(stockData["Open"][lastMarketDay]))-1)*100, 2)
        label = tk.Label(tickerFrame, text=f"{mapToName.get(i)} ")
        label.config(bg="white")
        valChange = tk.Label(tickerFrame, text=f"{stockDayChange}%")
        valChange.config(bg="white")
        label.grid(row=position, column=0)
        valChange.grid(row=position, column=1, sticky="e")
        if(stockDayChange<0):
            valChange.config(fg="red")
        elif(stockDayChange>0):
            valChange.config(fg="green")
        position+=1
        foundTickers[i]=stock
    if(str(datetime.date.today())!=lastMarketDay.split(" ")[0]):
            marketClosed = tk.Label(homeFrame, text="Market still closed", font=("Arial", 9), fg="red", bg="white")
            marketClosed.grid(row=0,column=0, sticky="s", columnspan=2)

    
def buildButtons():
    bd = 5
    bg = "lightgray"
    selectColor = "lightyellow"

    findButton = tk.Button(homeFrame, text="Find Stock", activebackground=selectColor, bd=bd, bg=bg, height=3, width=10, font=("Arial", 12), command=findStock)
    findButton.grid(column=2, row=3, sticky="ew")

    watchListButton = tk.Button(homeFrame, text="Watchlist", activebackground=selectColor,bd=bd, bg=bg, height=3, width=10, font=("Arial", 12), command=findStock)
    watchListButton.grid(column=6, row=3, sticky="ew")

    compareButton = tk.Button(homeFrame, text="Compare \nStocks", activebackground=selectColor,bd=bd, bg=bg, height=3, width=10, font=("Arial", 12), command=findStock)
    compareButton.grid(column=2, row=5, sticky="ew")

    browseTopButton = tk.Button(homeFrame, text="Browse Top", activebackground=selectColor,bd=bd, bg=bg, height=3, width=10, font=("Arial", 12), command=findStock)
    browseTopButton.grid(column=6, row=5, sticky="ew")


def buildTopwatchlist():
    file = open("watchlist.txt")
    tickers = file.readlines()
    watchlistLabel = tk.Label(homeFrame, text="From your watchlist")
    watchlistLabel.grid(row=0, column=7, sticky="ne")
    watchlistLabel.config(font=("Arial", 15), bg="white")
    for i, tckr in enumerate(tickers):
        tickers[i] = tckr.strip()
    buildWatchListHelper(tickers=tickers, day=lastMarketDay)

def buildWatchListHelper(tickers, day):
    biggestGainers = [["",0], ["",0], ["",0]]
    biggestLosers = [["",0], ["",0], ["",0]]
    for i in tickers:
        stock = yf.Ticker(i)
        foundTickers[i]=stock
        name = stock.info.get("shortName")
        stockData = stock.history("1d")
        stockDayChange = round(((float(stockData["Close"][day])/float(stockData["Open"][day]))-1)*100, 2)
        for i in range(0, 3):
            if(stockDayChange>biggestGainers[i][1]):
                temp = biggestGainers[i]
                biggestGainers[i]=[name, stockDayChange]
                if(i<2):
                    biggestGainers[i+1]=temp
                break
            elif(stockDayChange<biggestLosers[i][1]):
                temp = biggestLosers[i]
                biggestLosers[i]=[name, stockDayChange]
                if(i<2):
                    biggestLosers[i+1]=temp
                break
    winnersFrame = tk.Frame(homeFrame, bg="white")
    for i, x in enumerate(biggestGainers):
        if(x[1]>0):
            if(len(x[0])>20):
                templabel = tk.Label(winnersFrame, bg="white", text=f"{x[0][:20]}.")
            else:
                templabel = tk.Label(winnersFrame, bg="white", text=f"{x[0]}")
            templabel.grid(row=i+1, column = 0, sticky="nsew")
            vallabel = tk.Label(winnersFrame, bg="white", fg="green", text=f"{x[1]}%")
            vallabel.grid(row=i+1, column=1, sticky="w")
        elif(x[1]==0):
            if(i>0):
                break
            templabel = tk.Label(winnersFrame, bg="white", text="No losses!")
            templabel.grid(row=i+1, column=0, sticky="nsew")
            break

    winnersLabel = tk.Label(homeFrame, text="Biggest gains", font=("Arial", 12), bg="white")
    winnersLabel.grid(row=0, column=7, sticky="se")
    winnersFrame.grid(row=1, column=7, sticky="e")

    losersFrame = tk.Frame(homeFrame, bg="white")
    for i, x in enumerate(biggestLosers):
        if(x[1]<0):
            if(len(x[0])>20):
                templabel = tk.Label(losersFrame, bg="white", text=f"{x[0][:20]}.")
            else:
                templabel = tk.Label(losersFrame, bg="white", text=f"{x[0]}")
            templabel.grid(row=i+1, column=0, sticky="nsew")
            vallabel = tk.Label(losersFrame, bg="white", fg="red", text=f"{x[1]}%")
            vallabel.grid(row=i+1, column=1, sticky="w")
        elif(x[1]==0):
            if(i>0):
                break
            templabel = tk.Label(losersFrame, bg="white", text="No losses!")
            templabel.grid(row=i+1, column=0, sticky="nsew")
            break
    losersLabel = tk.Label(homeFrame, text="Biggest losses", font=("Arial", 12), bg="white")
    losersLabel.grid(row=2, column=7, sticky="ne")
    losersFrame.grid(row=2, column=7, sticky="e")


def findStock():
    homeFrame.grid_forget()
    stockFrame = tk.Frame(root, bg="white")
    stockFrame.grid(row=0,column=0, sticky="nsew")
    stock = ""
    enterStock = tk.Entry(stockFrame, textvariable=stock, border=5)
    enterStock.grid(row=0, column=0, sticky="nsew")
    homeButton = tk.Button(stockFrame, text="Home", command=lambda : backToHome(stockFrame))
    homeButton.grid(row=0, column=7, sticky="nsew")
    submitButton = tk.Button(stockFrame, text="Submit", command=lambda : parseStock(enterStock))
    submitButton.grid(row=0, column=1, sticky="nsew")

def parseStock(stock):
    val = stock.get().upper().strip()
    ticker = yf.Ticker(val)
    if (len(ticker.history(period="1m"))==0): 
        warning = tk.Toplevel(root)
        warning.geometry("200x100")
        label = tk.Label(warning, text="Stock not found")
        button = tk.Button(warning, text="Ok", command=warning.destroy)
        label.grid(row=0, column=0, sticky="nsew")
        button.grid(row=1, column=0, sticky="nsew")
        print(f"{stock} NOT FOUND ERROR")
    else:
        print(f"{stock} found")


def weightsConfigure(rowNums, columnNums):
    for i in range(6):
        homeFrame.grid_rowconfigure(i, weight=rowNums[i])
    for i in range(8):
        homeFrame.grid_columnconfigure(i, weight=columnNums[i])

def backToHome(frame):
    print("CHANGING FRAME TO HOME")
    frame.grid_forget()
    homeFrame.grid(row=0,column=0,sticky="nsew")

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

    weightsConfigure([1, 1, 3, 3, 3, 3], [2, 2, 2, 4, 4, 2, 2, 6])
    #print(foundTickers)
    root.mainloop()
