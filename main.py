# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
sys.path.append('C:\\Users\\user\\Anaconda3\\libs')
import postLib
import pandas as pd
import numpy as np
import datetime
from mpl_finance import candlestick2_ohlc
import pandas_datareader.data as web
from Calculator import Calculator
from Telegram import Telegram
def main():
    telg = Telegram()
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=60)
    calc = Calculator()


    stock_ds = web.DataReader("005930.KS", "yahoo", start, end)

    judge_data = pd.DataFrame()
    judge_data = calc.calcBOL(stock_ds)

    rsi = calc.calcRSI(stock_ds, stock_ds.index)  # web.DataReader를 통해 받았던 원래 DataFrame에 'RSI'열을 추가
    judge_data = judge_data.join(rsi)
    judge_data = judge_data.reset_index()
    endD = end.strftime('%Y-%m-%d %H:%M:%S')
    now_Data = judge_data[judge_data['Date']==endD]
    # now_Data['ticker'] = '삼성전자'
    # telg.auto_message(now_Data.to_string())


if __name__ == "__main__":
    main()