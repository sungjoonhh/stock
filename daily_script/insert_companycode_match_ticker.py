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
#KRX 가서 전종목 기본정보 엑셀 다운받고 실행
post = PostgresDataClass('192.168.0.3', 'stock', 'postgres', 'tjdwns00!')


data = pd.read_excel('C:\\Users\\sungjoon\\Downloads\\ac.xlsx')
data1 = data[['단축코드','한글 종목약명']]
tuples = [tuple(x) for x in data1.values.tolist()]

post.insert_list(tuples, 'krx.company_ticker')

