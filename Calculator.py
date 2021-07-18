# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 15:37:43 2021

@author: SUNGJOON
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np


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


    def stock_listup(self,stock_ds,stock_name) :
        judge_data = pd.DataFrame()

        judge_data = self.calcBOL(stock_ds)
        bol_80 = self.calcBOL_80(stock_ds)
        judge_data = judge_data.join(bol_80)
        judge_data['close'] = stock_ds['Close']

        rsi = self.calcRSI(stock_ds, stock_ds.index)  # web.DataReader를 통해 받았던 원래 DataFrame에 'RSI'열을 추가
        judge_data = judge_data.join(rsi)
        judge_data = judge_data.reset_index()

        judge_data['ticker'] = stock_name
        now_Data = judge_data.iloc[-1]

        return now_Data


    # %%

