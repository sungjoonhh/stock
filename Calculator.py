# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 15:37:43 2021

@author: SUNGJOON
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
from CurrentValueReader import CurrentValueReader

# 차트를 이룰 데이터 가져오기, 2019 1.1 ~ 2019.11.1 기간의 삼성전자 주가 정보 갖고 오기

class Calculator:
    def __init__(self):
        self.period = 14

    def calcRSI2(self,stock_ds, date_index):
        U = np.where(stock_ds.diff(1)['Close'] > 0, stock_ds.diff(1)['Close'],0)                                                # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
        D = np.where(stock_ds.diff(1)['Close'] < 0, stock_ds.diff(1)['Close'] * (-1),0)                                         # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
        AU = (pd.DataFrame(U, index=date_index).rolling(window=self.period).sum() + pd.DataFrame(U, index=date_index))/14       # AU, period=14일 동안의 U의 평균
        TU = pd.DataFrame(U, index=date_index)
        AD = (pd.DataFrame(D, index=date_index).rolling(window=self.period).sum() + pd.DataFrame(D, index=date_index))/14       # AD, period=14일 동안의 D의 평균
        TD =pd.DataFrame(D, index=date_index)
        rsi = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
        # rsi = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
        signal = rsi.rolling(window=9).mean()
        rsi.columns = ['rsi']
        rsi['signal'] = signal
        return rsi

    def calcRSI(self,stock_ds, date_index, ema=True):
        close_delta = stock_ds['Close'].diff()

        # Make two series: one for lower closes and one for higher closes
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)

        if ema:
            # Use exponential moving average
            ma_up = up.ewm(com=self.period - 1, adjust=True, min_periods=self.period).mean()
            ma_down = down.ewm(com=self.period - 1, adjust=True, min_periods=self.period).mean()
        else:
            # Use simple moving average
            ma_up = up.rolling(window=self.period, adjust=False).mean()
            ma_down = down.rolling(window=self.period, adjust=False).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100 / (1 + rsi))
        rsi = pd.DataFrame(rsi)
        rsi.columns = ['rsi']
        return rsi


    def calcBOL(self,stock_ds):
        judge_data = pd.DataFrame()
        ma20 = stock_ds['Close'].rolling(window=20).mean()  # 20일 이동평균값
        bol_upper = ma20 + 2 * stock_ds['Close'].rolling(window=20).std()  # BB(볼린저밴드) 상단 밴드
        bol_down = ma20 - 2 * stock_ds['Close'].rolling(window=20).std()  # BB(볼린저밴드) 하단 밴드

        judge_data['bol_upper_20'] = bol_upper
        judge_data['bol_mid_20'] = ma20
        judge_data['bol_down_20'] = bol_down

        return judge_data

    def calcBOL_80(self,stock_ds):
        judge_data = pd.DataFrame()
        ma80 = stock_ds['Close'].rolling(window=80).mean()  # 20일 이동평균값
        bol_upper = ma80 + 2 * stock_ds['Close'].rolling(window=80).std()  # BB(볼린저밴드) 상단 밴드
        bol_down = ma80 - 2 * stock_ds['Close'].rolling(window=80).std()  # BB(볼린저밴드) 하단 밴드

        judge_data['bol_upper_80'] = bol_upper
        judge_data['bol_mid_80'] = ma80
        judge_data['bol_down_80'] = bol_down

        return judge_data



    def calcVolumn(self,stock_ds):
        period = [1,3,7]
        agency_list = []
        foreigner_list= []
        ant_list = []
        for i in period:
            agency_list += [str(round(pd.to_numeric(stock_ds['agency']).rolling(i).sum().iloc[-1]/1000,1))+'K'+'(' + str(i)+'일)']
            foreigner_list += [str(round(pd.to_numeric(stock_ds['foreigner']).rolling(i).sum().iloc[-1]/1000,1))+'K' + '('+str(i)+'일)']
            ant_list += [str(round(pd.to_numeric(stock_ds['ant']).rolling(i).sum().iloc[-1] / 1000,1)) + 'K'+'(' + str(i) + '일)']

        now_Data = stock_ds.copy().iloc[-1]
        now_Data['foreigner'] = "[" + ", ".join(foreigner_list) + "]"
        now_Data['agency'] = "[" + ", ".join(agency_list) + "]"
        now_Data['ant'] = "[" + ", ".join(ant_list) + "]"
        now_Data = now_Data.dropna(axis=0)
        return now_Data

    def stock_listup(self,stock_ds,stock_name,company_trade_value,stock_market) :
        judge_data = pd.DataFrame()

        judge_data = self.calcBOL(stock_ds)
        judge_data = judge_data.join(self.calcBOL_80(stock_ds))
        judge_data['close'] = stock_ds['Close']
        judge_data = judge_data.join(self.calcRSI(stock_ds, stock_ds.index))
        judge_data = judge_data.join(company_trade_value)
        judge_data = judge_data.reset_index()
        judge_data.at[judge_data.index[-1], ['agency', 'etc', 'ant', 'foreigner', 'all']] = judge_data.iloc[-2][['agency', 'etc', 'ant', 'foreigner', 'all']].tolist()
        judge_data.iloc[-1]['rsi'] = judge_data.iloc[-2][['rsi']].tolist()

        judge_data['ticker'] = stock_name


        if stock_market =='한국' :
            judge_data = self.calcVolumn(judge_data)

        else :
            judge_data = judge_data.iloc[-1]

        return judge_data
