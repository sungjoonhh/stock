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


# def graph():
#     # 차트 레이아웃을 설정
#     fig = plt.figure(figsize=(10,10)) #최초의 창 크기를 10x10으로 설정, 크기를 설정하지 않으면 아무 것도 나오지 않음

#     #ax_main 실제로 데이터가 그려지는 영역
#     ax_main = fig.add_subplot(1,1,1) #1,1,1의 의미는 전체 창을 1x1로 쪼개고 ax_main을 생성한다는 뜻

#     # x축에 쓰일 날짜 값 조정
#     def x_date(x,pos):
#         try:
#             return index[int(x-0.5)][:7] # 0:6까지만 잘라서 2019-01와 같이 표현
#         except IndexError:
#             return ''

#     # x축을 조정
#     ax_main.xaxis.set_major_locator(ticker.MaxNLocator(10))
#     ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(x_date))

#     # 메인차트를 그리기
#     ax_main.set_xlabel('Date')
#     ax_main.plot(index, ma20, label='MA20') #20일선 표시
#     ax_main.plot(index, bol_upper, label='bol_upper') #60일선 표시
#     ax_main.plot(index, bol_down, label='bol_down') #60일선 표시
#     ax_main.set_title('HT. S Stock ',fontsize=22) #차트의 Title 설정
#     ax_main.set_xlabel('Date') #차트의 x축 label을 설정
#     #캔들 차트를 실제로 구성하는 부분
#     candlestick2_ohlc(ax_main,ds['Open'],ds['High'],ds['Low'],ds['Close'], width=0.5, colorup='r', colordown='b')

#     ax_main.legend(loc=5) #차트 범례를 오른쪽에 위치하도록 설정
#     plt.grid()
#     plt.show()
