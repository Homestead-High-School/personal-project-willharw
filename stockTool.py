import yfinance as yf
import tkinter as tk
from tkinter import ttk
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    ticker=yf.Ticker("^DJI").history(start=date-datetime.timedelta(days=10), end = date+datetime.timedelta(days=1),)
    #print(ticker)
    #print(ticker["Open"].keys())
    while(not (str(date)+" 00:00:00-04:00" in ticker["Open"].keys())):
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
            leftHeader.grid(sticky="n")

    
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
    rowweights = [1,1,1,1,1,1]
    colweights=[1,1,3,3,3,3,1,1]
    for i in range(6):
        stockFrame.grid_rowconfigure(i, weight=rowweights[i])
        tk.Label(stockFrame, text=f"{i}", bg="white", fg="white").grid(row=i, column=0, sticky="nsew")
    for i in range(8):
        stockFrame.grid_columnconfigure(i, weight=colweights[i])
        tk.Label(stockFrame, text=f"{i}", bg="white", fg="white").grid(row=0, column=i, sticky="nsew")
    stock = ""
    enterStock = tk.Entry(stockFrame, textvariable=stock, border=5)
    enterStock.grid(row=0, column=0, sticky="n")
    homeButton = tk.Button(stockFrame, text="Home", command=lambda : backToHome(stockFrame))
    homeButton.grid(row=0, column=7, sticky="n")
    submitButton = tk.Button(stockFrame, text="Submit", command=lambda : parseStock(stock=enterStock, stockFrame=stockFrame))
    submitButton.grid(row=0, column=1, sticky="nw")


def parseStock(stock : tk.Entry, stockFrame : tk.Frame):
    val = stock.get().upper().strip()
    ticker = 0
    try:
        if(foundTickers[val]!=None):
            ticker = foundTickers[val]
    except:
        ticker = yf.Ticker(val)
    if (len(ticker.history(period="1m"))==0): 
        errorMessage(frame=stockFrame, text="STOCK NOT FOUND")
    else:
        print(f"{stock} found")
        buildFindStockViewer(ticker=val, frame=stockFrame)
        

def buildFindStockViewer(ticker : str, frame : tk.Frame):
    global periodChooser
    print("building stock frame")
    splitted = lastMarketDay.split("-")
    yr=int(splitted[0])
    mnth=int(splitted[1])
    day=int(splitted[2].split(" ")[0])
    del splitted
    lastMarketDatetime = datetime.date(year=yr, month=mnth, day=day)
    startingPeriod = 1
    tickerYF = yf.Ticker(ticker)
    figure = graphBuilder(frame = frame, ticker = ticker, start=lastMarketDatetime-datetime.timedelta(weeks=1), end=lastMarketDatetime)
    stockLabel = tk.Label(frame, text=f"{tickerYF.info.get("shortName")}", bg="white", font=("Arial", 20)).grid(row=0,column=2,columnspan=4,sticky="n")
    stockTimePeriod = tk.Label(frame, text=f"Showing data for past {startingPeriod} weeks", bg="white", font=("Arial", 15)).grid(row=0,column=2,columnspan=4,sticky="s")
    periodOptions = ["1 week", "4 weeks", "1 year", "5 years"]
    periodChooser = ttk.Combobox(frame, values=periodOptions)
    periodChooser.grid(row=1, column=7, sticky="n")
    updateTime = tk.Button(frame, text="Update Time Period", bg="white", command=lambda : getTimePeriod(frame=frame, ticker = ticker, periodChooser=periodChooser)).grid(row=1,column=7,sticky="s")

def getTimePeriod(frame : tk.Frame, periodChooser : ttk.Combobox, ticker : str, marketDate : datetime.date):
    time = periodChooser.get()
    start = 0
    match time:
        case "1 week":
            start = marketDate-datetime.timedelta(weeks=1)
        case "4 weeks":
            start = marketDate-datetime.timedelta(weeks=4)
        case "1 year":
            start = marketDate-datetime.timedelta(weeks=52)
        case "5 years":
            start = marketDate-datetime.timedelta(weeks=52*5)
        case _:
            errorMessage(frame=frame, text="INVALID TIME, USE DROPDOWN")


    graphBuilder(frame=frame, ticker=ticker, end=marketDate, start = start)

def graphBuilder(frame : tk.Frame, ticker : str, start : datetime.date, end : datetime.date) -> FigureCanvasTkAgg:
    tickerYF = yf.Ticker(ticker)
    history = tickerYF.history(start=start, end=end, interval = "1d")
    print(history)
    prices=history["Close"]
    dates=prices.keys()
    print(prices,dates)
    newDates = list()
    for date in dates:
        # brokenDate = str(date).split(" ")[0].split("-")
        # newDates.append(brokenDate[1]+"-"+brokenDate[2])
        newDates.append(date)
    stockFigure = plt.Figure(figsize=(4,3), dpi=100)
    stockGraph = FigureCanvasTkAgg(stockFigure, frame)
    stockGraph.get_tk_widget().grid(row=1, column=2, columnspan=5, rowspan=4, sticky="nsew")
    mainGraph = stockFigure.add_subplot(111)
    mainGraph.plot(newDates, prices, color="red")
    mainGraph.set_xlabel("Date")
    mainGraph.set_ylabel("Price $")
    stockFigure.autofmt_xdate()
    return stockGraph

def errorMessage(frame : tk.Frame, text : str):
    warning = tk.Toplevel(frame)
    warning.geometry("200x100")
    label = tk.Label(warning, text=f"{str}")
    button = tk.Button(warning, text="Ok", command=warning.destroy)
    label.grid(row=0, column=0, sticky="nsew", columnspan=2)
    button.grid(row=1, column=0, sticky="nsew", columnspan=2)
    print(f"{str} ERROR")

def weightsConfigure(rowNums, columnNums):
    for i in range(6):
        homeFrame.grid_rowconfigure(i, weight=rowNums[i])
    for i in range(8):
        homeFrame.grid_columnconfigure(i, weight=columnNums[i])

def backToHome(frame : tk.Frame):
    print("CHANGING FRAME TO HOME")
    frame.grid_forget()
    homeFrame.grid(row=0,column=0,sticky="nsew")

def start():
    homeFrame.grid(row=0,column=0, sticky="nsew")

    weightsConfigure([1, 1, 3, 3, 3, 3], [2, 2, 2, 4, 4, 2, 2, 6])
    
    root.mainloop()
