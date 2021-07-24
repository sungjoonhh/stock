# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:06:23 2021

@author: SUNGJOON
"""
from pykrx import stock

class KrxReader :

    def stock_data_column_change(self, df):
        df = df[['고가', '저가', '시가', '종가', '거래량']]
        df.columns = ['High', 'Low', 'Open', 'Close', 'Volume']
        df.index.name = 'Date'
        return df


    def market_trade_value_column_change(self,df):
        df.columns = ['agency','etc','ant','foreigner','all']
        df.index.name = 'Date'
        return df


    def get_stock_data(self, start, end, company_code):
        if company_code == '1001' :
            return self.get_market_kospi( start, end, company_code)
        elif company_code == '2001' :
            return self.get_market_kosdaq( start, end, company_code)
        else :
            df = stock.get_market_ohlcv_by_date(start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), company_code)
            return self.stock_data_column_change(df)



    def get_market_kospi(self, start, end, company_code):
        df =stock.get_index_ohlcv_by_date(start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), "1001")

        return self.stock_data_column_change(df)

    def get_market_kosdaq(self, start, end, company_code):
        df =stock.get_index_ohlcv_by_date(start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), "2001")

        return self.stock_data_column_change(df)



    def get_market_trade_value(self, start, end, company_code):
        if company_code == '1001':
            company_code= 'KOSPI'
        elif company_code == '2001':
            company_code = 'KOSDAQ'

        df = stock.get_market_trading_volume_by_date(start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), company_code)

        return self.market_trade_value_column_change(df)