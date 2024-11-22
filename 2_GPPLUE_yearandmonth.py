# !/usr/bin/env python 3.8
# -*- coding:utf-8 -*-
# @Author   :Rocfly_z
# @Time     :2023/10/14 18:53
# @Software :PyCharm
'''
用于将某年某月数据均值成年均值和月均值数据
1. 在这个路径下有个excel文件D:\Big DP-LUE\data\9-data_handle\GPPLUE_yearmean\GPPLUE_result.xlsx；
2. excel文件中6个Sheet，每个Sheet有自己的名字，分别是：'CRO', 'DBF', 'EBF', 'ENF', 'GRA', 'MF'。并且每个Sheet中有7列数据，这些sheet数据属性都相同。第一列为200101到201412是以月为单位的时间数据，这里面前四个字符表示年份，后两个字符表示月份。此外，后面的六列表示不同类型的数据；
3. 第1列到第7列类型数据抬头依次是：'date', GPPsite', 'GPP_BRS-LUE', 'GPP_TRS-LUE', 'LUEsite', 'LUE_BRS-LUE', 'LUE_TRS-LUE'。
4. 我想区分年不区分月份进行均值。由于存在某一月数据空值，那直接把这一月去掉就行。最后也用excel文件保存，得到6个Sheet的7列数据。第一列是年（如：2002）的索引，第2到7列是不同类型数据在相同年份的均值。此外第一行表示抬头，抬头名称与原数据保持一致。每个Sheet的名字也与原excel保持一致。
5. 我也想区分月不区分年进行均值。由于存在某一月数据空值，那直接把这一月去掉就行。最后也用excel文件保存，得到6个Sheet的7列数据。第一列是月（如：1）的索引，第2到7列是不同类型数据在相同月份的均值。此外第一行表示抬头，抬头名称与原数据保持一致。每个Sheet的名字也与原excel保持一致。
6. 分别用两个excel保存。区分年份的保存名为：GPPLUE_year; 区分月份的保存名为：GPPLUE_month。保存位置与原文件位置一样。
'''


import pandas as pd

# 读取原始Excel文件
df = pd.read_excel(r'D:\Big DP-LUE\data\9-data_handle\GPPLUE_yearmean\GPPLUE_result.xlsx', sheet_name=None)

# 创建新的Excel文件用于保存区分年的均值数据
writer_year = pd.ExcelWriter(r'D:\Big DP-LUE\data\9-data_handle\GPPLUE_yearmean\GPPLUE_year1.xlsx')
for sheet_name, sheet_data in df.items():  # 遍历每个Sheet
    sheet_data['date'] = pd.to_datetime(sheet_data['date'], format='%Y%m')  # 将日期列转换为datetime格式
    year_data = sheet_data.groupby(sheet_data['date'].dt.year).mean()  # 计算每一年的均值
    year_data.to_excel(writer_year, sheet_name=sheet_name, index_label='Year')  # 将结果添加到新的Excel文件中
writer_year.save()  # 保存区分年的均值数据到新的Excel文件

# 创建新的Excel文件用于保存区分月的均值数据
writer_month = pd.ExcelWriter(r'D:\Big DP-LUE\data\9-data_handle\GPPLUE_yearmean\GPPLUE_month1.xlsx')
for sheet_name, sheet_data in df.items():  # 遍历每个Sheet
    sheet_data['date'] = pd.to_datetime(sheet_data['date'], format='%Y%m')  # 将日期列转换为datetime格式
    month_data = sheet_data.groupby(sheet_data['date'].dt.month).mean()  # 计算每一月的均值
    month_data.to_excel(writer_month, sheet_name=sheet_name, index_label='Month')  # 将结果添加到新的Excel文件中

# 保存区分月的均值数据到新的Excel文件
writer_month.save()
