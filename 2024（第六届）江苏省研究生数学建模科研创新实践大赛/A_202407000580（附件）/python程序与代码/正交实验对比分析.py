import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 加载处理后的数据和正交实验条件数据
data = pd.read_excel('data.xlsx', header=0)

# 打印列名以确保正确

# 提取基布数据（最后一行）和实验数据（不包括最后一行）
baseline_data = data.iloc[-1, 1:].apply(pd.to_numeric, errors='coerce')
experimental_data = data.iloc[1:-1, 1:].apply(pd.to_numeric, errors='coerce')

# 提取性能指标名称（跳过第一列，即实验编号）
performance_metrics = data.columns[1:]

# 提取实验组编号，并确保其为数值类型
experiment_numbers = data.iloc[1:-1, 0].astype(int)

# 设置中文字体
font = FontProperties(fname='C:/Windows/Fonts/simsun.ttc', size=12)

# 创建一个字典，映射性能指标到单位
metric_units = {
    '断裂强力': 'N',
    '断裂伸长率': '%',
    '撕裂强力': 'N',
    '透气率': 'mm/s',
    '透湿率': 'g/m2·24h',
    '柔软度': 'mm',
    '折皱回复角': '°'
}

# 可视化分析
fig, axs = plt.subplots(4, 2, figsize=(20, 20))
fig.subplots_adjust(hspace=0.5)


# 迭代字典，确保使用metric_units中的键作为metric，值作为unit
for ax, (metric, unit) in zip(axs.flatten(), metric_units.items()):
    if metric in experimental_data.columns:
        ylabel = f'{metric} [{unit}]'
        ax.bar(experiment_numbers, experimental_data[metric], label='实验数据')
        ax.axhline(y=baseline_data[metric], color='r', linestyle='--', label='基布数据')
        ax.set_xlabel('实验组编号', fontproperties=font)  # 将横坐标名称设置为实验组编号
        ax.set_ylabel(ylabel, fontproperties=font)  # 将纵坐标名称设置为性能指标名称和单位
        ax.legend(prop=font)
        ax.set_xticks(experiment_numbers)  # 设置x轴刻度
        ax.set_xticklabels(experiment_numbers, fontproperties=font)  # 设置x轴刻度标签
    else:
        print(f"Metric '{metric}' not found in experimental_data.columns")

# 删除最后一张没有数据的图
if len(metric_units) % 2 != 0:
    fig.delaxes(axs.flatten()[-1])

# 保存和展示图表
plt.tight_layout()
plt.savefig('Performance_Comparison.pdf')  
plt.savefig('Performance_Comparison.png')  
plt.show()
