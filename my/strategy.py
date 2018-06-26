#!/usr/bin/env python
# coding:utf-8

"""
function:
    策略实例：策略应该和账号绑定

    属性：
    order：下过的订单

    接口：
    下单函数
@author: zkang kai
@contact: 474918208@qq.com
"""


class Strategy(object):
    """
    策略用来实现交易逻辑
    """

    def __init__(self):
        super(Strategy, self).__init__()

    def init_need_data():
        # TODO 规定需要的数据
        pass

    def init_account():
        pass

    def stock_trader():
        pass

    def credit_trader():
        pass

    def commodity_futures_trader():
        pass

    def financial_futures_trader():
        pass

    def options_trader():
        pass

    def on_data():
        pass

    def order_update():
        pass

