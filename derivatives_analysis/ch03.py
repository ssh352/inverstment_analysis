

# coding: utf-8

# In[9]:


import tushare as ts
import numpy as np
import pandas as pd
import scipy.stats as st


# 基差 = 被对冲资产的即期价格 - 用于对冲的期货合约价格
# 
# $s_1$: 在$t_1$时刻的即期价格
# 
# $s_2$: 在$t_2$时刻的即期价格
# 
# $F_1$: 在$t_1$时刻的期货价格
# 
# $F_2$: 在$t_2$时刻的期货价格
# 
# $b_1$: 在$t_1$时刻的基差
# 
# $b_2$: 在$t_2$时刻的基差

# 基差定义:现货价格-期货价格

# ### 计算如果进行对冲的最终成交价格

# In[1]:


def cal_hedge_price(s2,f1,f2):
    '''
    计算最终成交的现货价格:
        s2:t2时刻即期价格
        f1:t1时刻期货价格
        f2:t2时刻期货价格
    '''
    b2 = s2 - f2
    return f1 + b2


# In[4]:


def cal_cross_hedge_price(s2,f1,f2,s3):
    '''
    计算交叉对冲最后成交的现货价格:
        s2:需要对冲资产的现货价格
        s3:与期货合约想对应的现货价格,s3的数值在表达式中无所谓
        s3-f2:代表基差
        s2-s3:代表资产不同带来的风险
    '''
    b2 = s2 - f2
    return f1 + s3 - f2 + s2 - s3


# In[3]:


#  hedge_price(0,0.92,0.98,0.925)


# ### 交叉对冲
# 在对冲期间内,即期价格$\delta{s}$相对期货价格$\delta{F}$的最优拟合
# $$ h^* = \rho * \sigma_{s}/\sigma_{F} $$

# In[87]:


def cal_h(s,f):
    '''
    计算现货价格和期货价格变动的相关性,用来确定对冲需要的头寸数量,一份s的资产需要h份的f
    s:代表现货价格的变动
    f:代表期货价格的变动
    '''
    diff_s = s - s.shift(1)
    diff_f = f - f.shift(1)

    return s.corr(f) * s.std() / f.std()


# In[7]:


def cal_N(s,f,qa,qf):
    '''
    计算对冲s需要的期货头寸数量
    qa:代表被对冲的数量
    qf:1份股指期货合约的规模

    用法:我需要200kg黄金,则qa=200,qf=5
    '''
    return cal_h(s,f) * qa / qf


# In[10]:


#  hs300 = ts.get_k_data(code = '000300',start='2018-01-01',end='',index=True)


# In[16]:


#  s600519 = ts.get_k_data(code = '600519',start='2018-01-01',end='')


# In[43]:


#  d_600519 = s600519['close'] - s600519['close'].shift(1)
#  d_000300 = hs300['close'] - hs300['close'].shift(1)


# In[55]:


#  cal_N(d_600519,d_000300,100,300)


# In[41]:


#  reg = np.polyfit(np.array(d_000300),np.array(d_600519),deg=1)


# In[42]:


#  reg


# In[54]:


#  st.linregress(d_000300.dropna(),d_600519.dropna())


# ### 尾随对冲:根据当天期货和现货的价格变动百分比,当天期货和现货的收盘价,计算下一天的需要的期货头寸

# In[75]:


def cal_N_everyday(s,f,qa,qf):
    '''
    尾随对冲:根据当天期货和现货的价格变动百分比,当天期货和现货的收盘价,计算下一天的需要的期货头寸
    如果用远期来对冲,则只要建仓一次即可.如果使用期货来对冲,则需要实时观察期货和现货之间的价格变动

    s:一般使用现货价格当天的tick线或者1分钟线,f同理
    '''
    return cal_h(s,f) * s.iloc[-1] * qa / (f.iloc[-1] * qf)


# In[60]:


#  s600519 = ts.get_k_data(code='600519',start='2018-05-07',end='2018-05-07',ktype='5')
#  s002736 = ts.get_k_data(code='002736',start='2018-05-07',end='2018-05-07',ktype='5')


# ### 股票组合的对冲

# In[77]:


def cal_N_stock_portfolio(s,f,va,vf):
    '''
    计算对冲股票组合需要的股指期货数量
    h:组合和股指期货的贝塔值
    va:组合的价值
    vf:一份期货合约的价值
    s:组合的价格序列
    f:股指期货的价格序列
    '''
    return cal_h(s,f) * va / vf
    #  return h * va / vf


# In[79]:


#  cal_N_stock_portfolio(1.5,5050000,252500)


# In[89]:


def cal_N_for_beta(h0,h1,va,vf):
    '''
    调整组合的贝塔值
    h0为期初的贝塔值
    h1为需要的贝塔值
    '''
    
    local_N = abs(h0-h1) * va / vf
    
    if h0 > h1:
        print "需要卖出股指期货合约降低贝塔,数量为%s" % local_N
        return -local_N
    elif h0 < h1:
        print "需要买入股指期货合约增加贝塔,数量为%s" % local_N
        return local_N
    else:
        print "输入贝塔值一致,无需调整"
        return 0
    


# In[90]:


#  cal_N_for_beita(1.5,2.5,505000.,252500.)


if __name__ = '__main__':
    pass
