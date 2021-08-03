# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 20:26:02 2021

@author: user
"""
import requests
import pandas as pd
from postLib import PostgresDataClass

from bs4 import BeautifulSoup
import datetime
import re
from FileReader   import FileReader
from postLib import PostgresDataClass


class HKParser :
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            "Upgrade-Insecure-Requests": "1", "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"}

        filereader = FileReader()
        self.post_dict = filereader.read_data('C:\\Users\\user\\Documents\\postgres.txt')
        self.user = self.post_dict['user']
        self.database = self.post_dict['database']
        self.password = self.post_dict['password']

    def hankyung_consensus_webcrawling(self,start,end) :



        df = pd.DataFrame()

        while start <= end:
            current_day = start.strftime('%Y-%m-%d')
            for page in range(1, 2):
                try:
                    url = "http://consensus.hankyung.com/apps.analysis/analysis.list?&sdate={current_day}&edate={current_day}&report_type=CO&order_type=&now_page={page}&pagenum=80".format(
                        current_day=current_day, page=page)
                    resp = requests.get(url, headers=self.headers)
                    soup = BeautifulSoup(resp.content, "html.parser")
                    no_today = soup.find("div", {"class": "table_style01"})
                    table = no_today.find("table")

                    board_index = 0
                    while board_index < 81:
                        board_index += 1

                        try:
                            board_date = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                board_index) + ") > td.first.txt_number")[0].get_text()
                        except:
                            board_date = '1999-01-01'
                            continue

                        try:
                            board_title = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                board_index) + ") > td.text_l > a")[0]['onmouseover'].split("'")[1]
                            board_name = soup.select(board_title + "> strong")[0].get_text()
                            a = re.split("[()]", board_name)
                            board_company = a[0]
                            board_company_code = a[1]
                            board_company_desc = a[2]
                        except:
                            board_company = ''
                            board_company_code = ''
                            board_company_desc = ''
                            continue

                        try:
                            board_price = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                board_index) + ") > td.text_r.txt_number")[0].get_text()

                        except:
                            board_price = ''

                        try:
                            board_opinion = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                board_index) + ") > td:nth-child(4)")[0].get_text()

                        except:
                            board_opinion = ''

                        try:
                            board_writer = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                board_index) + ") > td:nth-child(5)")[0].get_text()

                        except:
                            board_writer = ''

                        try:
                            board_investment = soup.select(
                                "#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                    board_index) + ") > td:nth-child(6)")[0].get_text()
                        except:
                            board_investment = ''

                        try:
                            board_category = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                board_index) + ") > td:nth-child(7) > div > a")[0]['href'].split("'")[1]
                        except:
                            board_category = ''

                        try:
                            board_reference = "http://consensus.hankyung.com" + soup.select(
                                "#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                    board_index) + ") > td:nth-child(8)> div > a")[0]['href']
                        except:
                            board_reference = ''

                        try:
                            board_pdf_url = "http://consensus.hankyung.com" + soup.select(
                                "#contents > div.table_style01 > table > tbody > tr:nth-child(" + str(
                                    board_index) + ") > td:nth-child(9) > div > a")[0]['href']
                        except:
                            board_pdf_url = ''

                        print(str(page) + "페이지의" + str(board_index) + "번째까지 게시글 확인 완료")
                        # content_594511 > strong
                        df = df.append({'date': board_date, 'company': board_company, 'company_code': board_company_code,
                                        'desc': board_company_desc, 'price': board_price, 'opinion': board_opinion,
                                        'writer': board_writer, 'investment': board_investment, 'category': board_category,
                                        'reference': board_reference, 'pdf': board_pdf_url}, ignore_index=True)
                except Exception as e:
                    print('예외가 발생하였습니다.', e)
            start += datetime.timedelta(days=1)

        df[['date', 'company', 'company_code', 'desc', 'price', 'opinion', 'writer', 'investment', 'category', 'reference','pdf']]
        df['price'] = df['price'].astype(int)
        df['date'] = df['date'].astype({'date': 'datetime64[ns]'})
        tuples = [tuple(x) for x in df.values.tolist()]
        post = PostgresDataClass(self.host, self.database, self.user, self.password)
        post.insert_list(tuples, 'stock.hk_consensus')
