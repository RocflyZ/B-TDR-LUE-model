# -*- coding=utf-8 -*-
# 2021-03-18
# python3.7
# 计算相关系数和误差指标，绘制带有colorbar的散点图
# 2021-12-13更改：①增加色带图例，②修改标签位置，③修改上标字体格式

# 第一步，根据a，b，LUEmsh和LUEmsu步长为0.1进行优化参数
# 第二步，根据第一步生成的CSV整理RMSE最小，次之R2最大的几组参数
# 第三步，将第二步获得的参数范围再将四个参数按照步长为0.01进行优化参数
# 第四步，根据第三步生成的CSV整理RMSE最小，次之R2最大的最优参数
# 第五步，利用“LUE Sd.py”绘制LUE散点图和“GPP Sd.py”绘制GPP散点图

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error


targets = ["LUEmsu", "LUEmsh", "Bias", "r", "MSE", "MAE", "R2", "RMSE"]  # 抬头索引
date_ta = [[] for i in range(8)]

# ---------------------导入CSV或xlsx文件--------------------------
df = pd.read_excel(r'D:\Big DP-LUE\data\7_data optimization\initial data\MF1.xlsx', engine='openpyxl')  # DataFrame
true = df['GPP (gC/m2/d)']  # 获取LUE实际值
APARsu = df['APARsu-TL']
APARsh = df['APARsh-TL']
ts = df['Ts']  # 获取温度胁迫因子
ws = df['WEF']  # 获取水分胁迫因子

# 利用Series将列表转换成新的，pandas可处理的数据
re_true = pd.Series(true)
re_APARsu = pd.Series(APARsu)
re_APARsh = pd.Series(APARsh)
re_ts = pd.Series(ts)
re_ws = pd.Series(ws)

# 创建步长为1/0.1和0.1/0.01步长的温度和LUE优化数组，pandas可处理的数据
LUEmsu = np.arange(0.8, 1.0, 0.01)
LUEmsh = np.arange(2.7, 2.9, 0.01)

# LUE=LUEmax * min(Ts,Ws)
nu1 = 0
for su in range(len(LUEmsu)):
    nu1 += 1
    nu2 = 0
    for sh in range(len(LUEmsh)):
        nu2 += 1
        pred = []  # LUE预测值
        for m in range(len(re_true)):
            GPP = (re_APARsh[m] * LUEmsh[sh] + re_APARsu[m] * LUEmsu[su]) * re_ts[m] * re_ws[m]
            pred.append(GPP)

        # -----------------------计算相关系数及误差指标-----------------------------
        # 用pandas计算相关系数，round(a, 4)是保留a的前两位小数
        re_pred = pd.Series(pred)
        mo = 0
        for x in range(len(re_true)):
            mo += re_pred[x] - re_true[x]
        Bias = round(mo / len(re_true), 4)
        r = round(re_true.corr(re_pred), 4)
        # 利用numpy的corrcoef得到相关系数矩阵（向量的相似程度）
        # corr_gust = np.corrcoef(true,pred)
        # r2_score = round(math.pow(corr_gust, 2), 4)
        R2 = round(metrics.r2_score(re_true, re_pred), 4)
        # 利用sklearn计算均方根误差MSE
        MSE = round(mean_squared_error(re_true, re_pred), 4)
        # MSE = np.sum(np.power((re_true - re_pred),2))/len(re_true)
        RMSE = round(np.sqrt(MSE), 4)
        MAE = round(mean_absolute_error(re_true, re_pred), 4)
        # NMB = round((np.sum(re_pred - re_true) / np.sum(true)), 4)
        # MBE = round((np.sum(re_pred - re_true) / len(true)), 4)

        date_ta[0].append(LUEmsu[su])
        date_ta[1].append(LUEmsh[sh])
        date_ta[2].append(Bias)
        date_ta[3].append(r)
        date_ta[4].append(MSE)
        date_ta[5].append(MAE)
        date_ta[6].append(R2)
        date_ta[7].append(RMSE)
        # print('已完成LUEmsu=' + str(LUEmsu[su]) + '；LUEmsh=' + str(LUEmsh[sh]) + '的模拟；')
    print('已完成LUEmsu=' + str(LUEmsu[su]) + '的模拟；')


data = pd.DataFrame({"LUEmsu": date_ta[0], "LUEmsh": date_ta[1], "Bias": date_ta[2], "r": date_ta[3],
                    "MSE": date_ta[4], "MAE": date_ta[5], "R2": date_ta[6], "RMSE": date_ta[7]})

data.to_csv(r'D:\Big DP-LUE\data\7_data optimization\optimal results\TL-LUE2\TL-LUE_MF11.csv', index=False)  # 将date_ta内的结果保存成csv文件
print('处理完毕')










