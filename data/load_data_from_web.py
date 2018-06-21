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
import tushare as ts
import openpyxl as oxl
import os
from collections import OrderedDict
import datetime
import json


def load_from_local():
    
    with open('__ HKEX __ HKEXnews __.html','r',encoding="utf-8") as f:
        return f.read()

def get_first_part():

    temp_html = soup.find("table",{"id":"Table5"})
    temp_html = temp_html.find_all('td',{"class":"arial12black"})

    first_dict = {}
    temp_string = temp_html[1].get_text().strip()
    temp_string = datetime.datetime.strptime(temp_string,"%d/%m/%Y")
    temp_string = temp_string.strftime("%Y-%m-%d")
    first_dict['last_date'] = temp_string
    first_dict['stock_code'] = temp_html[3].get_text().strip()
    first_dict['stock_name'] = temp_html[5].get_text().strip()

    return first_dict

def get_second_part():

    temp_html = soup.find("div",{"id":{"pnlResultSummary"}})
    temp_html = temp_html.find_all("span",{"class":"mobilezoom"})

    second_dict = {}
    second_dict['hold_volumn'] = temp_html[0].get_text().strip()
    second_dict['people_number'] = temp_html[1].get_text().strip()
    second_dict['hold_precent'] = temp_html[2].get_text().strip()
    second_dict['all_volumn'] = temp_html[6].get_text().strip()

    return second_dict

def get_third_part(first_dict):

    temp_html = soup.find("table",{"id":{"participantShareholdingList"}})
    temp_html = temp_html.find_all('tr')

    row_number = len(temp_html)
    col_number = len(temp_html[0].find_all('td'))

    d = {}
    for i in range(col_number):
        d[i] = []

    for i in range(1,row_number):
        temp_tr = temp_html[i]
        temp_td = temp_tr.find_all('td')
    
        if len(temp_td) !=col_number:
            continue
        
        for j in range(col_number):
            temp_string = temp_td[j].get_text().strip()
            d[j].append(temp_string)

    last_pd = pd.DataFrame(d)
    
    last_dict = {}
    for i in range(len(last_pd)):
        last_dict[last_pd.iat[i,0]] = last_pd.iat[i,1]

    name_dict.update(last_dict)

    new_pd = pd.DataFrame(last_pd[3])
    new_pd = new_pd.T
    new_pd.columns = last_pd[0]

    last_date = first_dict['last_date']
    time_span = pd.Timestamp(last_date)
    new_pd.index = [time_span]

    temp_string = datetime.datetime.strptime(last_date,'%Y-%m-%d')
    end_date = temp_string.date()
    start_date = end_date - datetime.timedelta(10)

    temp_df = ts.get_k_data('601888',start=start_date.isoformat(),end=end_date.isoformat())

    if temp_df.empty:
        #  close_data[last_date] = list(close_data.values())[-1]
        close_data[str(time_span)] = 0 
    else:
        close_data[str(time_span)] = temp_df.iat[-1,2]

    return new_pd

def save_to_excel(first_dict,second_dict,merge_pd):

    wb = oxl.Workbook()
    ws = wb.create_sheet(index=0,title='oxl-sheet')
    
    ws.cell(row=1,column=1).value = '持股日期'
    ws.cell(row=1,column=2).value = first_dict['last_date']
    ws.cell(row=1,column=3).value = '股票代码'
    ws.cell(row=1,column=4).value = first_dict['stock_code']
    ws.cell(row=1,column=5).value = '股票名称'
    ws.cell(row=1,column=6).value = first_dict['stock_name']

    ws.cell(row=3,column=1).value = '中央结算系统持股量'
    ws.cell(row=4,column=1).value = second_dict['hold_volumn']
    ws.cell(row=3,column=2).value = '参与者数目'
    ws.cell(row=4,column=2).value = second_dict['people_number']
    ws.cell(row=3,column=3).value = '总数百分比'
    ws.cell(row=4,column=3).value = second_dict['hold_precent']
    ws.cell(row=3,column=4).value = '全部持股量'
    ws.cell(row=4,column=4).value = second_dict['all_volumn']

    columns = merge_pd.columns
    index = merge_pd.index
    
    row_number = len(index)
    col_number = len(columns)

    ws.cell(row=8,column=1).value = '日期'
    ws.cell(row=8,column=2).value = '收盘价'

    for i in range(row_number):
        ws.cell(row=i+9,column=1).value = str(index[i])[0:10]
        ws.cell(row=i+9,column=2).value = close_data.get(str(index[i]),0)

    for i in range(col_number):
        ws.cell(row=8,column=i+3).value = columns[i]
        ws.cell(row=7,column=i+3).value = name_dict[columns[i]] 

    for i in range(row_number):
        for j in range(col_number):
            ws.cell(row=9+i,column=j+3).value = merge_pd.iat[i,j]

    wb.save('test.xlsx')
    print("数据已写入excel中!")

def plot_10(merge_pd):
    '''
    画前10大持仓股的曲线图
    '''
    temp_pd = merge_pd.sort_values(merge_pd.index[0],axis=1,ascendind=False)
    
    number = min(10,len(merge_pd))
    
    for i=0:range(number):
        temp_pd.
        pass
def save_to_config():

    first_dict = get_first_part()
    last_date = first_dict['last_date']

    if str(pd.Timestamp(last_date)) in close_data:
        print("该日期数据已经存在!")
        save_to_excel(config_dict['first_dict'],config_dict['second_dict'],pd.read_json(config_dict['old_pd'])) 
        return

    second_dict = get_second_part()
    third_pd = get_third_part(first_dict)
    merge_pd = third_pd.append(old_pd)
    merge_pd = merge_pd.sort_index(ascending=False)

    config_dict['name_dict'] = name_dict
    config_dict['close_data'] = close_data
    config_dict[last_date] = [first_dict,second_dict,third_pd.to_json()]
    config_dict['old_pd'] = merge_pd.to_json()
    config_dict['first_dict'] = first_dict
    config_dict['second_dict'] = second_dict
    config_dict['third_pd'] = third_pd.to_json()

    save_to_excel(first_dict,second_dict,merge_pd)
    
    with open('config.json','w',encoding='utf-8') as f:
        json.dump(config_dict,f)

    print('数据更新至%s!' % merge_pd.index[0])

if __name__ == '__main__':

    if os.path.exists('config.json'):
        with open('config.json','r',encoding='utf-8') as f:
            config_dict = json.load(f)
            name_dict = config_dict.get('name_dict',{})
            close_data = config_dict.get('close_data',{})
            old_pd = config_dict['old_pd']
            old_pd = pd.read_json(old_pd)
    else:
        config_dict = {}
        name_dict = {}
        close_data = {}
        old_pd = pd.DataFrame()

    html_txt = load_from_local()
    soup = BeautifulSoup(html_txt,'html.parser')

    save_to_config()

