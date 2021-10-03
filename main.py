# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
sys.path.append('C:\\Users\\Sungjoon\\\libs')
import pandas as pd
import datetime
# from mpl_finance import candlestick2_ohlc
import pandas_datareader.data as web
from Calculator import Calculator
from Telegram import Telegram
from CurrentValueReader import CurrentValueReader
from KrxReader import KrxReader
from Daily.HKParser import HKParser
from Daily.ThemaParser import ThemaParser

def main():
    telg = Telegram()
    end = datetime.datetime.now()#- datetime.timedelta(hours=12)
    start = end - datetime.timedelta(days=120)
    message =''
    calc = Calculator()
    # dart = dartConnect()
    hk = HKParser()
    thema = ThemaParser()

    currentValue = CurrentValueReader()
    krx = KrxReader()
    if (int(end.strftime('%H')) >= 17) and (int(end.strftime('%H')) <= 24) or (int(end.strftime('%H')) >= 0) and (int(end.strftime('%H')) < 9) :
        stock_market = '미국'
        stock_list = ['^GSPC','^IXIC','^DJI','^RUT', 'AAPL', 'NVDA', 'DNMR','TEAM','PLUG','BARK','KRBN','CROX']
        # stock_list = ['DNMR']
    else :
        stock_market = '한국'
        stock_list = ['DL이앤씨','에이스토리','카카오','네이버','SK이노베이션','와이엔텍','SK케미칼','에코프로비엠','DB하이텍','효성첨단소재','상아프론테크','에코프로비엠','엘앤에프']
    now_Data = []
    company_trade_value = pd.DataFrame()
    for stock in stock_list :
        try :
            if stock_market =='미국':
                company_stock = web.DataReader(stock, "yahoo", start, end)
                now_Data = calc.stock_listup(company_stock, stock, company_trade_value,stock_market)
                message = message + telg.america_message_Parsing(now_Data)

            elif stock_market =='한국' :
                company_code = currentValue.get_stock_code(stock)
                company_stock = krx.get_stock_data(start, end, company_code)
                company_trade_value = krx.get_market_trade_value(start, end, company_code)
                now_Data = calc.stock_listup(company_stock, stock, company_trade_value,stock_market)
                message = message + telg.message_Parsing(now_Data)

        except Exception as e:  # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            print('예외가 발생했습니다.', e)

    print(message)
    # telg.auto_message(message)

if __name__ == "__main__":
    main()