# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 14:50:11 2022

@author: sungjoon
"""
import pandas_datareader as pdr
import pandas_datareader.data as web
import datetime
import sys
import pandas as pd




sys.path.append('C:\\Users\\sungjoon\\libs')
sys.path.append('C:\\Users\\sungjoon\\GIT\\stock')




ticker_list = ['AAPL','MSFT','GOOG','AMZN','FB','TSM','TSLA','NVDA','JPM','ASML','NFLX','NKE','PFE','MRNA','QCOM','SBUX',
'AMD','TEAM','GM','ALB','PLUG','FSLR','CROX','DNMR','URA','SMH','LIT','ICLN','KRBN','SPY','QQQ',
'VOO','IVV','REMX','ABNB']




# %%

# telg = Telegram()
end = datetime.datetime.now()
start = end - datetime.timedelta(days=0)
post = PostgresDataClass('192.168.0.3', 'stock', 'postgres', 'tjdwns00!')




start_input = start.strftime('%Y%m%d')
end_input = end.strftime('%Y%m%d')

america_data_df = pd.DataFrame(columns=['High','Low','Open','Close','Volume','Adj Close'])
for ticker in ticker_list :
    print(ticker)
    america_data_df = america_data_df.append(web.DataReader(ticker, "yahoo", start_input, end_input))


    
    
    
    tuples = [tuple(x) for x in df.values.tolist()]

    post.insert_list(tuples, 'krx.daily_market')
      










#%%
        dfi.export(high_name_df,
                'C:\\Users\\sungjoon\\GIT\\stock\\daily_script\\{high_name}_image\\{date}.png'.format(date=current_day,high_name=high_name,high_value = high_value),
                max_cols=-1, max_rows=-1)

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
