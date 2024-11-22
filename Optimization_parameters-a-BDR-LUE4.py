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


targets = ["LUEmsh", "LUEmun", "a", "b", "Bias", "r", "MSE", "MAE", "R2", "RMSE"]  # 抬头索引
date_ta = [[] for i in range(10)]

# ---------------------导入CSV或xlsx文件--------------------------
df = pd.read_excel(r'D:\Big DP-LUE\data\7_data optimization\initial data\CRO1.xlsx', engine='openpyxl')  # DataFrame
true = df['GPP (gC/m2/d)']  # 获取LUE实际值
fPAR = df['fPAR']
PARdif = df['PARdif-PPFD']
PARdir = df['PARdir-PPFD']
PPFD_DIF = df['PPFD_DIF(molPhoton/m2/hh)']
PPFD_DIR = df['PPFD_DIR(molPhoton/m2/hh)']
fdPPFD = df['fdPAR']
ts = df['Ts']  # 获取水分胁迫因子
ws = df['WEF']  # 获取温度胁迫因子

# 利用Series将列表转换成新的，pandas可处理的数据
re_true = pd.Series(true)
re_fPAR = pd.Series(fPAR)
re_PARdif = pd.Series(PARdif)
re_PARdir = pd.Series(PARdir)
re_PPFD_DIF = pd.Series(PPFD_DIF)
re_PPFD_DIR = pd.Series(PPFD_DIR)
re_fdPPFD = pd.Series(fdPPFD)
re_ts = pd.Series(ts)
re_ws = pd.Series(ws)


# 创建步长为1/0.1和0.1/0.01步长的温度和LUE优化数组，pandas可处理的数据
a = np.arange(0.01, 0.02, 0.01)
b = np.arange(0.9, 0.95, 0.01)
LUEmsh = np.arange(2.65, 2.75, 0.01)
LUEmsu = np.arange(2.5, 2.6, 0.01)


nu1 = 0
for sh in range(len(LUEmsh)):
    nu1 += 1
    nu2 = 0
    for su in range(len(LUEmsu)):
        nu2 += 1
        nu3 = 0
        for pa in range(len(a)):
            nu3 += 1
            nu4 = 0
            for pb in range(len(b)):
                nu4 += 1
                pred = []  # LUE预测值
                for m in range(len(re_true)):
                    LCPmsu = re_PARdir[m] * LUEmsu[su] * 1/(b[pb] * re_PPFD_DIR[m] + 1)
                    LCPmsh = re_PARdif[m] * LUEmsh[sh] * re_fdPPFD[m]/(a[pa] * re_PPFD_DIF[m] + 1)
                    LCPmax = LCPmsu + LCPmsh
                    gpp = re_fPAR[m] * LCPmax * re_ws[m] * re_ts[m]
                    pred.append(gpp)

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

                date_ta[0].append(LUEmsh[sh])
                date_ta[1].append(LUEmsu[su])
                date_ta[2].append(a[pa])
                date_ta[3].append(b[pb])
                date_ta[4].append(Bias)
                date_ta[5].append(r)
                date_ta[6].append(MSE)
                date_ta[7].append(MAE)
                date_ta[8].append(R2)
                date_ta[9].append(RMSE)
        print('正在处理：LUEmsh=' + str(LUEmsh[sh]) + '；LUEmsu=' + str(LUEmsu[su]) + '；')
        #      '；a=' + str(a[pa]) + '；b=' + str(b[pb]) + '；')

data = pd.DataFrame({"LUEmsh":date_ta[0], "LUEmun":date_ta[1], "a":date_ta[2], "b":date_ta[3],
                     "Bias":date_ta[4], "r":date_ta[5], "MSE":date_ta[6], "MAE":date_ta[7], "R2":date_ta[8], "RMSE":date_ta[9]})

data.to_csv(r'D:\Big DP-LUE\data\7_data optimization\optimal results\BDR-LUE4\BRS-LUE_CRO4.csv', index=False)  # 将date_ta内的结果保存成csv文件
print('处理完毕')










