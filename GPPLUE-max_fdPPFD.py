# !/usr/bin/env python
# -*- coding:utf8 -*-
'''
@Time     :2021/11/21 12:22
@Author   :Rocfly_z
@FileName :csv_mod8_o3.py
@Software :PyCharm
'''
import numpy as np
import pandas as pd


# 定义相关参数
targets = ["GPPsitemax"]  # 抬头索引
date_ta = []  # 用于保存结果

datas = pd.read_csv(r'D:\Big DP-LUE\data\9-data_handle\GPPLUE-max_fdPPFD\GPPLUE-max_fdPPFD.csv', encoding='utf-8')  # 提取csv里面的所有数据
dat0_1 = []
dat1_2 = []
dat2_3 = []
dat3_4 = []
dat4_5 = []
dat5_6 = []
dat6_7 = []
dat7_8 = []
dat8_9 = []
dat9_10 = []

#  FLUXNET 站点半小时温度数据一天做均值，并且提取该天最大值和最小值
for k in range(len(datas['fdPPFD'])):  # 遍历csv文件所有行
    data2 = float(datas['fdPPFD'][k])
    data0 = float(datas['LUEsite'][k])      # 读取该行第二列
    if (data2 > 0) and (data2 <= 0.1) and (data0 < 40):
        dat0_1.append(data0)
    elif (data2 > 0.1) and (data2 <= 0.2) and (data0 < 40):
        dat1_2.append(data0)
    elif (data2 > 0.2) and (data2 <= 0.3) and (data0 < 40):
        dat2_3.append(data0)
    elif (data2 > 0.3) and (data2 <= 0.4) and (data0 < 40):
        dat3_4.append(data0)
    elif (data2 > 0.4) and (data2 <= 0.5) and (data0 < 40):
        dat4_5.append(data0)
    elif (data2 > 0.5) and (data2 <= 0.6) and (data0 < 40):
        dat5_6.append(data0)
    elif (data2 > 0.6) and (data2 <= 0.7) and (data0 < 40):
        dat6_7.append(data0)
    elif (data2 > 0.7) and (data2 <= 0.8) and (data0 < 40):
        dat7_8.append(data0)
    elif (data2 > 0.8) and (data2 <= 0.9) and (data0 < 40):
        dat8_9.append(data0)
    elif (data2 > 0.9) and (data2 <= 1) and (data0 < 40):
        dat9_10.append(data0)

date_ta.append(np.mean(dat0_1))
date_ta.append(np.mean(dat1_2))
date_ta.append(np.mean(dat2_3))
date_ta.append(np.mean(dat3_4))
date_ta.append(np.mean(dat4_5))
date_ta.append(np.mean(dat5_6))
date_ta.append(np.mean(dat6_7))
date_ta.append(np.mean(dat7_8))
date_ta.append(np.mean(dat8_9))
date_ta.append(np.mean(dat9_10))

data = pd.DataFrame(data=date_ta, columns=targets)  # 生成数据矩阵
data.to_csv(r'D:\Big DP-LUE\data\9-data_handle\GPPLUE-max_fdPPFD\Save.csv', index=False, header=True)  # 将date_ta内的结果保存成csv文件
print('处理完毕')
