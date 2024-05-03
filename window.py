import yfinance as yf
import tkinter as gui
import time

class Window:
    frame = gui.Tk()

    def __init__(self, name):
        self.frame.title(name)

    def start(self):
        self.frame.mainloop()

    def newLabel(self, xPos, yPos, contents):
        label = gui.Label(self.frame, )