# !/usr/bin/env python 3.8
# -*- coding:utf-8 -*-
# @Author   :Rocfly_z
# @Time     :2023/10/10 13:30
# @Software :PyCharm
"""
-  plt.cm.viridis ：Viridis颜色映射，从蓝色到黄色的范围。
-  plt.cm.jet ：Jet颜色映射，从蓝色到红色的范围。
-  plt.cm.cool ：Cool颜色映射，从青色到洋红的范围。
-  plt.cm.hot ：Hot颜色映射，从黑色到红色的范围。
-  plt.cm.gray ：Gray颜色映射，从黑色到白色的范围。
-  plt.cm.spring ：Spring颜色映射，从洋红到黄色的范围。
-  plt.cm.summer ：Summer颜色映射，从绿色到黄色的范围。
-  plt.cm.autumn ：Autumn颜色映射，从红色到黄色的范围。
-  plt.cm.winter ：Winter颜色映射，从蓝色到绿色的范围。
-  plt.cm.bone ：Bone颜色映射，从黑色到白色的范围。
-  plt.cm.copper ：Copper颜色映射，从黑色到铜色的范围。
-  plt.cm.pink ：Pink颜色映射，从粉色到白色的范围。
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# 读取Excel文件
data = pd.read_excel(r'D:\Big DP-LUE\data\9-data_handle\index-matrix\index1.xlsx', sheet_name='Sheet1')

# 提取数值矩阵
matrix = data.iloc[0:, 1:].values

# 绘制矩阵图像，使用红色颜色映射
# 双色渐变色可参照代码开头，单色渐变色还有Reds，Greens，Oranges, Purples, Greys等等
# plt.matshow(matrix, cmap=plt.cm.Blues)
plt.matshow(matrix, cmap=plt.cm.Reds)  # 加个_r,表示颜色倒置

# 在图像上显示具体数值
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        plt.text(j, i+0.2, "%.3f\n" % matrix[i][j], ha='center', va='center',
                 fontname='Times New Roman', fontsize=13)  # j和i是数值的位置

# 去除刻度线
plt.tick_params(axis='both', which='both', bottom=False)  # False

# 设置坐标轴标签
plt.xticks(np.arange(len(matrix[0])), data.columns[1:], fontname='Times New Roman', fontsize=13)
plt.yticks(np.arange(len(matrix)), data.iloc[0:, 0], fontname='Times New Roman', fontsize=13)

# 添加颜色条
cbar = plt.colorbar(shrink=0.8)  # 调整颜色条的高度为0.8
cbar.set_label('colorbar', fontname='Times New Roman', fontsize=13)  # colorbar标题
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontname='Times New Roman', fontsize=13)  # colorbar标签字体
# cbar.ax.set_ylim([1, 3.2])  # 调整颜色条的值为1.8, 4.3
cbar.set_ticks(np.linspace(0.5, 0.77, 7))  # 设置颜色条刻度为1到3.2的6个值

# 将colorbar的数值标签设置为Times New Roman字体，字号设置为13
cbar.ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.2f}'))  # colorbar的数值小数点

# 保存图像为jpg格式
plt.savefig(r'D:\Big DP-LUE\data\9-data_handle\index-matrix\R2.jpg', dpi=1200)

# 显示图像
plt.show()