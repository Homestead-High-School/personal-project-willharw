import yfinance as yf

#use this to update market cap data for all stocks in stocksnomarketcap.txt and put it in stocks.txt
def update():
    file = open("stocksnomarketcap.txt")
    file2 = open("stocks.txt", "w")
    list = file.readlines()
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
        print(line)
        file2.write(line +"\n")

# sectors = []
# for i in list:
#     sector = i.split("|")[1].strip()
#     if not (sector in sectors):
#         sectors.append(sector)
# print(sectors)