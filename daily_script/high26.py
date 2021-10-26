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
end = datetime.datetime.now()
start = end - datetime.timedelta(days=0)
post = PostgresDataClass('192.168.0.3', 'stock', 'postgres', 'tjdwns00!')
while start <= end:
    current_day = start.strftime('%Y%m%d')

    df = stock.get_market_ohlcv_by_ticker(current_day, market="KOSPI")
    df['market'] = 'KOSPI'
    df = df.reset_index()
    df = df[df['종가'] != 0]

    df1 = stock.get_market_ohlcv_by_ticker(current_day, market="KOSDAQ")
    df1['market'] = 'KOSDAQ'
    df1 = df1.reset_index()
    df1 = df1[df1['종가'] != 0]

    df = df.append(df1)
    df['update_time'] = start.date()

    tuples = [tuple(x) for x in df.values.tolist()]

    post.insert_list(tuples, 'krx.daily_market')
    del [[df]]
    del [[df1]]

    start += datetime.timedelta(days=1)

    print(current_day)
    post.execute("""insert into krx.daily_high26
        select c.*,d.high26
        from (select b.company_name,a.ticker,a.close,a.update_time
        from krx.daily_market a
        left join krx.company_ticker b
        on a.ticker = b.ticker
        where a.update_time = timestamp'{date}'
        and a.open !=0
        ) c
        left join (
        	select ticker,max(close) as high26
        	from krx.daily_market 
        	where update_time >timestamp'{date}' - interval '26 week'
        	group by ticker
        )d
        on c.ticker = d.ticker
        where close = high26
        on conflict do nothing""".format(date=current_day))

    # %%
    high26_df = post.select_dataframe("""
        select e.*,f.ranking
        from (select array_agg(d.thema_name) as thema,c.company_name,c.ticker,c.close,c.update_time,c.high26,c.cnt
        from (
            select a.*,b.cnt
            from krx.daily_high26 a
            left join (
                select company_name,ticker,count(*) as cnt
                from krx.daily_high26
                where update_time <= timestamp '{update_time}'
                and update_time >= timestamp '{update_time}' - interval '14 day'
                --and company_name ='효성첨단소재'
                group by company_name,ticker
            )b
            on a.ticker =b.ticker
            where a.update_time = timestamp '{update_time}'
        )c
        left join stock.thema_stock d
        on c.company_name = d.company_name
        group by c.company_name,c.ticker,c.close,c.update_time,c.high26,c.cnt
        )e
        left join (
            select *,dense_rank() over (order by transaction_amount desc) as ranking
            from krx.daily_market 
            where update_time = timestamp '{update_time}'
        )f
        on e.ticker = f.ticker 
        order by cnt desc
        """.format(update_time=current_day))
    dfi.export(high26_df,
               'C:\\Users\\sungjoon\\GIT\\stock\\daily_script\\high26_image\\{date}.png'.format(date=current_day),
               max_cols=-1, max_rows=-1)

    # %%

    # lst = []
    # for ticker in stock.get_market_ticker_list(market='KOSDAQ'):
    #         company = stock.get_market_ticker_name(ticker)
    #         lst = lst + [(ticker,company)]

    #         #%%

    # post = PostgresDataClass('192.168.0.3','stock','postgres','tjdwns00!')
    # post.insert_list(lst, 'krx.company_ticker')

    high26_html = '<pre>' + high26_df.to_html() + '</pre>'

    filereader = FileReader()
    telg_dict = filereader.read_data('C:\\Users\\sungjoon\\libs\\telegram.txt')
    token = telg_dict['token']
    chat_id = telg_dict['chat_id']
    bot = telegram.Bot(token=token)

    chat_id = chat_id
    print(high26_html)
    bot.send_photo(chat_id, caption = '26주 신고가', photo=open(
        'C:\\Users\\sungjoon\\GIT\\stock\\daily_script\\high26_image\\{date}.png'.format(date=current_day), 'rb'))
