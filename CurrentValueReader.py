# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:06:23 2021

@author: SUNGJOON
"""

from bs4 import BeautifulSoup
import requests


class CurrentValueReader :

    def get_code(self, company_code):
        url = "https://finance.naver.com/item/main.nhn?code=" + company_code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        return bs_obj


    def get_price(self, company_code):
        bs_obj = self.get_code(company_code)
        no_today = bs_obj.find("p", {"class": "no_today"})
        blind = no_today.find("span", {"class": "blind"})
        now_price = blind.text
        return now_price

    def get_stock_code(self, company_code, stock_index):
        url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=" + company_code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        blind = bs_obj.find("section", {"class": "sc_new cs_stock cs_stock_same _cs_stock"})
        no_today = blind.find("em", {"class": "t_nm"})
        if stock_index =='코스피':
            now_price = no_today.text + ".KS"
        elif stock_index =='코스닥':
            now_price = no_today.text + ".KQ"
        return now_price


    def get_supply(self,company_code):
        company_code = company_code.split('.')[0]
        url = "https://finance.naver.com/item/frgn.nhn?code={company_code}&page=1".format(company_code = company_code)
        headers = {'User-Agent': 'Mozilla/5.0'}
        result = requests.get(url, headers=headers)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        bs_obj = bs_obj.find("div", {"section inner_sub"})
        blind = bs_obj.find("table", {'summary': "외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다."})


        return str(blind)