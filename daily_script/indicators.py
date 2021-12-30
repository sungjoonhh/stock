# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 21:57:00 2021

@author: sungjoon
"""
import sys
sys.path.append('C:\\Users\\sungjoon\\libs')
sys.path.append('C:\\Users\\sungjoon\\GIT\\stock')
import FinanceDataReader as fdr
#pip install -U finance-datareader
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as pdr
from FileReader import FileReader
import telegram
import dataframe_image as dfi
import matplotlib
import datetime
from pykrx import stock

plt.rc('font', family='Malgun Gothic')


#%%
def daily_calc(df,name):
    df['Close_YD'] = df['Close'].shift(1)
    df_tail = df.tail(1)

    return name, df_tail['Close'].values[0], round(((df_tail['Close'] - df_tail['Close_YD'])/df_tail['Close_YD']).values[0]*100,2)
#%%


data_list = [['달러','USD/KRW']
             ,['코스피','KS11']
             ,['코스닥','KQ11']
             ,['비트코인','BTC/KRW']
             ,['S&P500','US500']
             ,['나스닥','IXIC']
             ,['공포지수','VIX']
             ]


data_list2 = [['미국채 10년물','DGS10']
             ,['미국채 2년물','DGS2']
             ]

# data_list3 = [['코스피 PER','1001'],
#               ['코스닥 PER','2001']]

# data_list4 = [['코스피 PBR','1001'],
#               ['코스닥 PBR','2001']]


#%%
filereader = FileReader()
telg_dict = filereader.read_data('C:\\Users\\sungjoon\\libs\\telegram.txt')
token = telg_dict['token']
chat_id = telg_dict['chat_id']
bot = telegram.Bot(token=token)

chat_id = chat_id


end = datetime.datetime.now().strftime('%Y-%m-%d')
start = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')

current_day = datetime.datetime.now().strftime('%Y%m%d')
#%%
fig, axs = plt.subplots(len(data_list)+len(data_list2),\
             #+len(data_list3)+len(data_list4),\
            constrained_layout=True,figsize=(15,15))
index = 0
for name,ticker in data_list :
    date = fdr.DataReader(ticker, start=start)
    print(index)
    axs[index].plot(date['Close'].copy())
    axs[index].set_title(str(name)  + ' : ' + str(date['Close'].tail(1).values[0]))
    # value_list = value_list + [daily_calc(date,name)]
    index += 1
    

for name,ticker in data_list2 :
    data = fdr.DataReader(ticker, start=start, data_source='fred')
    data['Close'] = data[ticker]
    axs[index].plot(data['Close'].copy())
    axs[index].set_title(str(name) + ' : ' + str(data['Close'].tail(1).values[0]))
    index += 1
    # value_list = value_list + [daily_calc(data,name)]


# for name,ticker in data_list3 :
#     data = stock.get_index_fundamental(start, end, ticker)
#     data['PER'] = data['PER']
#     axs[index].plot(data['PER'].copy())
#     axs[index].set_title(str(name) + ' : ' + str(data['PER'].tail(1).values[0]))
#     index += 1
     
# for name,ticker in data_list4 :
#     data = stock.get_index_fundamental(start, end, ticker)
#     data['PBR'] = data['PBR']
#     axs[index].plot(data['PBR'].copy())
#     axs[index].set_title(str(name) + ' : ' + str(data['PBR'].tail(1).values[0]))
#     index += 1

plt.savefig('C:\\Users\\sungjoon\\GIT\\stock\\daily_script\\indicator_image\\{date}.png'.format(date=current_day),dpi=300)

bot.send_photo(chat_id, caption = '지수', photo=open(
    'C:\\Users\\sungjoon\\GIT\\stock\\daily_script\\indicator_image\\{date}.png'.format(date=current_day), 'rb'))


#%%

# telegram_txt = ''
# for value in value_list :
#     telegram_txt += '종목 : {}\t 종가 : {}\t 변동 : {}\n'.format(value[0],value[1],value[2])
    



# # bot.sendMessage(chat_id, text=telegram_txt)


# #%%
# from pykrx import stock
# df = stock.get_index_fundamental("2021-01-01", "2021-12-10", "2001")       

# df = stock.get_index_fundamental("20211122")       


# #%%
# # start += datetime.timedelta(days=1)
# fig, axs = plt.subplots(2,2)
# fig.suptitle('Vertically stacked subplots')
# axs[0,0].plot = date['Close'].plot().copy()
# axs[0,1].plot = date['Close'].plot().copy()
#%%

#%%
# graph = USD_KRX.loc[:,'Close'].plot()
# graph.axhline(1050, ls='--', color='r')#1050선
# graph.axhline(1150, ls='--', color='r')#1150선

#%%
# KOSPI
# KOSPI = fdr.DataReader('KS11', start = '2020-11-30')
# KOSPI_data = daily_calc(KOSPI)
# KOSPI ['Close'].plot()

# #%%
# KOSDAQ = fdr.DataReader('KQ11', start = '2020-11-29')
# print(daily_calc(KOSDAQ))
# KOSDAQ['Close'].plot()
# #%%

# # BITCOIN
# BIT = fdr.DataReader('BTC/KRW', start = '2020-11-29')
# print(daily_calc(BIT))
# BIT['Close'].plot()

# #%%

# # S&P500
# SP500 = fdr.DataReader('US500', start = '2020-11-29')
# print(daily_calc(SP500))
# SP500['Close'].plot()

# #%%
# # NASDAQ
# NASDAQ = fdr.DataReader('IXIC', start = '2020-11-29')
# print(daily_calc(NASDAQ))
# NASDAQ['Close'].plot()
# #%%

# # VIX 
# VIX = fdr.DataReader('VIX', start = '2020-11-20',end='2021-11-29')#VIX(변동성 지수)
# print(daily_calc(VIX))

# graph = VIX['Close'].plot()
# graph.axhline(20, ls='--', color='r')#20선

# #%%

# #AMERICAN GOVERMENT BOND (10)
# DGS10 = fdr.DataReader('DGS10', start = '2020-11-20', data_source='fred') 
# DGS10 ['Close'] = DGS10['DGS10']
# print(daily_calc(DGS10))

# graph= DGS10.plot()
# graph.axhline(1.5, ls='--', color='r')


# #AMERICAN GOVERMENT BOND (2)
# DGS2 = fdr.DataReader('DGS2', start = '2020-11-20', data_source='fred') 
# print(daily_calc(DGS2))

# graph= DGS2.plot()
# graph.axhline(1.5, ls='--', color='r')

# #%%
# index_list = [['KOSPI','KS11'],['S&P','US500']]

# df_list = [fdr.DataReader(code,'2021-01-01')['Close'] for name,code in index_list]
# df = pd.concat(df_list, axis=1)
# df.columns = [name for name, code in index_list]
# df_plot = df / df.iloc[0] - 1.0
# df_plot.plot()
# #%%


# #%%
# df = DGS['DGS10']