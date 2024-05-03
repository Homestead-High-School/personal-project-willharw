import yfinance as yf
import tkinter as gui
from tkinter import messagebox
import time

stock = yf.Ticker("TSLA")
#print(stock.info)

window = gui.Tk()
window.title("counting")
window.geometry("200x200")

def countDown():
    temp = int(entrybox.get())
    label = gui.Label(window, text=str(temp))
    label.pack()
    while temp>0:
        window.update()
        temp-=1
        time.sleep(1)
        label.config(text=str(temp))

entryVal = ""
entrybox = gui.Entry(window)
entrybox.place(x=50,y=100)
button = gui.Button(window, text="Start countdown", bd=10, command=countDown)
button.pack()
window.mainloop()