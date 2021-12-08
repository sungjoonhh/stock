# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 20:26:02 2021

@author: user
"""
    
    
import sys
sys.path.append('C:\\Users\\sungjoon\\libs')
import requests
from io import BytesIO
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from bs4 import BeautifulSoup
import datetime
import re
from postLib import  PostgresDataClass

import numpy as np


#%%
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
pd.set_option('display.float_format', None)

financialStatements = [['https://www.choicestock.co.kr/search/financials/{stock}/MRT','연환산'],
['https://www.choicestock.co.kr/search/financials/{stock}/MRY','연간'],
['https://www.choicestock.co.kr/search/financials/{stock}/MRQ','분기']]

investmentIndicators = [['https://www.choicestock.co.kr/search/invest/{stock}/MRT','연환산'],
['https://www.choicestock.co.kr/search/invest/{stock}/MRY','연간'],
['https://www.choicestock.co.kr/search/invest/{stock}/MRQ','분기']]


financialIndex= [[2,'손익계산서'],
[3,'재무상태표'],
[4,'현금흐름표']]


investmentIndex =[[1,'투자지표']]

ticker = 'TSLA'

#%%
all_df = pd.DataFrame()

for fs,fsName in financialStatements:
    try :
        url = fs.format(stock=ticker)
        resp = requests.get(url, headers = headers)
        soup = BeautifulSoup(resp.content, "html.parser")


        for fi,fiName in financialIndex: 
            try :
                df = pd.DataFrame()
                board_date = soup.select("#container > div.sub_mid.tabs_area > div > div:nth-child({idx}) > div.scroll_table > table".format(idx=fi))[0]
                df = pd.read_html(str(board_date))[0]
                df['ticker'] = ticker
                df['basis'] = fsName
                df['balance_sheet'] = fiName
                all_df = all_df.append(df)
                del [[df]]


            except :
                print(1)
                continue
        

    except :
        print(2)
        continue        
#%%
print("#container > div.sub_mid.tabs_area > div > div:nth-child({idx}) > div.scroll_table > table".format(idx=fi))

#%%
for invest,investName in investmentIndicators:
    try :
        url = invest.format(stock=ticker)
        resp = requests.get(url, headers = headers)
        soup = BeautifulSoup(resp.content, "html.parser")


        for ii,iiName in investmentIndex: 
            try :
                df = pd.DataFrame()
                board_date = soup.select(" #container > div.sub_mid.tabs_area > div > div.scroll_table_wrap > div > table")[0]
                df = pd.read_html(str(board_date))[0]
                df['ticker'] = ticker
                df['basis'] = investName
                df['balance_sheet'] = iiName
                all_df = all_df.append(df)
                del [[df]]

            except :
                print(3)
                continue
        

    except :
        print(4)
        continue        

all_df['Unnamed: 0']
#%%

all_df.rename(columns = {'Unnamed: 0' : 'label'}, inplace = True)
result_df = pd.melt(all_df,
                    id_vars=['ticker','label','basis','balance_sheet'],
                    )
result_df = result_df.dropna()

result_df['variable'] = '20'+ result_df['variable']
result_df['variable'] = pd.to_datetime(result_df['variable'],format='%Y.%m/%d')

result_df = result_df[['ticker','label','basis','balance_sheet','value','variable']]
result_df = result_df.where(pd.notnull(result_df) , None)


#%%
tuples = [tuple(x) for x in result_df.values.tolist()]

tuple1 = tuples[:1]
post = PostgresDataClass('192.168.0.3','stock','postgres','tjdwns00!')
post.insert_list(tuples, 'stock.financial_statements_america')

