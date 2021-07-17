# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:06:23 2021

@author: SUNGJOON
"""

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time





def get_code(company_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + company_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj




def get_price(company_code):
    bs_obj = get_code(company_code)
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"})
    now_price = blind.text
    return now_price


company_code = "008770"


now = datetime.now()


now_price = get_price(item)
print(now_price)
