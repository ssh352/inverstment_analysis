#!/usr/bin/env python
# coding:utf-8

"""
function:
    从tushare下载日线数据,存储格式为hdf5
@author: zkang kai
@contact: 474918208@qq.com

history:
    脚本创建
"""
import tushare as ts
import pandas as pd
import jaqs.util as jutil
import os
import warnings
import progressbar


warnings.filterwarnings('ignore')


def load_data():
    "
    从tushare中下载数据, 首先下载所有数据的基础信息, 得到股票的上市时间
    判断h5文件中是否存在某个数据, 更新初始时间
        "
    stock_basics = ts.get_stock_basics()
    stock_basics = stock_basics[stock_basics['timeToMarket'] > 19000000]
    stock_basics.to_hdf(
        os.path.join(
            dir_name,
            basics_name),
        'stock_basics',
        append=True)

    code_index = stock_basics.index
    ipodate = stock_basics['timeToMarket']

    day_store = pd.HDFStore(os.path.join(dir_name, stock_name))
    time_delta = datetime.timedelta(1)

    for i in progressba.progressbar(range(len(stock_basics))):
        temp_code = code_index[i]

        if temp_code in already_load:
            temp_time = already_load[temp_code]
            temp_time = datetime.datetime.strptime(
                time_time, '%Y-%m-%d') + time_delta
            temp_time = temp_time.date()
        else:
            temp_time = ipodate.iat[i]
            temp_time = str(temp_time)
            temp_time = temp_time[0:4] + '-' + \
                temp_time[4:6] + '-' + temp_time[6:]

        temp_df = ts.get_k_data(
            code=temp_code,
            start=temp_time,
            end='',
            autype='qfq',
            ktype='D')
        already_load[temp_code] = temp_df.tail(1).iat[0, 0]
        day_store[temp_code] = temp_df

    config_dict['already_load'] = already_load
    jutil.save_json(config_dict)
    day_store.close()


if __name__ == '__main__':
    config_path = r"../config/tushare_config.json"
    config_dict = jutil.read_json(config_path)

    dir_name = config_dict.get('dirname', '~')
    basics_name = config_dict.get('basics_hdf', 'basics.h5')
    stock_name = config_dict.get('day_stock_hdf', 'day_stock.h5')
    already_load = config_dict.get('already_load', {})

    load_data()
