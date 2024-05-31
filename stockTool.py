import yfinance as yf
import tkinter as tk
from tkinter import ttk
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import updateMarketCap
import locale
import webbrowser
from tkinter import font as fontlist
locale.setlocale(locale.LC_ALL, '')

font = "Arial"

root = tk.Tk()
root.geometry("800x600")
root.config(bg="white")
root.title("Stock Analysis Tool")
# homeFrame = tk.Frame(root)
# homeFrame.config(bg="white")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
foundTickers = dict()

leftStockInfoFrame = tk.Frame(root, bg="red")
leftWatchListInfoFrame = tk.Frame(root, bg="blue")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# img = PIL.Image.open("background.png")
# resized = img.resize((screen_width,screen_height))
# bgimage = PIL.ImageTk.PhotoImage(resized)
# tk.Label(homeFrame, image=bgimage).grid(row=0,column=0,rowspan=6,columnspan=8)

# title = tk.Label(homeFrame, text="Stock Tool", font=(font, 30))
# title.grid(row=1, column=2, columnspan=4, sticky="nsew")
# title.config(font=(font, 30), bg="white")
timeAddon = ""
lastMarketDay = datetime.date.today()
lastMarketDate = lastMarketDay
def setLastMarketDay() -> datetime.date:
    date=datetime.date.today()
    ticker=yf.Ticker("^DJI").history(period="1mo")
    # dates = yf.Ticker("AAPL").history(period="1y")["Close"].keys()
    # for d in dates:
    #     print(d)
    global timeAddon
    if(ticker["Close"].keys()[0].dst() == datetime.timedelta(hours=1)):
        addon = " 00:00:00-04:00"
    else:
        addon = " 00:00:00-05:00"
    while(not (str(date)+addon in ticker["Open"].keys())):
        date=date-datetime.timedelta(days=1)
    global lastMarketDay
    global lastMarketDate
    lastMarketDate = date
    lastMarketDay=str(date)+addon
    timeAddon=addon
    print(f"LAST MARKET DAY IS {lastMarketDay}")
    
def build():
    global homeFrame
    homeFrame = tk.Frame(root)
    homeFrame.config(bg="white")
    title = tk.Label(homeFrame, text="Stock Tool", font=(font, 30))
    title.grid(row=1, column=2, columnspan=4, sticky="nsew")
    title.config(font=(font, 30), bg="white")
    homeButtonBuilder()
    homeBuildWatchList()
    homeIndexBuilder()

def homeIndexBuilder():
    tickers = ("^DJI", "^IXIC", "^GSPC")
    mapToName = {"^DJI":"Dow Jones", "^IXIC":"NASDAQ", "^GSPC":"S&P 500"}
    position = 0
    tickerFrame = tk.Frame(homeFrame)
    tickerFrame.grid(row=1, column=0, columnspan=1, sticky="n")
    tickerFrame.config(bg="white")
    leftHeader = tk.Label(homeFrame, text=f"Market on {lastMarketDay.split(" ")[0]}", font=(font,10))
    leftHeader.grid(row=0, column=0, columnspan=1)
    leftHeader.config(font=(font,12), bg="white")
    tk.Button(homeFrame, text="Settings", command = lambda : homeSettings()).grid(row=5, column=7, sticky="se")

    for i in tickers:
        stock = yf.Ticker(i)
        stockData = stock.history(period="1d")
        stockDayChange = round(((float(stockData["Close"][lastMarketDay])/float(stockData["Open"][lastMarketDay]))-1)*100, 2)
        label = tk.Label(tickerFrame, text=f"{mapToName.get(i)} ", font=(font, 10))
        label.config(bg="white")
        valChange = tk.Label(tickerFrame, text=f"{stockDayChange}%", font=(font, 10))
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
            marketClosed = tk.Label(homeFrame, text="Market still closed", font=(font, 9), fg="red", bg="white")
            marketClosed.grid(row=0,column=0, sticky="s", columnspan=1)
            leftHeader.grid(sticky="n")
def homeButtonBuilder():
    bd = 5
    bg = "lightgray"
    selectColor = "lightyellow"

    findButton = tk.Button(homeFrame, text="Find Stock", activebackground=selectColor, bd=bd, bg=bg, height=3, width=10, font=(font, 12), command=lambda : findStock())
    findButton.grid(column=2, row=3, sticky="ew")

    watchListButton = tk.Button(homeFrame, text="Watchlist", activebackground=selectColor,bd=bd, bg=bg, height=3, width=10, font=(font, 12), command=watchList)
    watchListButton.grid(column=5, row=3, sticky="ew")

    compareButton = tk.Button(homeFrame, text="Compare \nStocks", activebackground=selectColor,bd=bd, bg=bg, height=3, width=10, font=(font, 12), command=lambda : compareStocks("1 Month"))
    compareButton.grid(column=2, row=5, sticky="ew")

    browseTopButton = tk.Button(homeFrame, text="Browse Stocks", activebackground=selectColor,bd=bd, bg=bg, height=3, width=10, font=(font, 12), command=browseStocks)
    browseTopButton.grid(column=5, row=5, sticky="ew")
def homeBuildWatchList():
    file = open("watchlist.txt")
    tickers = file.readlines()
    watchlistLabel = tk.Label(homeFrame, text="Watchlist", font=(font, 20))
    watchlistLabel.grid(row=0, column=7, sticky="ne")
    watchlistLabel.config(font=(font, 15), bg="white")
    for i, tckr in enumerate(tickers):
        tickers[i] = tckr.strip()
    homeWatchListBuildHelper(tickers=tickers, day=lastMarketDay)
