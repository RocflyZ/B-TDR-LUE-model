import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import skill_metrics as sm

# 输入统计数据
labels = ["CRO", "DBF", "EBF", "ENF", "GRA", "MF"]
observed_sd = 2
model_sd = [6.394706413, 2.529509101, 2.293903679, 3.195140355, 3.645741738, 2.079992494]
correlation = [0.880908622, 0.844985207, 0.777174369, 0.717635005, 0.794355084, 0.778460018]
rmse = [3.563, 1.519, 1.695, 2.474, 2.477, 1.477]

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
                         colRMS='orange', styleRMS='-', widthRMS=1.5, tickRMS=[0, 1, 2, 3, 4],
                         colSTD='k', styleSTD='-', widthSTD=1)

# 强制设置标准偏差的范围
plt.gca().set_xlim(0, 8)
plt.gca().set_ylim(0, 8)

plt.title("BDR-LUE Model", fontdict=text_font, pad=20)

# 保存图像为JPEG格式，300 DPI
plt.savefig("BDR-LUE-1.jpg", dpi=300, bbox_inches='tight')

# 显示图像
plt.show()
