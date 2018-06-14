#!/usr/bin/env python
# coding:utf-8

"""
function: 
@author: zkang kai
@contact: 474918208@qq.com
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup


def load_from_local():
    
    with open('d:/__ HKEX __ HKEXnews __.html','r',encoding="utf-8") as f:
        return f.read()


def cal_pd():

    soup = BeautifulSoup(html_txt)

    temp_html = soup.find("table",{"id":"Table5"})
    temp_html = temp_html.find_all('td',{"class":"arial12black"})

    first_dict['last_date'] = temp_html[1].get_text().strip()
    first_dict['stock_code'] = temp_html[3].get_text().strip()
    first_dict['stock_name'] = temp_html[5].get_text().strip()

    temp_html = soup.find("div",{"id":{"pnlResultSummary"}})
    temp_html = temp_html.find_all("span",{"class":"mobilezoom"})

    second_dict['hold_volumn'] = temp_html[0].get_text().strip()
    second_dict['people_number'] = temp_html[1].get_text().strip()
    second_dict['hold_precent'] = temp_html[2].get_text().strip()
    second_dict['all_volumn'] = temp_html[6].get_text().strip()

    temp_html = soup.find("table",{"id":{"participantShareholdingList"}})
    temp_all_tr = temp_html.find_all('tr')

    row_number = len(temp_all_tr)

    col_number = len(temp_all_tr[0].find_all('td'))

    for i in range(len(row_number)):
        d[i] = []

    for i in range(1,row_number):
        temp_tr = temp6[i]
        temp_td = temp_tr.find_all('td')
    
        if len(temp_td) !=col_number:
            continue
        
        for j in range(col_number):
            temp_string = temp_td[j].get_text().strip()
            d[j].append(temp_string)

    last_pd = pd.DataFrame(d)
    
    last_dict = {}
    for i in range(len(temp_pd)):
        last_dict[last_pd.iat[i,0]] = last_pd.iat[i,1]

    new_pd = pd.DataFrame(last_pd[3])
    new_pd = new_pd.T
    new_pd.columns = last_pd[0]

    merge_pd = pd.concat([old_pd,new_pd])
    name_dict.update(last_dict)


    


if __name__ == '__main__':

    store = pd.HDFStore('data.h5')

    name_dict = store['name_dict']
    old_pd = store['old_pd']

