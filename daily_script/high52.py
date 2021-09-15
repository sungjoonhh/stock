# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 21:40:26 2021

@author: user
"""
import pykrx
from pykrx import stock
import datetime
import sys
sys.path.append('C:\\Users\\user\\Anaconda3\\libs')

from postLib import  PostgresDataClass



#%%


end = datetime.datetime.now()
start = end - datetime.timedelta(days=0)
post = PostgresDataClass('192.168.0.3','stock','postgres','tjdwns00!')
while start <= end :
    current_day = start.strftime('%Y%m%d')
    
    
    
    df = stock.get_market_ohlcv_by_ticker(current_day, market="KOSPI")
    df['market']='KOSPI'
    df = df.reset_index()
    df = df[df['종가']!=0]
    
    
    df1 = stock.get_market_ohlcv_by_ticker(current_day, market="KOSDAQ")
    df1['market']='KOSDAQ'
    df1 = df1.reset_index()
    df1 = df1[df1['종가']!=0]
    
    
    
    
    df = df.append(df1)
    df['update_time'] = start.date()

    tuples = [tuple(x) for x in df.values.tolist()]

    post.insert_list(tuples, 'krx.daily_market')
    del [[df]]
    del [[df1]]
    
    start += datetime.timedelta(days=1)






    print(current_day)
    post.execute("""insert into krx.daily_high52
        select c.*,d.high52
        from (select b.company_name,a.ticker,a.close,a.update_time
        from krx.daily_market a
        left join krx.company_ticker b
        on a.ticker = b.ticker
        where a.update_time = timestamp'{date}'
        ) c
        left join (
        	select ticker,max(close) as high52
        	from krx.daily_market 
        	where update_time >timestamp'{date}' - interval '52 week'
        	group by ticker
        )d
        on c.ticker = d.ticker
        where close = high52
        on conflict do nothing""".format(date = current_day))

#%%

    post.execute("""		insert into krx.daily_high52 
        select c.*,d.high52 
        from (
	        select b.company_name,a.ticker,a.close,a.update_time
	        from krx.daily_market a
	        left join krx.company_ticker b
	        on a.ticker = b.ticker
	        where a.open !=0
        ) c
        left join (
        	select ticker,update_time, max(close) over (partition by ticker order by update_time asc rows between 364 preceding and current ROW) as high52
        	from krx.daily_market 
        )d
        on c.ticker = d.ticker
        and c.update_time = d.update_time
        where c.update_time > timestamp '{date}' - interval '52 week'
        and c.close = d.high52
        on conflict do nothing 
        """.format(date= current_day))






#%%


# lst = []
# for ticker in stock.get_market_ticker_list(market='KOSDAQ'):
#         company = stock.get_market_ticker_name(ticker)
#         lst = lst + [(ticker,company)]

#         #%%
        
# post = PostgresDataClass('192.168.0.3','stock','postgres','tjdwns00!')
# post.insert_list(lst, 'krx.company_ticker')






