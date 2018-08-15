
''' 
    专业投机原理-形态统计
 {1-开盘价,2-最高价，3-最低价，4-收盘价，5-成交量，6-成交额，7-振幅，8-涨跌幅，9-换手率，10-市盈率，11-市净率，12-市值,13}
 1-短期趋势统计 2-中期趋势统计 3-长期趋势统计 4-宽幅振荡日统计 5-市盈率比较 6-市净率比较 7-均线分析 8-月交易日 9-周交易日
 形态1：最高价高于前一日的最高价，而最低价则低于前一日的最低价，并且收盘价也低于前一日的最低价--作者认为应该买入（观察认为是一个反转指标，特别是长期高低点）
 形态2：当日收盘价高于前一交易日的最高价，而且前两个交易日都是收盘价走高,它能引诱公众进场买入--作者认为应该卖出
 形态3：收盘价低于前一交易日的最低价。另外，这一天的收盘价还可以低于前3~8个交易日的最低价--作者认为应该买入
 形态4：收盘价高于前一日的最高价，收盘价接近最高价。--作者认为应该卖出
 形态5：当日收盘上涨,收盘价位于上涨价格区间下方的25#以内，收盘价还应低于开盘价。-- 作者认为应该买入
 形态1，形态2在震荡表现比较好，形态5在趋势表现比较好
 四天准则：在中期走势中，当市场在高点或低点以连续四天下跌或上涨的走势而呈现反转时，趋势很可能发生变化。
 宽幅震荡：比较大的振幅日 300291 fclose('alla'); clc;clear;exit
'''
# WriteSpecialDate(file_name,special_time,special_type) special_type:趋势（0-低点 1-高点）2-宽幅震荡日 3-形态1 4-形态2 5-形态3 6-形态4 7-形态5
a=max( original_data(end-100:end,2) ); b = min( original_data(end-100:end,3) );disp([a,b,2*(a-b)/(a+b)] )
str_path = 'C:\Users\Administratori\Documents\MATLAB\Data\Stock\result_';
stock_code = '300178'; DispFundamentalInfo(stock_code); CalHighAndLow(stock_code,'Stock');file_name = [str_path,stock_code,'.mat'];load(file_name); disp(all_static_data{7});
str1=['D:\SpecialDate\\',stock_code(1:6)]; WriteSpecialDate([str1,'middle.txt'],middle_cell_data);WriteSpecialDate([str1,'long.txt'],long_cell_data);#disp(all_static_data{3})
# 就历史资料来看，目前的中期趋势如何？道氏理论对目前的行情有何看法？是否存在背离的现象？成交量是否有明显的变化？行情宽度是否配合趋势的发展？
# 长期趋势如何？他是处于上升趋势、下降趋势、窄幅盘整还是正在变化中？就历史资料来看，目前长期趋势的期限与幅度如何？它是处于初期、末期还是中间阶段？
row = size(original_time,1); disp(all_static_data{5}); disp(all_static_data{6}); disp(all_static_data{8}); disp(all_static_data{9});  ChangeAttentionStock(stock_code,'w');
disp(all_static_data{4});icon1 = original_data(:,22) == 1; WriteSpecialDate( cellstr( datestr( original_time(icon1),'yyyy-mm-dd') ),'2');disp( sum(icon1)/row )
icon1 = original_data(:,17) == 1; WriteSpecialDate('D:\SpecialDate\SpecialDate.txt',cellstr( datestr( original_time(icon1),'yyyy-mm-dd') ),'3');disp( sum(icon1)/row )
icon1 = original_data(:,18) == 1; WriteSpecialDate('D:\SpecialDate\SpecialDate.txt',cellstr( datestr( original_time(icon1),'yyyy-mm-dd') ),'4');disp( sum(icon1)/row )
icon1 = original_data(:,19) == 1; WriteSpecialDate('D:\SpecialDate\SpecialDate.txt',cellstr( datestr( original_time(icon1),'yyyy-mm-dd') ),'5');disp( sum(icon1)/row ) 
icon1 = original_data(:,20) == 1; WriteSpecialDate('D:\SpecialDate\SpecialDate.txt',cellstr( datestr( original_time(icon1),'yyyy-mm-dd') ),'6');disp( sum(icon1)/row )
icon1 = original_data(:,21) == 1; WriteSpecialDate('D:\SpecialDate\SpecialDate.txt',cellstr( datestr( original_time(icon1),'yyyy-mm-dd') ),'7');disp( sum(icon1)/row )
WriteSpecialDate( 'D:\SpecialDate\ShortTrendDate.txt',short_cell_data(:,1),short_cell_data);disp( short_cell_data(end,:) );disp(all_static_data{1})




## 
# tdb_connect('114.80.154.34', '10061', 'TDcc012', '24104686');
# tdb_connect('114.80.154.34', '10060', 'TDcc010', '17790769');
# tdb_connect('172.24.182.19', '10010', 'shb_cmy','135246');
# r = tdb_gettransaction('601801.sh', 20161116, 91500000, 20161116, 150000000);
# r1 = tdb_getorder('300164.sz');
# r = tdb_gettransaction('300164.sz'); 
tdb_close();

global w 
w = windmatlab;
w.menu
##  计算大盘
tic; ReAllData();toc;
## 短线交易秘诀
## 市盈率,市净率分析
## 开盘价+波幅
# TS已经完成

## 债券市场、商品市场、黄金市场
#根据我个人的观点，分析市场行为的最佳方法是自上而下。换言之，首先观察驱动经济循环的基本经济力量：其次观察整体股票、债券和商品等市场衍生的趋势；最后则检视个别的股票、债券与商品。 
[bonds_data,~,~,bonds_times,~,~] = w.wsd('000012.SH','close','2000-01-01','2017-01-21','Fill=Previous','PriceAdj=CP');
[stock_data,~,~,stock_times,~,~] = w.wsd('000001.SH','close','2000-01-01','2017-01-21','Fill=Previous','PriceAdj=F');
[commodity_data,~,~,commodity_times,~,~] = w.wsd('CCFI.WI','close','2000-01-01','2017-01-21','Fill=Previous','PriceAdj=F');

icon = ~(isnan(bonds_data) | isnan(stock_data) | isnan(commodity_data));
temp_bonds_data = bonds_data(icon);
temp_stock_data = stock_data(icon);
temp_time = datestr(stock_times(icon),'yyyy-mm-dd');
plot(bonds_data(icon),stock_data(icon))
## 止损、止盈的设定

## 资金管理

## 识别买方和卖方
recent_data  = [ max( original_data(end-3:end,2) ),min( original_data(end-3:end,3) ),mean( original_data(end-3:end,2) - original_data(end-3:end,3) ) ];

## 专业投机原理
## 技术分析、统计方法、经济基本面
