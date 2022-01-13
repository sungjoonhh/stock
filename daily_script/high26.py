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


while start <= end:
    for high_value in high_value_list :
        print(high_value)
        high_name = 'high'+ str(high_value)
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


        print(current_day)
        post.execute("""insert into krx.daily_{high_name}
            select c.*,d.{high_name}
            from (select b.company_name,a.ticker,a.close,a.update_time
            from krx.daily_market a
            left join krx.company_ticker b
            on a.ticker = b.ticker
            where a.update_time = timestamp'{date}'
            and a.open !=0
            ) c
            left join (
                select ticker,max(close) as {high_name}
                from krx.daily_market 
                where update_time >timestamp'{date}' - interval '{high_value} week'
                group by ticker
            )d
            on c.ticker = d.ticker
            where close = {high_name}
            on conflict do nothing""".format(date=current_day,high_name= high_name, high_value = high_value))

        # %%
        high_name_df = post.select_dataframe("""
            select e.company_name as 회사,e.close as 종가,round(f.rate::numeric,2)::varchar || '%' as 수익률,e.cnt as 횟수 ,f.ranking as 거래순위 ,e.update_time as 날짜,e.thema as 테마
            from (select array_agg(d.thema_name) as thema,c.company_name,c.ticker,c.close,c.update_time,c.{high_name},concat(c.cnt::varchar, '/{high_value}') as cnt
            from (
                select a.*,b.cnt
                from krx.daily_{high_name} a
                left join (
                    select company_name,ticker,count(*) as cnt
                    from krx.daily_{high_name} 
                    where update_time <= timestamp '{update_time}'
            and update_time >= timestamp '{update_time}' - interval '{high_value}' day
            --and company_name ='효성첨단소재'
                group by company_name,ticker
            )b
            on a.ticker =b.ticker
            where a.update_time = timestamp '{update_time}'
            )c
            left join stock.thema_stock d
            on c.company_name = d.company_name
            group by c.company_name,c.ticker,c.close,c.update_time,c.{high_name},c.cnt
            )e
            left join (
                select *,dense_rank() over (order by transaction_amount desc) as ranking
                from krx.daily_market 
                where update_time = timestamp '{update_time}'
            )f
            on e.ticker = f.ticker 
            where rate !=0
            order by rate desc
            """.format(update_time=current_day,high_name=high_name,high_value = high_value))
        dfi.export(high_name_df,
                'C:\\Users\\sungjoon\\GIT\\stock\\daily_script\\{high_name}_image\\{date}.png'.format(date=current_day,high_name=high_name,high_value = high_value),
                max_cols=-1, max_rows=-1)

        # %%

        # lst = []
        # for ticker in stock.get_market_ticker_list(market='KOSDAQ'):
        #         company = stock.get_market_ticker_name(ticker)
        #         lst = lst + [(ticker,company)]

        #         #%%

        # post = PostgresDataClass('192.168.0.3','stock','postgres','tjdwns00!')
        # post.insert_list(lst, 'krx.company_ticker')

        high_name_html = '<pre>' + high_name_df.to_html() + '</pre>'

        filereader = FileReader()
        telg_dict = filereader.read_data('C:\\Users\\sungjoon\\libs\\telegram.txt')
        token = telg_dict['token']
        chat_id = telg_dict['chat_id']
        bot = telegram.Bot(token=token)

        chat_id = chat_id
        bot.send_photo(chat_id, caption = '{high_value}주 신고가'.format(high_value = high_value), photo=open(
            'C:\\Users\\sungjoon\\GIT\\stock\\daily_script\\{high_name}_image\\{date}.png'.format(date=current_day,high_name=high_name,high_value = high_value), 'rb'))

        del [[high_name_df]]
    start += datetime.timedelta(days=1)
