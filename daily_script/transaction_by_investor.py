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

data_list5 = [['원유','POILWTIUSDM']
             ,['금','GOLDAMGBD228NLBM']
             ]

data_list6 = [['은','LBMA/SILVER','quandl']
             ,['구리','LME/PR_CU''quandl']
             ]


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
fig, axs = plt.subplots(len(data_list)+len(data_list2)+len(data_list5),\
            constrained_layout=True,figsize=(15,15))
index = 0
fig.suptitle(end, fontsize=16)
#%%
for name,ticker in data_list :
    date = fdr.DataReader(ticker, start=start)
    color = 'red' if (date['Close'][-1]-date['Close'][-2])/date['Close'][-2] >0 else 'blue'
    calculator = '+' if (date['Close'][-1]-date['Close'][-2])/date['Close'][-2] >0 else ''
    
    
    print(index)
    axs[index].plot(date['Close'].copy(),color)
    axs[index].set_title(str(name)  + ' : ' + str(date['Close'][-1]) +'('+\
                         calculator +\
                         str(round((date['Close'][-1]-date['Close'][-2])/date['Close'][-2] * 100,2))+'%)', fontsize=13,fontweight="bold")
    # value_list = value_list + [daily_calc(date,name)]
    index += 1
#%%
for name,ticker in data_list2 :
    data = fdr.DataReader(ticker, start=start, data_source='fred')
    data['Close'] = data[ticker]
    
    print(index)
    axs[index].plot(data['Close'].copy(),color = color)
    axs[index].set_title(str(name)  + ' : ' + str(data['Close'][-1]) +'('+\
                         calculator +\
                         str(round((data['Close'][-1]-data['Close'][-2])/data['Close'][-2] * 100,2))+'%)', fontsize=13,fontweight="bold")
    index += 1

#%%
for name,ticker in data_list5 :
    data = pdr.DataReader(ticker, start=start, data_source='fred')
    data['Close'] = data[ticker]
    data = data.dropna()
    
    print(index)
    axs[index].plot(data['Close'].copy(),color = color)
    axs[index].set_title(str(name)  + ' : ' + str(data['Close'][-1]) +'('+\
                         calculator +\
                         str(round((data['Close'][-1]-data['Close'][-2])/data['Close'][-2] * 100,2))+'%)', fontsize=13,fontweight="bold")
    index += 1



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