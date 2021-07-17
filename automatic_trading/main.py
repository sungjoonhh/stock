# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 15:37:43 2021

@author: SUNGJOON
"""

from mpl_finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas_datareader.data as web
import datetime
import pandas as pd
import numpy as np


# 차트를 이룰 데이터 가져오기, 2019 1.1 ~ 2019.11.1 기간의 삼성전자 주가 정보 갖고 오기


def calcRSI(stock_ds, period, date_index):
    U = np.where(stock_ds.diff(1)['Close'] > 0, stock_ds.diff(1)['Close'],
                 0)  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
    D = np.where(stock_ds.diff(1)['Close'] < 0, stock_ds.diff(1)['Close'] * (-1),
                 0)  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
    AU = pd.DataFrame(U, index=date_index).rolling(window=period).mean()  # AU, period=14일 동안의 U의 평균
    AD = pd.DataFrame(D, index=date_index).rolling(window=period).mean()  # AD, period=14일 동안의 D의 평균
    rsi = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    signal = rsi.rolling(window=9).mean()
    rsi.columns = ['rsi']
    rsi['signal'] = signal
    return rsi


def calcBOL(stock_ds):
    judge_data = pd.DataFrame()
    ma20 = stock_ds['Close'].rolling(window=20).mean()  # 20일 이동평균값
    bol_upper = ma20 + 2 * stock_ds['Close'].rolling(window=20).std()  # BB(볼린저밴드) 상단 밴드
    bol_down = ma20 - 2 * stock_ds['Close'].rolling(window=20).std()  # BB(볼린저밴드) 하단 밴드

    judge_data['bol_upper'] = bol_upper
    judge_data['bol_mid'] = ma20
    judge_data['bol_down'] = bol_down

    return judge_data


def main():
    start = datetime.datetime(2021, 3, 16)
    end = datetime.datetime(2021, 7, 16)
    stock_ds = web.DataReader("008770.KS", "yahoo", start, end)
    date_index = stock_ds.index
    period = 14

    judge_data = pd.DataFrame()
    judge_data = calcBOL(stock_ds)
    endD = end.strftime('%Y-%m-%d %H:%M:%S')

    rsi = calcRSI(stock_ds, period, date_index)  # web.DataReader를 통해 받았던 원래 DataFrame에 'RSI'열을 추가
    judge_data = judge_data.join(rsi)
    judge_data = judge_data.reset_index()


if __name__ == "__main__":
    main()

# %%

