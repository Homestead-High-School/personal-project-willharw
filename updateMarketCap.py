import yfinance as yf
import tkinter as tk
#use this to update market cap data for all stocks in stocksnomarketcap.txt and put it in stocks.txt
def updateStocksTxt(frame = tk.Frame):
    file = open("stocksnomarketcap.txt")
    file2 = open("stocks.txt", "w")
    list = file.readlines()
    currentStock = tk.Label(frame, bg="white", text="Starting...")
    currentStock.grid(row=2,column=0)
    for i in list:
        line = i.strip()
        stock = line.split("|")[0].strip()
        print(stock)
        ticker = yf.Ticker(stock)
        try:
            temp = ticker.info["marketCap"]
            try: 
                temp2 = ticker.info["shortName"]
                line += "|"+temp2+"|"+str(temp)
            except:
                line += "|"+"NOTFOUND"+"|"+str(temp)
        except:
            try:
                temp = ticker.info["shortName"]
                line += "|"+temp+"|"+"NOTFOUND"
            except:
                line += "|"+"NOTFOUND"+"|"+"NOTFOUND"
        currentStock.config(text=stock)
        print(line)
        file2.write(line +"\n")

# sectors = []
# for i in list:
#     sector = i.split("|")[1].strip()
#     if not (sector in sectors):
#         sectors.append(sector)
# print(sectors)