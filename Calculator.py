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

    def calcRSI(self,stock_ds, date_index):
        U = np.where(stock_ds.diff(1)['Close'] > 0, stock_ds.diff(1)['Close'],0)  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
        D = np.where(stock_ds.diff(1)['Close'] < 0, stock_ds.diff(1)['Close'] * (-1),0)  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
        AU = pd.DataFrame(U, index=date_index).rolling(window=self.period).mean()  # AU, period=14일 동안의 U의 평균
        AD = pd.DataFrame(D, index=date_index).rolling(window=self.period).mean()  # AD, period=14일 동안의 D의 평균
        rsi = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
        signal = rsi.rolling(window=9).mean()
        rsi.columns = ['rsi']
        rsi['signal'] = signal
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

        return now_Data

    def stock_listup(self,stock_ds,stock_name,company_trade_value) :
        judge_data = pd.DataFrame()

        judge_data = self.calcBOL(stock_ds)
        judge_data = judge_data.join(self.calcBOL_80(stock_ds))
        judge_data['close'] = stock_ds['Close']
        judge_data = judge_data.join(self.calcRSI(stock_ds, stock_ds.index))
        judge_data = judge_data.join(company_trade_value)
        judge_data = judge_data.reset_index()
        judge_data['ticker'] = stock_name

        now_Data = self.calcVolumn(judge_data)


        return now_Data
