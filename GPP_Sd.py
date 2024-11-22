# -*- coding=utf-8 -*-
# 2021-03-18
# python3.7
# 计算相关系数和误差指标，绘制带有colorbar的散点图
# 2021-12-13更改：①增加色带图例，②修改标签位置，③修改上标字体格式

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # 绘图库
import matplotlib.colors as colors
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms
from matplotlib import rcParams
from sklearn import metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error
import openpyxl as op
import math

# ---------------------------导入文件和列表---------------------------------
# 导入CSV或xlsx文件----------------------
# df = pd.read_excel('KD_ALL.xlsx', engine='openpyxl')  # DataFrame
# # 第一组值 实际值
# true = df['FLUXNET_KD']
# # 第二组值  预测值
# pred = df['CERES_KD']

df = pd.read_excel('GPP1.xlsx', engine='openpyxl')  # DataFrame
true = df['GPPsite']
pred = df['GPP_BRS-LUE']

# 利用Series将列表转换成新的，pandas可处理的数据
re_true = pd.Series(true)
re_pred = pd.Series(pred)
mo = 0
for x in range(len(re_true)):
    mo += re_pred[x]-re_true[x]
Bias = round(mo/len(re_true), 4)

# -----------------------计算相关系数及误差指标-----------------------------
# 用pandas计算相关系数，round(a, 4)是保留a的前两位小数
corr_gust = round(re_true.corr(re_pred), 4)
# 利用numpy的corrcoef得到相关系数矩阵（向量的相似程度）
# corr_gust = np.corrcoef(true,pred)
# r2_score = round(math.pow(corr_gust, 2), 4)
r2_score = round(metrics.r2_score(re_true, re_pred), 4)
# 利用sklearn计算均方根误差MSE
MSE = round(mean_squared_error(re_true, re_pred), 4)
# MSE = np.sum(np.power((re_true - re_pred),2))/len(re_true)
RMSE = round(np.sqrt(MSE), 4)
MAE = round(mean_absolute_error(re_true, re_pred), 4)
# NMB = round((np.sum(re_pred - re_true) / np.sum(true)), 4)
# MBE = round((np.sum(re_pred - re_true) / len(true)), 4)

# ---------------------------参数设置---------------------------------------
# 计算数据最大最小值，设为坐标轴起止值
if true.max() >= pred.max():
    lineEnd = math.ceil(true.max())  # math.ceil()函数返回大于整数的最小整数值。如果number已经是整数，则返回相同的数字。
else:
    lineEnd = math.ceil(pred.max())
if true.min() <= pred.min():
    lineStart = math.floor(true.min())  # math.floor()函数返回不大于x的最大整数。
else:
    lineStart = math.floor(pred.min())
rag = [lineStart, lineEnd]


# 计算散点密度，用来绘制彩色散点图
def density_calc(x, y, radius):
    """
    散点密度计算（以便给散点图中的散点密度进行颜色渲染）
    :param x:
    :param y:
    :param radius:
    :return:  数据密度
    """
    res = np.empty(len(x), dtype=np.float32)  # np.empty()创建一个没有任何具体值的ndarray数组，dtype：指定输出数组的数值类型
    for i in range(len(x)):
        #print(i)
        res[i] = np.sum((x > (x[i] - radius)) & (x < (x[i] + radius))
                        & (y > (y[i] - radius)) & (y < (y[i] + radius)))
    return res


colormap = plt.get_cmap("jet")  # 色带
font1 = {'family': 'Times New Roman',
         'weight': 'bold',
         'size': 14,
         'color': 'black'
         }
font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 16
         }

#  --------------------------------画散点图---------------------------------
# 画两列表散点图
plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内，该代码写在最开始，在所有其他设置之前，否则失效。
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内，该代码写在最开始，在所有其他设置之前，否则失效。
fig = plt.figure()
plt.subplot(1, 1, 1, aspect='equal')
Z1 = density_calc(true, pred, 1)  # 1可理解为半径为1的圆内点的个数，并以点的个数确定颜色深浅
sc = plt.scatter(true, pred, c=Z1, cmap=colormap, marker=".", s=15,
                 norm=colors.LogNorm(vmin=Z1.min(), vmax=Z1.max()))