def homeWatchListBuildHelper(tickers, day):
    biggestGainers = [["",0], ["",0], ["",0]]
    biggestLosers = [["",0], ["",0], ["",0]]
    for i in tickers:
        try:
            stock = yf.Ticker(i)
            foundTickers[i]=stock
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
        except:
            print(f"Error: {i} not found")
    winnersFrame = tk.Frame(homeFrame, bg="white")
    for i, x in enumerate(biggestGainers):
        if(x[1]>0):
            if(len(x[0])>20):
                templabel = tk.Label(winnersFrame, bg="white", text=f"{x[0][:20]}.", font=(font, 10))
            else:
                templabel = tk.Label(winnersFrame, bg="white", text=f"{x[0]}", font=(font, 10))
            templabel.grid(row=i+1, column = 0, sticky="nsew")
            vallabel = tk.Label(winnersFrame, bg="white", fg="green", text=f"{x[1]}%", font=(font, 10))
            vallabel.grid(row=i+1, column=1, sticky="w")
        elif(x[1]==0):
            if(i>0):
                break
            templabel = tk.Label(winnersFrame, bg="white", text="No gains!", font=(font, 10))
            templabel.grid(row=i+1, column=0, sticky="nsew")
            break

    winnersLabel = tk.Label(homeFrame, text="Biggest gains", font=(font, 12), bg="white")
    winnersLabel.grid(row=0, column=7, sticky="se")
    winnersFrame.grid(row=1, column=7, sticky="e")

    losersFrame = tk.Frame(homeFrame, bg="white")
    for i, x in enumerate(biggestLosers):
        if(x[1]<0):
            if(len(x[0])>20):
                templabel = tk.Label(losersFrame, bg="white", text=f"{x[0][:20]}.", font=(font, 10))
            else:
                templabel = tk.Label(losersFrame, bg="white", text=f"{x[0]}", font=(font, 10))
            templabel.grid(row=i+1, column=0, sticky="nsew")
            vallabel = tk.Label(losersFrame, bg="white", fg="red", text=f"{x[1]}%", font=(font, 10))
            vallabel.grid(row=i+1, column=1, sticky="w")
        elif(x[1]==0):
            if(i>0):
                break
            templabel = tk.Label(losersFrame, bg="white", text="No losses!", font=(font, 10))
            templabel.grid(row=i+1, column=0, sticky="nsew")
            break
    losersLabel = tk.Label(homeFrame, text="Biggest losses", font=(font, 12), bg="white")
    losersLabel.grid(row=2, column=7, sticky="ne")
    losersFrame.grid(row=2, column=7, sticky="e")
def homeSettings():
    toplevel = tk.Toplevel(homeFrame, bg="white")
    tk.Button(toplevel, text="Update stocks.txt", command = lambda : updateMarketCap.updateStocksTxt(frame=toplevel)).grid(row=1,column=0)
    tk.Label(toplevel, text="Warning: this is experimental and will FREEZE THE PROGRAM for 10-15 minutes\nIt will update all the market caps and company names used in stocks.txt", bg="white", font=(font, 10)).grid(row=0,column=0)
    tk.Button(toplevel, text="Change font", command = lambda: updateFont(toplevel), state="disabled").grid(row=2,column=0)

def updateFont(frame : tk.Frame):
    frame.destroy()
    toplevel = tk.Toplevel(homeFrame, bg="white")
    default = ""
    entry=tk.Entry(toplevel, bg="white", textvariable=default)
    entry.grid(row=0,column=0)
    submitButton = tk.Button(toplevel, text="Submit", command=lambda : setFont(frame=toplevel, entry=entry))
    submitButton.grid(row=0, column=1, sticky="nw")
def setFont(frame : tk.Frame, entry : tk.Entry):
    global font
    enterstr = entry.get()
    frame.destroy()
    if(enterstr in fontlist.families()):
        font=enterstr
        homeFrame.destroy()
        build()
    else:
        errorMessage(root, "Not a font")

def compareStocks(time : str):
    compareFrame = tk.Frame(root, bg="white")
    tk.Label(compareFrame, text="Stock Comparison", bg="white", font=(font, 25)).grid(row=0,column=2,columnspan=4, sticky="new")
    homeFrame.grid_forget()
    compareFrame.grid(row=0,column=0, sticky="nsew")
    rowweights = [1,1,1,1,1,1]
    colweights=[1,1,1,1,1,1,1,1]
    homeButton = tk.Button(compareFrame, text="Home",command = lambda : backToHome(compareFrame))
    homeButton.grid(row=0,column=7,sticky="ne")

    periodOptions = ["1 Week", "1 Month", "1 Year", "5 Years"]
    default = time
    periodChooser = ttk.Combobox(compareFrame, values=periodOptions, textvariable=default, state="readonly")
    periodChooser.grid(row=1, column=0, sticky="n")
    periodChooser.insert(0, time)
    tk.Button(compareFrame, text="Submit", command=lambda : compareGraphWrapper(frame=compareFrame, entry=periodChooser)).grid(row=1,column=0,sticky="s")

    for i in range(6):
        compareFrame.grid_rowconfigure(i, weight=rowweights[i], uniform="a")
    for i in range(8):
        compareFrame.grid_columnconfigure(i, weight=colweights[i], uniform="b")
    editCompare = tk.Button(compareFrame, text="Edit Comparison",command = lambda : compareEditor(compareFrame))
    editCompare.grid(row=0,column=0,sticky="nw")
    compareGraphBuilder(compareFrame, time=time)

def compareGraphWrapper(frame : tk.Frame, entry : ttk.Combobox):
    time=entry.get()
    frame.grid_forget()
    compareStocks(time)
