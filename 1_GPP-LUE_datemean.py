# !/usr/bin/env python 3.8
# -*- coding:utf-8 -*-
# @Author   :Rocfly_z
# @Time     :2023/10/14 15:54
# @Software :PyCharm
'''
用于将某年某月某天的数据均值成某年某月数据
1. 在这个路径下有个csv文件D:\Big DP-LUE\data\9-data_handle\LUE-month\GPP-LUE.csv；
2. csv文件中有8列数据，这些数据是以天为单位的，但只有年（如：2002）和月（如：2）的索引，没有天的索引。第一列是年份，第二列是月份，后面的六列表示不同类型的数据；
3. 年份数据是从2001到2014年的，月份是1月到12月的； 年份是“Year”，月份是“month”。此外，第3列到底10列类型数据抬头依次是：'GPPsite', 'GPP_RTL-LUE', 'GPP_BRS-LUE', 'GPP_TRS-LUE', 'LUEsite', 'LUE_RTL-LUE', 'LUE_BRS-LUE', 'LUE_TRS-LUE'。
4. 我想将同一年且同一月下的第3到8列的6组数据中，同一种数据进行均值。由于存在某一天数据空值，那直接把这一天去掉就行，如果这个月都是空值，那就把这个月去掉；
5. 最后也用csv文件保存，得到7列数据。第一列是年+月（如：200202）的索引，第2到7列是不同类型数据在相同年相同月下的均值。此外第一行表示抬头，第一行第一列的抬头时“date”，第一行的其他六列分别对应原csv文件的第一行的六种不同类型数据的名字。
'''
import pandas as pd


# 读取原始CSV文件
df = pd.read_csv(r'D:\Big DP-LUE\data\9-data_handle\GPPLUE_yearmean\GPP-LUE.csv')

# 设置新的列名
new_columns = ['date', 'GPPsite', 'GPP_EC-LUE', 'GPP_CI-LUE', 'GPP_TL-LUE', 'GPP_RTL-LUE', 'GPP_BRS-LUE', 'GPP_TRS-LUE']

# 创建新的DataFrame用于存储结果
new_df = pd.DataFrame(columns=new_columns)

# 遍历每一年和每一月
for year in range(2001, 2015):
    for month in range(1, 13):  # 获取同一年同一月的数据
        month_data = df[(df['Year'] == year) & (df['month'] == month)]
        if len(month_data) > 0:  # 检查是否有数据
            mean_values = month_data.iloc[:, 2:].mean().values.tolist()  # 计算每一列的均值——从3列开始算
        else:
            mean_values = [None] * 7  # 如果没有数据，则将同一行参数均值设置为空值

        new_df.loc[len(new_df)] = [f'{year}{month:02d}'] + mean_values  # 将结果添加到新的DataFrame中

# 将结果保存为新的CSV文件
new_df.to_csv(r'D:\Big DP-LUE\data\9-data_handle\GPPLUE_yearmean\GPP-LUE-averaged.csv', index=False)