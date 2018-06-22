#!/usr/bin/env python
# coding:utf-8

"""
function: 
@author: zkang kai
@contact: 474918208@qq.com
"""

import wx


def update(event):
    '''
    更新数据
    '''
    temp_string = ui_begin_date.GetValue()
    contents.SetValue(temp_string)


def write_to_excel(event):
    '''
    写入excel中
    '''

    pass

app = wx.App()

win = wx.Frame(None,title="simple editor",size=(410,335))

begin_button = wx.Button(win,label='更新数据',pos=(225,10),size=(80,45))
begin_button.Bind(wx.EVT_BUTTON,update)
save_button = wx.Button(win,label='写入excle',pos=(315,10),size=(80,45))
save_button.Bind(wx.EVT_BUTTON,write_to_excel)

ui_label1 = wx.StaticText(win, label = "起始日期", pos = (5,5)) 
ui_label2 = wx.StaticText(win, label = "终止日期", pos = (5,35)) 

ui_begin_date = wx.TextCtrl(win,pos=(60,5),size=(150,25))
ui_end_date = wx.TextCtrl(win,pos=(60,35),size=(150,25))

contents = wx.TextCtrl(win,pos=(5,70),size=(390,260),style=wx.TE_MULTILINE |
                       wx.HSCROLL)

win.Show()
app.MainLoop()
