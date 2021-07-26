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
from dartConnect import dartConnect
from CurrentValueReader import CurrentValueReader
from KrxReader import KrxReader

def main():
    telg = Telegram()
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=120)
    message =''
    calc = Calculator()
    # dart = dartConnect()
    currentValue = CurrentValueReader()
    krx = KrxReader()
    stock_list = [['코스피','한국'],['코스닥','한국'],['SK이노베이션','한국'],['에이스토리','한국'],['DL이앤씨','한국']]

    for stock, stock_market in stock_list :
        try :
            # a = dart.get_company_code("삼성전자")
            company_code = currentValue.get_stock_code(stock)
            if stock_market =='미국':
                company_stock = web.DataReader('CROX', "yahoo", start, end)
            elif stock_market =='한국' :
                company_stock = krx.get_stock_data(start, end, company_code)

            company_trade_value = krx.get_market_trade_value(start, end, company_code)

            now_Data = calc.stock_listup(company_stock,stock,company_trade_value)
            message = message + telg.message_Parsing(now_Data)

        except Exception as e:  # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            print('예외가 발생했습니다.', e)

    print(message)
    telg.auto_message(message)

if __name__ == "__main__":
    main()