import yfinance as yf 
import pandas as pd 

tickerSymbol = "TSLA"

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='10y', interval='1d')

print(tickerDf.tail())