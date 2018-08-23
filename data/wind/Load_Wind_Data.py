# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:43:27 2017

@author: zhangkai

history:
2017-11-28 修改源代码
"""

import time
from datetime import date, datetime

import pymysql
from WindPy import w
from pymongo import MongoClient


# %%
def GetIpoDate(stk_code):
    sql = "select ipodate from All_Stock_Info where windcode='%s' limit 1" % (stk_code)
    cursor.execute(sql)
    row_1 = cursor.fetchone()
    connect.commit()
    return row_1[0]


def GetLastTradeDate():
    end_date = date.today()
    count = w.tdayscount(end_date)
    if count.Data == 0 or datetime.now().hour <= 15:
        return w.tdaysoffset(-1, end_date).Data[0][0].date()

    return end_date


def UpdateOneStockDataFromWind(stk_code, field_list):
    # 下载数据
    sql_stk_code = ''.join(['`', stk_code, '`'])

    sql = "show tables like '%s'" % stk_code
    effect = cursor.execute(sql)
    if effect == 0:
        sql = "CREATE TABLE %s like template" % sql_stk_code
        cursor.execute(sql)
        connect.commit()
        start_data = GetIpoDate(stk_code)
    else:
        sql = "select date from %s order by date desc limit 1" % (sql_stk_code)
        effect = cursor.execute(sql)
        row_1 = cursor.fetchall()
        connect.commit()
        if effect == 0:
            start_data = GetIpoDate(stk_code)
        else:
            start_data = row_1[0][0]

    if start_data >= last_date:
        print(stk_code + "已经是最新数据!")
        return

    wind_data = w.wsd(stk_code, field_list, start_data, last_date, "showblank=-1;Fill=Previous;PriceAdj=F")

    if wind_data.ErrorCode != 0:
        print(stk_code + '更新数据失败!')
        return

    # 更新mongodb数据库
    collection = db[stk_code]
    # 更新mysql数据库
    sql = []
    many_mongo = []
    temp_data = wind_data.Data
    temp_time = wind_data.Times
    num = len(temp_time)
    if num == 1:
        sql = "INSERT INTO %s VALUES ('%s',%f,%f,%f,%f,%f,%f,%f)" % (
            sql_stk_code, temp_time[0].isoformat(), temp_data[0], temp_data[1], temp_data[2], temp_data[3],
            temp_data[4], temp_data[5], temp_data[6])
        many_mongo = {
            'date': temp_time[0].isoformat(),
            'open': temp_data[0],
            'high': temp_data[1],
            'low': temp_data[2],
            'close': temp_data[3],
            'volume': temp_data[4],
            'amt': temp_data[5],
            'vwap': temp_data[6]
        }
        collection.insert_one(many_mongo)
        effect = cursor.execute(sql)
        connect.commit()
    else:
        for i in range(0, num):
            temp_time_s1 = temp_time[i].isoformat()
            sql.append(str((temp_time_s1, temp_data[0][i], temp_data[1][i], temp_data[2][i], temp_data[3][i],
                            temp_data[4][i], temp_data[5][i], temp_data[6][i])))
            many_mongo.append({
                'date': temp_time_s1,
                'open': temp_data[0][i],
                'high': temp_data[1][i],
                'low': temp_data[2][i],
                'close': temp_data[3][i],
                'volume': temp_data[4][i],
                'amt': temp_data[5][i],
                'vwap': temp_data[6][i]
            })
        collection.insert_many(many_mongo)
        sql = ("INSERT INTO %s VALUES " + ','.join(sql)) % sql_stk_code
        effect = cursor.execute(sql)
        connect.commit()
    print(stk_code + "更新数据成功!")


def GetLastDateInMysql():
    sql = "select date from UpdateTime order by date desc limit 1"
    effect = cursor.execute(sql)
    row_1 = cursor.fetchone()
    connect.commit()
    if effect == 0:
        return datetime.today()
    else:
        return row_1[0]


def UpdateAllStockDataFromWind():
    stk_code_list_old = GetAllStockInfoFromMySql("windcode")
    stk_code_list_old = MysqlToList(stk_code_list_old)
    wind_dates = []
    if stk_code_list_old:
        start_date = GetLastDateInMysql()
        start_date = w.tdaysoffset(1, start_date)
        start_date = start_date.Times[0]
        if start_date <= last_date:
            open_data = w.wsd(stk_code_list_old, "open", start_date, last_date, "showblank=-1;Fill=Previous;PriceAdj=F")
            if open_data.ErrorCode != 0:
                print("open_data load error!")
                return

            high_data = w.wsd(stk_code_list_old, "high", start_date, last_date, "showblank=-1;Fill=Previous;PriceAdj=F")
            if high_data.ErrorCode != 0:
                print("high_data load error!")
                return

            low_data = w.wsd(stk_code_list_old, "low", start_date, last_date, "showblank=-1;Fill=Previous;PriceAdj=F")
            if low_data.ErrorCode != 0:
                print("low_data load error!")
                return

            close_data = w.wsd(stk_code_list_old, "close", start_date, last_date,
                               "showblank=-1;Fill=Previous;PriceAdj=F")
            if close_data.ErrorCode != 0:
                print("close_data load error!")
                return

            volume_data = w.wsd(stk_code_list_old, "volume", start_date, last_date,
                                "showblank=-1;Fill=Previous;PriceAdj=F")
            if volume_data.ErrorCode != 0:
                print("volume_data load error!")
                return

            amt_data = w.wsd(stk_code_list_old, "amt", start_date, last_date, "showblank=-1;Fill=Previous;PriceAdj=F")
            if amt_data.ErrorCode != 0:
                print("amt_data load error!")
                return

            vwap_data = w.wsd(stk_code_list_old, "vwap", start_date, last_date, "showblank=-1;Fill=Previous;PriceAdj=F")
            if vwap_data.ErrorCode != 0:
                print("vwap_data load error!")
                return

            wind_dates = w.tdays(start_date, last_date)

            wind_dates = wind_dates.Times
            open_data = open_data.Data
            high_data = high_data.Data
            low_data = low_data.Data
            close_data = close_data.Data
            volume_data = volume_data.Data
            amt_data = amt_data.Data
            vwap_data = vwap_data.Data

    num_date = len(wind_dates)

    if num_date <= 0:
        print("原始数据已经是最新数据!")
    elif num_date == 1:
        for i in range(0, len(stk_code_list_old)):
            sql_stk_code = ''.join(['`', stk_code_list_old[i], '`'])
            sql = "INSERT INTO %s VALUES ('%s',%f,%f,%f,%f,%f,%f,%f)" % (
                sql_stk_code, wind_dates.isoformat(), open_data[0], high_data[0], low_data[0], close_data[0],
                volume_data[0], amt_data[0], vwap_data[0])
            cursor.execute(sql)
            connect.commit()
            collection = db[stk_code_list_old[i]]
            collection.insert_one({'date': wind_dates.isoformat(),
                                   'open': open_data[0],
                                   'high': high_data[0],
                                   'low': low_data[0],
                                   'close': close_data[0],
                                   'volume': volume_data[0],
                                   'amt': amt_data[0],
                                   'vwap': vwap_data[0]})

    else:
        for i in range(0, len(stk_code_list_old)):
            sql_stk_code = ''.join(['`', stk_code_list_old[i], '`'])
            sql = []
            many_mongo = []
            for j in range(0, num_date):
                temp_time = wind_dates[j].isoformat()
                sql.append(str((temp_time, open_data[i][j], high_data[i][j], low_data[i][j], close_data[i][j],
                                volume_data[i][j], amt_data[i][j], vwap_data[i][j])))
                many_mongo.append({
                    'date': temp_time,
                    'open': open_data[i][j],
                    'high': high_data[i][j],
                    'low': low_data[i][j],
                    'close': close_data[i][j],
                    'volume': volume_data[i][j],
                    'amt': amt_data[i][j],
                    'vwap': vwap_data[i][j]
                })

            # 更新数据库
            try:
                collection = db[stk_code_list_old[i]]
                collection.insert_many(many_mongo)
                sql = ("INSERT INTO %s VALUES " + ','.join(sql)) % sql_stk_code
                cursor.execute(sql)
                connect.commit()
            except Exception as err:
                print(err)

    print("更新原始数据成功!")
    UpdateStockCodeFormWind()

    stk_code_list_new = GetAllStockInfoFromMySql("windcode")
    stk_code_list_new = MysqlToList(stk_code_list_new)
    new_stock_list = list(
        set(stk_code_list_new).difference(set(stk_code_list_old)))  # stk_code_list_new中有而stk_code_list_old中没有的
    for stk_code in new_stock_list:
        UpdateOneStockDataFromWind(stk_code, field_list)

    sql = "INSERT INTO UpdateTime VALUES ('%s')" % last_date.isoformat()
    cursor.execute(sql)
    connect.commit()
    collection = db['UpdateTime']
    collection.insert_one({'date': last_date.isoformat()})


def UpdateStockCodeFormWind():
    all_stk_code = w.wset("sectorconstituent", ''.join(["date=", last_date.isoformat(),
                                                        ";sectorid=a001010100000000;field=wind_code"]))  # 取全部A股股票代码、名称信息

    # 更新mysql中的最后更新日期数据
    if all_stk_code.ErrorCode != 0:
        print('更新wind全部代码数据失败!')
    else:  # 获取所有股票基本信息，IPO日期
        all_stk_code = all_stk_code.Data[0]
        data = w.wsd(all_stk_code, "ipo_date", last_date, last_date, "PriceAdj=F")
        if data.ErrorCode != 0:
            print("获得股票IPO数据失败!")
        else:
            sql = "truncate table All_Stock_Info"
            cursor.execute(sql)
            connect.commit()
            db.All_Stock_Info.remove()

            temp_data = data.Data[0]
            sql = []
            many_mongo = []
            for i in range(len(all_stk_code)):
                temp_data_1 = temp_data[i].isoformat()
                sql.append(str((all_stk_code[i], temp_data_1)))
                many_mongo.append({"windcode": all_stk_code[i], "ipodate": temp_data_1})

            collection = db['All_Stock_Info']
            collection.insert_many(many_mongo)
            sql = ("INSERT INTO All_Stock_Info VALUES " + ','.join(sql))
            cursor.execute(sql)
            connect.commit()
            print('更新wind全部代码数据成功!')


def GetAllStockInfoFromMySql(sql_fields):
    sql = "select " + sql_fields + " from All_Stock_Info"
    cursor.execute(sql)
    connect.commit()
    all_stk_info_data = cursor.fetchall()
    return all_stk_info_data


def CreateTableInMysql():
    # 创建mysql模板表、基本信息表
    sql = "show tables like 'template'"
    result = cursor.execute(sql)
    if result == 0:
        sql = 'CREATE TABLE template (date DATE ,open FLOAT,high FLOAT,low FLOAT,close FlOAT,volume FlOAT,amt double,vwap double,primary key(date) )'
        cursor.execute(sql)

    sql = "show tables like 'All_Stock_Info'"
    result = cursor.execute(sql)
    if result == 0:
        sql = 'CREATE TABLE All_Stock_Info (windcode VARCHAR(9),ipodate DATE,primary key(windcode) )'
        cursor.execute(sql)

    sql = "show tables like 'UpdateTime'"
    result = cursor.execute(sql)
    if result == 0:
        sql = 'CREATE TABLE UpdateTime (date DATE)'
        cursor.execute(sql)
    connect.commit()


def MysqlToList(all_stk_info_data):
    stk_code_list = []
    for stk_code in all_stk_info_data:
        stk_code_list.append(stk_code[0])

    return stk_code_list


def DeleteData(stk_code):
    sql_stk_code = ''.join(['`', stk_code, '`'])
    sql = "show tables like '%s'" % stk_code
    result = cursor.execute(sql)
    if result == 0:
        print(stk_code + '数据表不存在!')
    else:
        sql = 'truncate table ' + sql_stk_code
        cursor.execute(sql)
        connect.commit()

    db[stk_code].remove()
    print(stk_code + '删除数据成功!')

def WsqCallback():
    print("WsqCallBack")
    pass

def test():
    pass



if __name__ == '__main__':

    # %% mysql连接和配置
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='stock_data',
        charset='utf8'
    )
    cursor = connect.cursor()  # 获取游标

    CreateTableInMysql()
    # %% mongodb连接和配置
    conn = MongoClient('localhost', 27017)
    db = conn.stock_data  # 连接mydb数据库，没有则自动创建
    # %% wind连接和配置
    field_list = ['open', 'high', "low", "close", "volume", "amt", "vwap"]
    w.start()  # 启动连接
    last_date = GetLastTradeDate()
    start_time = time.clock()

    UpdateAllStockDataFromWind()

    # 关闭连接
    cursor.close()
    connect.close()

    end_time = time.clock()
    print('Running time: %s Seconds' % (end_time - start_time))