def compareGraphBuilder(frame : tk.Frame, time : str):
    listtickers=[]
    match time:
        case "1 Week":
            setweeks = 1
            interval = "1d"
        case "1 Month":
            setweeks=4
            interval = "1d"
        case "1 Year":
            setweeks=52
            interval = "1d"
        case "5 Years":
            setweeks=52*5
            interval = "1d"
        case _:
            print("error")
    tk.Label(frame, text="If a stock doesn't appear in a certain time frame, it probably didn't exist for the whole time period", font=(font, 10), bg="white").grid(row=6, column=0, columnspan=7)
    date=lastMarketDate-datetime.timedelta(weeks=setweeks)
    ticker=yf.Ticker("^DJI").history(start=lastMarketDate-datetime.timedelta(weeks=setweeks), end = lastMarketDate+datetime.timedelta(days=1), interval=interval)
    # print(ticker)
    # print(date)
    if interval == "60m":
        addon = " 09:30:00-04:00"
    else:
        addon = " 00:00:00-04:00"
    while(not (str(date)+addon in ticker["Open"].keys())):
        date=date-datetime.timedelta(days=1)
    beginningDateFormatted =str(date)+addon

    with open("compare.txt","r") as file:
        l = file.readlines()
        for line in l:
            listtickers.append(line.strip())
    stockFigure = plt.Figure(figsize=(4,3), dpi=100)
    stockGraph = FigureCanvasTkAgg(stockFigure, frame)
    widget = stockGraph.get_tk_widget().grid(row=1, column=1, columnspan=6, rowspan=5, sticky="nsew")
    mainGraph = stockFigure.add_subplot(111)
    for ticker in listtickers:
        try:
            tickerYF = yf.Ticker(ticker)
            history = tickerYF.history(start=lastMarketDate-datetime.timedelta(weeks=setweeks), end=lastMarketDate, interval = interval)
            prices=history["Close"]
            dates=prices.keys()
            beginningPrice = prices[beginningDateFormatted]
            pricesPercentFromDate = []
            for price in prices:
                pricesPercentFromDate.append(price/beginningPrice*100-100)
            mainGraph.plot(dates, pricesPercentFromDate, label=ticker)
            mainGraph.set_xlabel("Date")
            mainGraph.set_ylabel("Price % Change")
        except:
            print(ticker, "broke")
            continue
    mainGraph.legend()
    mainGraph.set_title(time)
    stockFigure.autofmt_xdate()
def compareEditor(frame : tk.Frame):
    toplevel = tk.Toplevel(frame, bg="white")
    listtickers=[]
    tk.Label(toplevel, bg="white", font=(font, 15), text="Check to remove").grid(row=0, column=0)
    with open("compare.txt","r") as file:
        l = file.readlines()
        for line in l:
            listtickers.append(line.strip())
    checkbuttonvals = []
    for i in range(len(listtickers)):
        checkbuttonvals.append(tk.IntVar())
    for i, ticker in enumerate(listtickers):
        tk.Checkbutton(toplevel, text=ticker, bg="white", font=(font, 10), variable=checkbuttonvals[i], onvalue=1, offvalue=0, height=2, width=10).grid(row=i+1, column=0)
    tk.Button(toplevel, text="Submit", command=lambda : compareRemove(frame=frame, toplevel=toplevel, tickers=listtickers, checkvals=checkbuttonvals)).grid(row=len(listtickers)+1, column=0)
def compareRemove(frame : tk.Frame, toplevel : tk.Toplevel, tickers : list, checkvals : list):
    frame.destroy()
    
    toplevel.destroy()
    toremove = []
    for index, val in enumerate(checkvals):
        if(val.get()==1):
            toremove.append(tickers[index])
    print(toremove)
    with open("compare.txt", "r") as f:
        lines = f.readlines()
    with open("compare.txt", "w") as f:
        print("removing")
        for line in lines:
            if not (line.strip() in toremove):
                f.write(line)
    compareStocks(time="1 Month")

def findStock():
    stockFrame = tk.Frame(root, bg="white")
    homeFrame.grid_forget()
    stockFrame.grid(row=0,column=0, sticky="nsew")
    rowweights = [1,1,1,1,1,1]
    colweights=[1,1,3,3,3,3,1,1]
    default=""
    searchForCompanyButton = tk.Button(stockFrame, text="Search by company name",command = lambda : findStockCompanySearch(frame=stockFrame, button=searchForCompanyButton, entry=companyEntry))
    searchForCompanyButton.grid(row=1,column=1,sticky="nw")
    companyEntry = tk.Entry(stockFrame, textvariable=default, border=5)
    companyEntry.grid(row=1,column=0, sticky="new")
    extraStuff = [searchForCompanyButton, companyEntry]
    for i in range(6):
        stockFrame.grid_rowconfigure(i, weight=rowweights[i])
        #tk.Label(stockFrame, text=f"{i}", bg="white", fg="white").grid(row=i, column=0, sticky="nsew")
    for i in range(8):
        stockFrame.grid_columnconfigure(i, weight=colweights[i])
        #tk.Label(stockFrame, text=f"{i}", bg="white", fg="white").grid(row=0, column=i, sticky="nsew")
    
    enterStock = tk.Entry(stockFrame, textvariable=default, border=5)
    enterStock.grid(row=0, column=0, sticky="new")
    homeButton = tk.Button(stockFrame, text="Home", command=lambda : backToHome(stockFrame))
    homeButton.grid(row=0, column=7, sticky="new")
    submitButton = tk.Button(stockFrame, text="Find Stock Ticker", command=lambda : findStockParse(stock=enterStock, stockFrame=stockFrame, extra=extraStuff))
    submitButton.grid(row=0, column=1, sticky="nw")
def findStockCompanySearch(frame:tk.Frame, button:tk.Button, entry:tk.Entry):
    strToFind=entry.get().strip().upper()
    matchingCompanies=[]
    with open("stocks.txt","r") as file:
        l = file.readlines()
        for line in l:
            companyname = line.strip().split("|")[2].upper()
            if(companyname.find(strToFind)>-1):
                matchingCompanies.append(line)
    toplevel = tk.Toplevel(frame)
    for i,line in enumerate(matchingCompanies):
        split = line.strip().split("|")
        ticker = split[0]
        name = split[2]
        comButton = tk.Button(toplevel, text=f"{ticker}-{name}", command=lambda stock=ticker : findStockPickCompany(frame=frame,toplevel=toplevel, button=button, entry=entry, ticker=stock) )
        comButton.grid(row=i, column=0, sticky="ew")
