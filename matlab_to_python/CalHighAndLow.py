#!/usr/bin/env python
# coding:utf-8

"""
function:
@author: zkang kai
@contact: 474918208@qq.com
"""

import numpy as np
import pandas as pd
import tushare as ts


def CalHighAnaLow(stk_data):
    '''
    根据传入的dataframe计算股票的高低点
    '''


    '''计算内移日'''
    temp_data = stk_data

    while(1):
        index = ( temp_data.high <= temp_data.high.shift(1)) & ( temp_data.low >= temp_data.low.shift(1) )

        stk_data['neiyiri'] = index 
        stk_data = stk_data.fillna(True)
        if index.any() == False:
            break;
        
        temp_data = stk_data[ stk_data['neiyiri'] == False ]


    '''计算外移日'''
    temp_data = stk_data
    index = (temp_data.high <= temp_data.high.shift(-1)) & (temp_data.low >= temp_data.low.shift(-1))
    stk_data['waiyiri'] = index 

    '''计算短期高低点'''
    temp_data = stk_data[ stk_data['neiyiri'] == False ]
    index = (temp_data.high >= temp_data.high.shift(1) ) & (temp_data.high >= temp_data.high.shift(-1) )
    index1 = (temp_data.low <= temp_data.low.shift(1) ) & (temp_data.low <= temp_data.low.shift(-1) )
    stk_data['first_high'] = index
    stk_data['first_low'] = index1

    '''计算中期高低点'''
    temp_data = stk_data[ stk_data['first_high'] == True ]
    index = (temp_data.high >= temp_data.high.shift(1) ) & (temp_data.high >= temp_data.high.shift(-1) )
    temp_data = stk_data[ stk_data['first_low'] == True ]
    index1 = (temp_data.low <= temp_data.low.shift(1) ) & (temp_data.low <= temp_data.low.shift(-1) )
    stk_data['second_high'] = index
    stk_data['second_low'] = index1

    '''计算长期高低点'''
    temp_data = stk_data[ stk_data['second_high'] == True ]
    index = (temp_data.high >= temp_data.high.shift(1) ) & (temp_data.high >= temp_data.high.shift(-1) )
    temp_data = stk_data[ stk_data['second_low'] == True ]
    index1 = (temp_data.low <= temp_data.low.shift(1) ) & (temp_data.low <= temp_data.low.shift(-1) )
    stk_data['third_high'] = index
    stk_data['third_low'] = index1

    return stk_data

def ShowInfo(stk_data,cycle):
    '''
    输出不同周期高低点的情况
    '''

    number = len(stK_data)

    for i in range(number):
        
        if stk_data['first_high'].iat[i] == True:
            print("%s 形成短期高点,最高点为 %d")
