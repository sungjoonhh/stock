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


def main():
    telg = Telegram()
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=120)
    message =''
    calc = Calculator()
    # dart = dartConnect()
    currentValue = CurrentValueReader()

    stock_list = [['삼성전자','코스피'],["SK",'코스피'],['DL이앤씨','코스피'],["하이브",'코스피']]
    for stock, stock_index in stock_list :
        try :
            # a = dart.get_company_code("삼성전자")
            company_list = currentValue.get_stock_code(stock,stock_index)
            stock_ds = web.DataReader(company_list, "yahoo", start, end)


            table = calc.supply_toDatFrame(company_list)
            now_Data = calc.stock_listup(stock_ds,stock,table)
            message = message + telg.message_Parsing(now_Data)

        except Exception as e:  # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            print('예외가 발생했습니다.', e)

    print(message)
    telg.auto_message(message)

if __name__ == "__main__":
    main()