def findStockPickCompany(frame : tk.Frame, toplevel : tk.Toplevel, button:tk.Button, entry:tk.Entry, ticker:str):
    frame.destroy()
    toplevel.destroy()
    button.destroy()
    entry.destroy()
    browseStocksHelper(ticker)
    #FIX THIS SO IT DOESNT BUILD A WHOLE NEW FRAME
def findStockParse(stock : tk.Entry, stockFrame : tk.Frame, extra : list):
    val = stock.get().upper().strip()
    for i in extra:
        try:
            i.destroy()
        except:
            print("failed to destroy extra object")
    for widget in stockFrame.winfo_children():
        if(type(widget)==tk.Label or type(widget)==tk.Frame):
            for subwidget in widget.winfo_children():
                subwidget.grid_remove()
            widget.grid_remove()

    ticker = None
    try:
        if(foundTickers[val]!=None):
            ticker = foundTickers[val]
    except:
        ticker = yf.Ticker(val)
    if (len(ticker.history(period="1mo"))==0): 
        errorMessage(frame=stockFrame, text="STOCK NOT FOUND")
    else:
        print(f"{stock} found")
        findStockBuilder(ticker=val, frame=stockFrame)
def findStockBuilder(ticker : str, frame : tk.Frame):
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
    #print(tickerYF.major_holders)
    news = tickerYF.news
    news = news[:5]
    #newsframe = tk.Frame(frame, bg="red").grid(row=3,column=7,rowspan=2,sticky="nsew")
    tk.Label(frame, bg="white", font=(font, 15), text="News").grid(row=5,column=0,sticky="s")

    for index, dict in enumerate(news):
        temp = tk.Label(frame, bg="white", fg="blue",font=(font, 8), text=f"{dict.get("title")}", cursor="hand2")
        temp.grid(row=index+6,column=0,columnspan=6, sticky="sw")
        url = str(dict.get("link"))
        print(url)
        temp.bind("<Button-1>", func=lambda event, u=url: callback(u))

    compareButton = tk.Button(frame, text="Add to compare", command = lambda : addToCompare(ticker, button=compareButton))
    compareButton.grid(row=2,column=7,sticky="new")

    with open("compare.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        if line.strip()==ticker:
            compareButton.config(state="disabled")

    addToWatchlistButton = tk.Button(frame, text="Add to watchlist", command=lambda stock=ticker : findStockWatchlistAdder(stock=stock, button=addToWatchlistButton), state="active")
    addToWatchlistButton.grid(row=0,column=6, sticky="new")
    with open("watchlist.txt", "r") as file:
        tickers = file.readlines()
        for t in tickers:
            tstrip = t.strip()
            if(tstrip==ticker):
                addToWatchlistButton.config(state="disabled", text="On watchlist")

    figure = findStockGraphBuilder(frame = frame, ticker = ticker, start=lastMarketDatetime-datetime.timedelta(weeks=1), end=lastMarketDatetime)
    stockLabel = tk.Label(frame, text=f"{tickerYF.info.get("shortName")}", bg="white", font=(font, 20)).grid(row=0,column=2,columnspan=4,sticky="n")
    stockInfo = tickerYF.info
    #print(stockInfo)
    isStock = False
    try:
        stockBio = tk.Label(frame, text=f"Country: {stockInfo["country"]}\nIndustry: {stockInfo["industry"]}\nFirst Trading Date: {time.strftime("%Y-%m-%d", time.localtime(stockInfo["firstTradeDateEpochUtc"]))}", bg="white", font=(font,10)).grid(row=0, column=2, columnspan=4, sticky="s")
        isStock = True
    except:
        try:
            stockBio = tk.Label(frame, text=f"Fund (collection of stocks)\nFirst Trading Date: {time.strftime("%Y-%m-%d", time.localtime(stockInfo["firstTradeDateEpochUtc"]))}", bg="white", font=(font,10)).grid(row=0, column=2, columnspan=4, sticky="s")
        except: 
            try:
                stockBio = tk.Label(frame, text=f"Country: {stockInfo["country"]}\nIndustry: {stockInfo["industry"]}", bg="white", font=(font,10)).grid(row=0, column=2, columnspan=4, sticky="s")
                isStock=True
            except:
                stockBio = tk.Label(frame, text="Error displaying bio", bg="white", font=(font,10)).grid(row=0, column=2, columnspan=4, sticky="s")
    findStockLeftInfoBuilder(frame=frame, info=stockInfo, isStock=isStock)
    if(lastMarketDatetime==datetime.date.today()):
        periodOptions = ["Today","1 week", "4 weeks", "1 year", "5 years"]
    else:
        periodOptions = ["1 week", "4 weeks", "1 year", "5 years"]
    startingChoice = "1 Year"
    periodChooser = ttk.Combobox(frame, values=periodOptions, textvariable=startingChoice, state="readonly")
    periodChooser.grid(row=0, column=7, sticky="s")
    updateTime = tk.Button(frame, text="Update Time Period", bg="white", command=lambda : findStockTimePeriodResolver(frame=frame, ticker = ticker, button=periodChooser, marketDate=lastMarketDatetime)).grid(row=1,column=7,sticky="n")
def callback(link : str):
    webbrowser.open_new(link)

def findStockLeftInfoBuilder(frame : tk.Frame, info : dict, isStock : bool):
    ticker = info["symbol"]
    global leftStockInfoFrame
    leftStockInfoFrame.children.clear()
    leftStockInfoFrame = tk.Frame(frame, bg="white", highlightcolor="yellow")
    leftStockInfoFrame.grid(row=1, column=0, rowspan=6)
    
    #print(info)
    if(isStock):
        tck = yf.Ticker(ticker)
        try:
            shares = tck.insider_transactions["Shares"]
            texts = tck.insider_transactions["Text"]
            dates = tck.insider_transactions["Start Date"]
            oneYearAgo = datetime.date.today()-datetime.timedelta(days=365)
            sharesSold = 0
            sharesPurchased = 0
            for i, text in enumerate(texts):
                text = str(text)
                dateString = str(dates[i]).split(" ")[0].split("-")
                dateOfTransaction = datetime.date(year=int(dateString[0]), month=int(dateString[1]), day=int(dateString[2]))
                #print(dateOfTransaction, oneYearAgo)
                if(dateOfTransaction>oneYearAgo):
                    if(text.find("Sale")>-1):
                        sharesSold+=shares[i]
                    elif(text.find("Purchase")>-1) or text.find("Award")>-1:
                        sharesPurchased+=shares[i]
                else:
                    break
            tk.Label(frame, text=f"Recent insider share purchases: {sharesPurchased}", bg="white", border=3, relief="ridge", font=(font, 10)).grid(row=5, column=7, sticky="ew")
            tk.Label(frame, text=f"Recent insider share sales: {sharesSold}", bg="white", border=3, relief="ridge", font=(font, 10)).grid(row=5, column=7, sticky="ews")                  
        except:
            print("No insider transactions found")
        
        infoList = ["currentPrice", "recommendationKey", "overallRisk", "beta","dividendYield", "forwardPE", "shortPercentOfFloat","averageVolume", "marketCap", "pegRatio", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "targetMedianPrice", "targetMeanPrice", "totalCashPerShare"]

        for i, value in enumerate(infoList):
            try:
                tk.Label(leftStockInfoFrame, text=f"{value} : {info[value]}", bg="white", border=3, relief="ridge", font=(font, 10)).grid(row=i+3, column=0, sticky="ew")
            except:
                tk.Label(leftStockInfoFrame, text=f"{value} : UNAVAILABLE", bg="white", border=3, relief="ridge", font=(font, 10)).grid(row=i+3, column=0, sticky="ew")
    else:
        infoList = ["legalType", "category", "averageVolume", "totalAssets", "trailingPE", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "ytdReturn"]
        for i, value in enumerate(infoList):
            try:
                tk.Label(leftStockInfoFrame, text=f"{value} : {info[value]}", bg="white", border=3, relief="ridge", font=(font, 10)).grid(row=i+1, column=0, sticky="we")
            except:
                tk.Label(leftStockInfoFrame, text=f"{value} : UNAVAILABLE", bg="white", border=3, relief="ridge", font=(font, 10)).grid(row=i+1, column=0, sticky="we")
def findStockTimePeriodResolver(frame : tk.Frame, button : ttk.Combobox, ticker : str, marketDate : datetime.date):
    time = button.get()
    start = 0
    timeLabel = tk.Label(frame, text="", bg="white", font=(font, 15))
    timeLabel.grid(row=1,column=2,sticky="nsew")
    match time:
        case "Today":
            start = marketDate
            timeLabel.config(text="Showing data for today")
        case "1 week":
            start = marketDate-datetime.timedelta(weeks=1)
            timeLabel.config(text="Showing data for past week")
        case "4 weeks":
            start = marketDate-datetime.timedelta(weeks=4)
            timeLabel.config(text="Showing data for past 4 weeks")
        case "1 year":
            start = marketDate-datetime.timedelta(weeks=52)
            timeLabel.config(text="Showing data for past year")
        case "5 years":
            start = marketDate-datetime.timedelta(weeks=52*5)
            timeLabel.config(text="Showing data for past 5 years")
        case _:
            errorMessage(frame=frame, text="INVALID TIME, USE DROPDOWN")
    findStockGraphBuilder(frame=frame, ticker=ticker, end=marketDate, start = start)
def findStockGraphBuilder(frame : tk.Frame, ticker : str, start : datetime.date, end : datetime.date) -> FigureCanvasTkAgg:
    tickerYF = yf.Ticker(ticker)
    if(start==end):
        history = tickerYF.history(period="1d", interval = "1m")
    else:
        history = tickerYF.history(start=start, end=end, interval = "1d")
    prices=history["Close"]
    dates=prices.keys()
    stockFigure = plt.Figure(figsize=(4,3), dpi=100)
    stockGraph = FigureCanvasTkAgg(stockFigure, frame)
    stockGraph.get_tk_widget().grid(row=1, column=2, columnspan=5, rowspan=4, sticky="nsew")
    mainGraph = stockFigure.add_subplot(111)
    mainGraph.plot(dates, prices, color="red")
    mainGraph.set_xlabel("Date")
    mainGraph.set_ylabel("Price $")
    stockFigure.autofmt_xdate()
    return stockGraph
def findStockWatchlistAdder(stock : str, button : tk.Button):
    button.config(state="disabled", text="Added!", fg="green")
    file = open("watchlist.txt", "a")
    file.write(stock+"\n")
    file.close()

def addToCompare(ticker : str, button : tk.Button):
    button.config(state="disabled", text="Added!")

    with open("compare.txt", "a") as f:
        f.write(ticker+"\n")
def rmFromCompare(ticker : str):
    with open("compare.txt", "r") as f:
        lines = f.readlines()
    with open("compare.txt", "w") as f:
        print("removing")
        for line in lines:
            if (line.strip() != ticker):
                f.write(line)
    
def watchList():
    watchListFrame = tk.Frame(root, bg="white")
    homeFrame.grid_forget()
    watchListFrame.grid(row=0, column=0, sticky="nsew")
    colweights = [1,5,2,2,2,2,2,2]
    rowweights = [1,2,2,2,2,2]
    for i in range(6):
        watchListFrame.grid_rowconfigure(i, weight=rowweights[i])
    for i in range(8):
        watchListFrame.grid_columnconfigure(i, weight=colweights[i])
    homeButton = tk.Button(watchListFrame, text="Home", command=lambda : backToHome(watchListFrame), border=5, relief="raised")
    homeButton.grid(row=0, column=7, sticky="new")
    addButton = tk.Button(watchListFrame, text="Add stock to watchlist", command = lambda : watchListAdd(frame=watchListFrame, entry=addEntry), border=5, relief="raised")
    addButton.grid(row=2, column=3, sticky="s")
    default = ""
    addEntry=tk.Entry(watchListFrame, bg="white", textvariable=default, border=5)
    addEntry.grid(row=3, column=3, sticky="n")

    rmButton = tk.Button(watchListFrame, text="Remove stock from watchlist", command=lambda : watchListRm(frame=watchListFrame, entry=rmEntry), border=5, relief="raised")
    rmButton.grid(row=4,column=3, sticky="s")
    rmEntry=tk.Entry(watchListFrame, bg="white", textvariable=default, border=5)
    rmEntry.grid(row=5, column=3, sticky="n")
    watchListLeftBuilder(watchListFrame)
    tk.Label(watchListFrame, text="Your watchlist", bg="white", font=(font, 20)).grid(row=0, column=1, columnspan=3, sticky="n")
    tk.Button(watchListFrame, text="Refresh", command = lambda : watchListLeftBuilder(watchListFrame), border=5, relief="raised").grid(row=1,column=7, sticky="ne")
    tk.Label(watchListFrame, text="Past Day", bg="white", font=(font, 12)).grid(row=0, column=0, sticky="w")
    tk.Label(watchListFrame, text="Ticker - Name", bg="white", font=(font, 12)).grid(row=0, column=0)
def watchListLeftBuilder(frame : tk.Frame):
    file = open("watchlist.txt")
    for widget in frame.winfo_children():
        if(widget == tk.Label):
            widget.destroy()
    tickers = file.readlines()
    plaintexttickers = []
    for i, tckr in enumerate(tickers):
        tckr = tckr.strip()
        plaintexttickers.append(tckr)
        try:
            tickers[i]=foundTickers[tckr]
        except:
            try:
                tickers[i]=yf.Ticker(tckr)
                foundTickers[tckr] = tickers[i]
            except:
                errorMessage(frame=frame, text="INVALID TICKER IN WATCHLIST")
    tickersFrame = tk.Frame(frame, bg="white")
    tickersFrame.grid(row=1, column=0, rowspan=6, columnspan=1, sticky="news")
    tickersFrame.grid_columnconfigure(0, weight=1)
    for i, ticker in enumerate(tickers):
        tickersFrame.grid_rowconfigure(i, weight=1)
        tk.Button(master=tickersFrame, bg="white", text=f"{plaintexttickers[i]}-{ticker.info["shortName"]}", command=lambda stock=plaintexttickers[i]: browseStocksHelper(browsedTicker=stock)).grid(row=i, column=1, sticky="nw")
        stockData = ticker.history("1d")
        try:
            percentchange = round(((float(stockData["Close"][lastMarketDay])/float(stockData["Open"][lastMarketDay]))-1)*100, 2)
        except:
            percentchange = 34402
        percentLabel = tk.Label(master=tickersFrame, bg="white", text=f"{percentchange}%", font=(font, 10))
        percentLabel.grid(row=i, column=0, sticky="n")
        if(percentchange<0):
            percentLabel.config(fg="red")
        elif(percentchange>0):
            percentLabel.config(fg="green")
def watchListAdd(frame : tk.Frame, entry : tk.Entry):
    stock = entry.get().upper().strip()
    try:
        foundTickers[stock]
        errorMessage(frame=frame, text="ALREADY IN HERE SILLY")
    except:
        try:
            something = yf.Ticker(stock)
            print("1")
            foundTickers.update({stock : something})
            print("2")
            file = open("watchlist.txt", "a")
            file.write(stock+"\n")
            file.close()
            print("3")
            entry.delete(first=0, last=len(stock))
        except Exception as e:
            errorMessage(frame=frame, text=str(e))
    watchListLeftBuilder(frame=frame)
def watchListRm(frame : tk.Frame, entry : tk.Entry):
    stock = entry.get().upper().strip()
    try:
        foundTickers.pop(stock) 
        with open("watchlist.txt", "r") as f:
            lines = f.readlines()
        with open("watchlist.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != stock:
                    f.write(line)
        entry.delete(first=0, last=len(stock))
    except:
        errorMessage(frame=frame, text="NOT IN WATCHLIST")
    watchListLeftBuilder(frame=frame)


def browseStocks():
    browseFrame = tk.Frame(root, bg="white")
    homeFrame.grid_forget()
    browseFrame.grid(row=0, column=0, sticky="nsew")
    colweights = [1,1,1,1,1,1,1,1,1,1,1]
    rowweights = [1,1,1,1,1,1,1,1]
    for i in range(8):
        browseFrame.grid_rowconfigure(i, weight=rowweights[i])
    for i in range(11):
        browseFrame.grid_columnconfigure(i, weight=colweights[i], uniform="a")
    homeButton = tk.Button(browseFrame, text="Home", command=lambda : backToHome(browseFrame), border=5, relief="raised")
    homeButton.grid(row=0, column=10, sticky="new")

    bubbleButton = tk.Button(browseFrame, text="Top 30", command=lambda : browseStocksTop30(browseFrame), border=5, relief="raised")
    bubbleButton.grid(row=0, column=9, sticky="new")

    tk.Label(browseFrame, text="Browse Stocks", bg="white", font=(font,20)).grid(row=0, column=3, columnspan=4, sticky="n")
    industries = ['Healthcare', 'Basic Materials', 'Consumer Defensive', 'Financial Services', 'Industrials', 'Technology', 'Consumer Cyclical', 'Real Estate', 'Communication Services', 'Energy', 'Utilities']
    
    #this bit of code creates a hashmap with each key being an industry and value being sorted list of stocks in industry by market cap
    database = {}
    for i in industries:
        database[i]=[]
    with open("stocks.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            #print(line)
            line=line.strip()
            splitup = line.split("|")
            currentlist = database[splitup[1]]
            database.update({splitup[0] : currentlist.append(splitup)})
    bgs = ["#ffa1a1","#b5b184","#c1d8e3","#46874c","#775b82","#ff8ad4","#d69e6d","#ba8865","#e8dfdf","#fcf762","#03c4ff"]
    for i,industry in enumerate(industries):
        rawindustry=industry
        splitindustry = industry.split(" ")
        title = ""
        for txt in splitindustry:
            title+=txt+"\n"
        tk.Label(browseFrame, text=title.strip(), bg="white", font=(font, 10)).grid(row=1, column=i)
        stocksInSector = database[industry]
        sortedStocks = sorted(stocksInSector, key=sortTupleSecondVal, reverse=True)
        database.update({industry : sortedStocks})
        for j in range(5):
            stock = sortedStocks[j]
            #print(stock)
            if(len(stock[2])>15):
                secondline = ""
                split = stock[2].split(" ")
                splitcleaned =[]
                if(len(split)>2):   
                    for e in split:
                        if(e.find("Inc.")>-1 or e.find(")")>-1 or  e.find("and")>-1 or e.find("&")>-1):
                            continue
                        else:
                            splitcleaned.append(e)
                else:
                    splitcleaned = split
                if(len(splitcleaned)>3):
                    splitcleaned=splitcleaned[:3]
                for word in splitcleaned:
                    if(len(word)<4):
                        secondline+=word+" "
                    else:
                        secondline+=word+"\n"
                secondline=secondline.strip()
            else:
                secondline=stock[2]
            temp = tk.Button(browseFrame, text=f"{stock[0]}\n{secondline}\n${round(int(stock[-1])/1_000_000_000,1)}B", height=5, width=13, bg=bgs[i], relief="solid", border=1, font=(font, 12), command=lambda stock=stock: browseStocksHelper(browsedTicker=stock[0]))
            temp.grid(row=j+2, column=i)
        if(len(industry)>15):
            split = industry.split(" ")
            industry = ""
            for j in split:
                industry+=j+"\n"
        industry=industry.strip()
        tk.Button(browseFrame, text=f"See more\n{industry}\nstocks", bg="lightgrey", relief="groove", border=2, font=(font, 11), height=4,command = lambda industry=rawindustry : browseStocksSeeMore(frame=browseFrame, sector=industry, database=database, page=1, lastFrame=None)).grid(row=7, column=i, sticky="ew")
def browseStocksSeeMore(frame : tk.Frame, sector : str, database : dict, page : int, lastFrame : tk.Frame):
    listStocks = database[sector]
    try: 
        lastFrame.grid_forget()
    except:
        del lastFrame
    frame.grid_forget()
    expandedFrame = tk.Frame(root, bg="white")
    expandedFrame.grid(row=0, column=0, sticky="nsew")
    colweights = [1,1,1,1,1,1,1,1,1,1,1]
    rowweights = [1,1,1,1,1,1,1,1,1,1,1]
    for i in range(11):
        expandedFrame.grid_rowconfigure(i, weight=rowweights[i])
    for i in range(10):
        expandedFrame.grid_columnconfigure(i, weight=colweights[i])
    backButton = tk.Button(expandedFrame, text="Back", command=lambda : switchFrames(goTo=frame, hide=expandedFrame), border=5, relief="raised")
    backButton.grid(row=0, column=9, sticky="new")
    tk.Label(expandedFrame, text=f"{sector} - Page {page}", bg="white", font=(font,20)).grid(row=0, column=2, columnspan=5, sticky="n")
    
    prevPage = tk.Button(expandedFrame, text="Previous Page", command = lambda : browseStocksSeeMore(frame=frame, sector=sector, database=database, page=page-1, lastFrame=expandedFrame))
    prevPage.grid(row=0,column=0)
    nextPage = tk.Button(expandedFrame, text="Next Page", command = lambda : browseStocksSeeMore(frame=frame, sector=sector, database=database, page=page+1, lastFrame=expandedFrame))
    nextPage.grid(row=0,column=2)
    if(page==1):
        prevPage.config(state="disabled")
    if((len(listStocks)+99)//100==page):
        nextPage.config(state="disabled")
    i = page*100-100
    for row in range(1, 11):
        for col in range(0, 10):
            tupleinfo = listStocks[i]
            if(len(tupleinfo[2])>20):
                secondline = tupleinfo[2][:20]+"."
            else:
                secondline=tupleinfo[2]
            try:
                tk.Button(expandedFrame, text=f"{tupleinfo[0]} - Mkt.Cap${round(int(tupleinfo[-1])/1_000_000_000, 2)}B\n{secondline}", command=lambda stock=tupleinfo[0] : browseStocksHelper(browsedTicker=stock)).grid(row=row,column=col)
            except:
                tk.Button(expandedFrame, text=f"{tupleinfo[0]}\n{secondline}", command=lambda stock=tupleinfo[0] : browseStocksHelper(browsedTicker=stock)).grid(row=row,column=col)
            i+=1
def browseStocksHelper(browsedTicker : str):
    stockFrame = tk.Frame(root, bg="white")
    homeFrame.grid_forget()
    stockFrame.grid(row=0,column=0, sticky="nsew")
    rowweights = [1,1,1,1,1,1]
    colweights=[1,1,3,3,3,3,1,1]
    for i in range(6):
        stockFrame.grid_rowconfigure(i, weight=rowweights[i])
        #tk.Label(stockFrame, text=f"{i}", bg="white", fg="white").grid(row=i, column=0, sticky="nsew")
    for i in range(8):
        stockFrame.grid_columnconfigure(i, weight=colweights[i])
        #tk.Label(stockFrame, text=f"{i}", bg="white", fg="white").grid(row=0, column=i, sticky="nsew")
    stock = ""
    enterStock = tk.Entry(stockFrame, textvariable=stock, border=5)
    enterStock.grid(row=0, column=0, sticky="nw")
    homeButton = tk.Button(stockFrame, text="Back", command=lambda : backToHome(stockFrame))
    homeButton.grid(row=0, column=7, sticky="new")
    submitButton = tk.Button(stockFrame, text="Find Stock Ticker", command=lambda : findStockParse(stock=enterStock, stockFrame=stockFrame, extra=[]))
    submitButton.grid(row=0, column=1, sticky="nw")

    val = browsedTicker

    for widget in stockFrame.winfo_children():
        if(type(widget)==tk.Label or type(widget)==tk.Frame):
            for subwidget in widget.winfo_children():
                subwidget.grid_remove()
            widget.grid_remove()

    ticker = None
    try:
        if(foundTickers[val]!=None):
            ticker = foundTickers[val]
    except:
        ticker = yf.Ticker(val)
    if (len(ticker.history(period="1mo"))==0): 
        errorMessage(frame=stockFrame, text="STOCK NOT FOUND")
    else:
        print(f"{stock} found")
        findStockBuilder(ticker=val, frame=stockFrame)
def browseStocksTop30(frame : tk.Frame):
    frame.grid_forget()
    topFrame = tk.Frame(root, bg="white")
    topFrame.grid(row=0,column=0,sticky="nsew")
    backButton = tk.Button(topFrame, text="BACK", command=lambda : switchFrames(goTo=frame, hide=topFrame))
    backButton.grid(row=0,column=5,sticky="ne")
    
    colweights = [1,1,1,1,1,1]
    rowweights = [1,3,3,3,3,3]
    for i in range(6):
        topFrame.grid_rowconfigure(i, weight=rowweights[i])
    for i in range(6):
        topFrame.grid_columnconfigure(i, weight=colweights[i], uniform="a")

    with open("stocks.txt", "r") as file:
        lines = file.readlines()
        linetuples = []
        for line in lines:
            try:
                if(int(line.strip().split("|")[-1])>100_000_000_000):
                    linetuples.append(line.split("|"))
            except:
                continue
    sortedstocks = sorted(linetuples, key=sortTupleSecondVal, reverse=True)
    sortedstocks = sortedstocks[:45]
    withtickers = []
    for stock in sortedstocks:
        tick = yf.Ticker(stock[0])
        newlist = []
        for thing in stock:
            newlist.append(thing)
        newlist.append(tick)
        newlist.append(tick.info["marketCap"])
        withtickers.append(newlist)

    sortedByCap = sorted(withtickers, key = lambda stock : stock[-1], reverse="True")
    for row in range(1,6):
        for col in range(0,6):
            stockline = sortedByCap[(row-1)*6+col]
            stock = stockline[4]
            stockData = stock.history(period="1d")
            stockDayChange = round(((float(stockData["Close"][lastMarketDay])/float(stockData["Open"][lastMarketDay]))-1)*100, 2)
            stockbutton = tk.Button(topFrame, font=(font, 12),text=f"{stockline[0]}\n{stockline[2]}\n{stockline[1]}\n{locale.currency(int(stockline[-1]), grouping=True)}\n{stockDayChange}%", command=lambda stock=stockline[0]: browseStocksHelper(browsedTicker=stock))
            stockbutton.grid(row=row,column=col,sticky="NSEW")
            if(stockDayChange>0):
                if(stockDayChange>1):
                    stockbutton.config(bg="green")
                else:
                    stockbutton.config(bg="lightgreen")
            elif(stockDayChange<0):
                if(stockDayChange<1):
                    stockbutton.config(bg="darkred")
                else:
                    stockbutton.config(bg="lightred")
         

def sortTupleSecondVal(s):
    try:
        return int(s[-1])
    except:
        return 0

def errorMessage(frame : tk.Frame, text : str):
    warning = tk.Toplevel(frame)
    warning.geometry("200x100")
    label = tk.Label(warning, text=f"{text}", font=(font, 10))
    button = tk.Button(warning, text="Ok", command=warning.destroy)
    label.grid(row=0, column=0, sticky="nsew", columnspan=2)
    button.grid(row=1, column=0, sticky="nsew", columnspan=2)
    print(f"{str} ERROR")

def homeWeightsConfigure(rowNums, columnNums):
    for i in range(6):
        homeFrame.grid_rowconfigure(i, weight=rowNums[i])
    for i in range(8):
        homeFrame.grid_columnconfigure(i, weight=columnNums[i], uniform="A")
    # img = PIL.Image.open("background.png")
    # resized = img.resize((100,100))
    # bgimage = PIL.ImageTk.PhotoImage(resized)
    # tk.Label(homeFrame, image=bgimage).grid(row=0,column=0)

def switchFrames(goTo : tk.Frame, hide : tk.Frame):
    hide.grid_forget()
    goTo.grid(row=0,column=0, sticky="nsew")

def backToHome(frame : tk.Frame):
    print("CHANGING FRAME TO HOME")

    for widget in frame.winfo_children():
        widget.grid_forget()

    frame.grid_forget()
    homeFrame.grid(row=0,column=0,sticky="nsew")

def start():
    homeFrame.grid(row=0,column=0, sticky="nsew")

    homeWeightsConfigure([1, 1, 3, 3, 3, 3], [3,1,2,1,1,2,1,3])
    
    root.mainloop()
