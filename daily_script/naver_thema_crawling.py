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





# from html_table_parser import parser_functions as parser

#%%

end = datetime.datetime.now()
start = end - datetime.timedelta(days=10)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
pd.set_option('display.float_format', None)
df = pd.DataFrame()

#%%
for pagenum in range(1,8):
    url = "https://finance.naver.com/sise/theme.nhn?field=name&ordering=asc&page={pagenum}".format(pagenum=pagenum)
    resp = requests.get(url, headers = headers)
    soup = BeautifulSoup(resp.content, "html.parser")


    thema_num = 0
    while thema_num < 50:
        try : 
            thema_num += 1
            board_date = soup.select("#contentarea_left > table.type_1.theme > tr:nth-child("+str(thema_num)+") > td.col_type1 > a")[0]

    
            linkUrl = 'https://finance.naver.com' + board_date['href']

            linkResp = requests.get(linkUrl, headers = headers)
            linkSoup = BeautifulSoup(linkResp.content, "html.parser")
            thema = board_date.text
        except Exception as e:
            continue
        link_num = 0
        while link_num < 100 :
            try : 
                link_num += 1
    
                link_board_date = linkSoup.select("#contentarea > div:nth-child(5) > table > tbody > tr:nth-child("+str(link_num)+") > td.name > div > a")[0].text
                print(thema, link_board_date)
                df = df.append({'thema' : thema, 'stock' : link_board_date}, ignore_index =True)                

                
            except : 
                continue

            
            
df1 = df.groupby(['stock'])['thema'].apply(lambda x: ','.join(x)).reset_index()


df.to_excel('C:\\Users\\user\\thema.xlsx')
df1.to_excel('C:\\Users\\user\\thema2.xlsx')

tuples = [tuple(x) for x in df.values.tolist()]

post = PostgresDataClass('192.168.0.3','stock','postgres','tjdwns00!')
post.insert_list(tuples, 'stock.thema_stock')