# plt.legend(loc="lower right")  #添加图例
plt.xlabel("GPP$_{FLUXNET}$ (gC $m^{-2} day^{-1}$)", fontdict=font2)  # 设置横轴标签
plt.ylabel("GPP$_{BRS-LUE}$ (gC $m^{-2} day^{-1}$)", fontdict=font2)  # 设置纵轴标签
# plt.xlim(rag)  # x轴取值范围
# plt.ylim(rag)  # y轴取值范围
plt.xlim(0, 40)
plt.ylim(0, 40)
# plt.xlim(0, 55)
# plt.ylim(0, 55)  # APSIM DSSAT
# plt.xticks(fontproperties='Times New Roman', size=15, weight='bold')
# plt.yticks(fontproperties='Times New Roman', size=15, weight='bold')
plt.xticks(fontproperties='Times New Roman', size=16, weight='normal')
plt.yticks(fontproperties='Times New Roman', size=16, weight='normal')

# 色带图例
# cbar = plt.colorbar(sc, ticks=np.linspace(0, 10000, 5))
cbar = plt.colorbar(sc, ticks=(0, 10, 100, 1000))
cbar.set_label("Scatter Density", fontdict=font2)
cbar.ax.tick_params(which="major", direction="in", length=13, labelsize=15, width=0.5)  # 主刻度
cbar.ax.tick_params(which="minor", direction="in", length=0)  # 副刻度

# 计算趋势线
z = np.polyfit(true, pred, 1)  # np.polyfit函数：采用的是最小二次拟合,1是阶数
p = np.poly1d(z)  # np.polyld函数：得到多项式系数，按照阶数从高到低排列
plt.plot(true, p(true), "-", lw=1.5, label="trendline", c='red')
# 添加y=x线
# plt.plot(rag, rag, "--", lw=1, c='black')
plt.plot([0, 40], [0, 40], "--", lw=1, c='black')
# 回归线公式
print("y=%.2fx+(%.2f)" % (z[0], z[1]))
# 输出评价指标
print("相关系数（R）：%.4f\n" % corr_gust + "决定系数（r2_score）：%.4f\n" % r2_score
      + "均方误差（MSE）：%.4f\n" % MSE + "均方根误差（RMSE）：%.4f\n" % RMSE
      + "平均绝对误差（MAE）：%.4f\n" % MAE + "平均观测误差(Bias): %.4f\n" % Bias)

# 通用趋势线标签
# plt.text(2, 35, "y = %.2fx + %.2f" % (z[0], z[1]), fontdict=font1)
# plt.text(1, 33, "y = %.2fx + %.2f" % (z[0], z[1]), fontdict=font1)
# 通用趋势线标签,指标标签
plt.text(1.5, 27.5, "y = %.2fx + %.2f\n" % (z[0], z[1]) + 'R² = %.3f\n' % r2_score + 'RMSE = %.3f\n' % RMSE + 'MAE = %.3f\n' % MAE + 'Bias = %.3f' % Bias,
       fontdict=font2)
# plt.text(1.5, 27.5, "y = %.2fx + %.2f\n" % (z[0], z[1]) + 'R² = %.3f\n' % r2_score + 'RMSE = %.3f\n' % RMSE + 'MAE = 1.803\n' + 'Bias = 0.332',
#          fontdict=font2)



# 以下两句可将上标字体更改为Times New Roman
plt.rcParams['font.family'] = "Times New Roman"
plt.rcParams['mathtext.default'] = 'regular'
# 更改全局字体（有这一句可取消plt.xticks的设置，但仅这一句无法修改上标字体）
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['savefig.dpi'] = 300  # 设置保存图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率

# 保存图片
# savefig_name = r"D:\Test\plot\scatter\pre_KD_ALL.jpg"
fig.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
# plt.savefig(savefig_name, dpi=500)
plt.show()
