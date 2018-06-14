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
import datetime


warnings.filterwarnings('ignore')


def load_data():
    """
    从tushare中下载数据, 首先下载所有数据的基础信息, 得到股票的上市时间
    判断h5文件中是否存在某个数据, 更新初始时间
    """

    temp_df = ts.get_k_data('000001', '', '', index=True)
    tushare_last_date = temp_df.iat[-1, 0]

    if datetime.datetime.strptime(last_date, '%Y-%m-%d') == datetime.datetime.strptime(tushare_last_date, '%Y-%m-%d'):
        print "data is the latest!"
        return

    jutil.create_dir(os.path.join(dir_name, basics_name))
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

    for i in progressbar.progressbar(range(len(stock_basics))):
        temp_code = code_index[i]

        if temp_code in already_load:
            temp_time = already_load[temp_code]
            temp_time = datetime.datetime.strptime(
                temp_time, '%Y-%m-%d') + time_delta
            temp_time = temp_time.date().isoformat()
        else:
            temp_time = ipodate.iat[i]
            temp_time = str(temp_time)
            temp_time = datetime.datetime.strptime(temp_time,"%Y%m%d").date().isoformat()

        temp_df = ts.get_k_data(
            code=temp_code,
            start=temp_time,
            end='',
            autype='qfq',
            ktype='D')
        
        if temp_df.empty:
            continue

        already_load[temp_code] = temp_df.iat[-1, 0]
        day_store[temp_code] = pd.concat([day_store[temp_code],temp_df])

    config_dict['already_load'] = already_load
    config_dict['last_date'] = tushare_last_date
    jutil.save_json(config_dict, config_path)
    day_store.close()
    print "last date to %s!" % tushare_last_date


if __name__ == '__main__':
    config_path = r"../config/tushare_config.json"
    config_dict = jutil.read_json(config_path)

    dir_name = config_dict.get('dirname', '~')
    basics_name = config_dict.get('basics_hdf', 'basics.h5')
    stock_name = config_dict.get('day_stock_hdf', 'day_stock.h5')
    already_load = config_dict.get('already_load', {})
    last_date = config_dict.get('last_date', '1900-01-01')

    load_data()
