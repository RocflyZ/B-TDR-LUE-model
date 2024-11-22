import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import skill_metrics as sm

# 输入统计数据
labels = ["CRO", "DBF", "EBF", "ENF", "GRA", "MF"]
observed_sd = 2
model_sd = [5.84780645898745, 2.74482946825848, 2.47685455030566, 3.49049666046591, 3.42622144322749, 2.25701870892539]
correlation = [0.862554346113913, 0.864291617453276, 0.764198926981712, 0.736885337077622, 0.809938269252664, 0.808084154033477]
rmse = [3.875, 1.436, 1.679, 2.413, 2.46, 1.363]

# 设置matplotlib 基本配置
rcParams["figure.figsize"] = [8, 8]
rcParams["figure.facecolor"] = "white"
rcParams["figure.edgecolor"] = "white"
rcParams["figure.dpi"] = 100
rcParams['lines.linewidth'] = 2
rcParams["font.family"] = "Times New Roman"
rcParams.update({'font.size': 20})
plt.close('all')

# 转换统计数据
sdev = np.array([observed_sd] + model_sd)
ccoef = np.array([1.0] + correlation)
crmsd = np.array([0] + rmse)

# 开始绘图
text_font = {'size': '15', 'weight': 'bold', 'color': 'black'}
fig = sm.taylor_diagram(sdev, crmsd, ccoef, markerLabel=['Ref'] + labels,
                         markerLabelColor='k', markerLegend='on', colCOR='gray', styleCOR='--', widthCOR=1.0,
                         colRMS='orange', styleRMS='-', widthRMS=1.5, tickRMS=[0, 1, 2, 3, 5],
                         colSTD='k', styleSTD='-', widthSTD=1)

# 强制设置标准偏差的范围
plt.gca().set_xlim(0, 8)
plt.gca().set_ylim(0, 8)

plt.title("TDR-LUE Model", fontdict=text_font, pad=20)

# 保存图像为JPEG格式，300 DPI
plt.savefig("TDR-LUE-1.jpg", dpi=300, bbox_inches='tight')

# 显示图像
plt.show()
