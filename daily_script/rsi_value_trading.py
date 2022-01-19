# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 21:40:26 2021

@author: user
"""
import pandas as pd
import pykrx
from pykrx import stock
import datetime
import sys

sys.path.append('C:\\Users\\sungjoon\\libs')
sys.path.append('C:\\Users\\sungjoon\\GIT\\stock')
from postLib import PostgresDataClass
# from Telegram import Telegram
from FileReader import FileReader
import telegram
import dataframe_image as dfi

# %%

# telg = Telegram()
high_value_list = [26]
end = datetime.datetime.now()
start = end - datetime.timedelta(days=0)
post = PostgresDataClass('192.168.0.3', 'stock', 'postgres', 'tjdwns00!')




def calcRSI(stock_ds, period, ema=True):
    stock_ds =stock_ds.sort_values('update_time')
 
    close_delta = stock_ds['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema:
        # Use exponential moving average
        ma_up = up.ewm(com=period - 1, adjust=True, min_periods=period).mean()
        ma_down = down.ewm(com=period - 1, adjust=True, min_periods=period).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=period, adjust=False).mean()
        ma_down = down.rolling(window=period, adjust=False).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    stock_ds['rsi'] = pd.DataFrame(rsi)
    return stock_ds

#%%
while start <= end:
        current_day = start.strftime('%Y%m%d')


        # %%
        rsi_value_df = post.select_dataframe("""
                select b.company_name,a.* 
                from krx.daily_market a
                left join krx.company_ticker b
                on a.ticker = b.ticker  
            where a.update_time > timestamp'{update_time}' - interval '6' month
            order by ticker 
        """.format(update_time=current_day))
    
            
    
        unique_value = rsi_value_df[['ticker','company_name']].drop_duplicates()
        unique_value = unique_value.reset_index()
    
        data_df = pd.DataFrame()
        for i,rows in unique_value.iterrows() :
            print(str(i) + ' / ' + str(len(unique_value))+ ' : ' + str(rows['company_name']))
            b = rsi_value_df[rsi_value_df['ticker'] == rows['ticker']]
            data_df  = data_df.append(calcRSI(b,14))
            
        kkk = data_df[(data_df['rsi']<30) &(data_df['update_time']=='2022-01-19')]
        kkkkk = kkk[kkk ['transaction_amount']>10000000000]
    

        # %%
        # high_name_html = '<pre>' + high_name_df.to_html() + '</pre>'

        # filereader = FileReader()
        # telg_dict = filereader.read_data('C:\\Users\\sungjoon\\libs\\telegram.txt')
        # token = telg_dict['token']
        # chat_id = telg_dict['chat_id']
        # bot = telegram.Bot(token=token)

        # chat_id = chat_id
        # bot.send_photo(chat_id, caption = '{high_value}주 신고가'.format(high_value = high_value), photo=open(
        #     'C:\\Users\\sungjoon\\GIT\\stock\\daily_script\\{high_name}_image\\{date}.png'.format(date=current_day,high_name=high_name,high_value = high_value), 'rb'))

        # del [[high_name_df]]
    start += datetime.timedelta(days=1)
