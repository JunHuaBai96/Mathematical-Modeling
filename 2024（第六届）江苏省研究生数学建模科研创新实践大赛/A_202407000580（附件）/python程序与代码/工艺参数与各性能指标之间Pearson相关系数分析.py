import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 设置字体为 SimHei，用于支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载标准化后的数据
data = pd.read_excel('standardized_data-1.xlsx')

# 提取工艺参数和性能指标的数据
process_parameters = data.iloc[:, 1:4]
performance_indicators = data.iloc[:, 4:]

# 计算工艺参数与性能指标之间的Pearson相关系数
correlation_matrix = pd.concat([process_parameters, performance_indicators], axis=1).corr()

# 提取工艺参数与性能指标之间的相关系数部分
correlation_process_performance = correlation_matrix.iloc[:3, 3:]

# 设置字体大小
plt.rcParams.update({'font.size': 14})

# 可视化相关系数矩阵
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_process_performance, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.xlabel('性能指标', fontsize=16)
plt.ylabel('工艺参数', fontsize=16)
plt.tight_layout()

# 保存图表
plt.savefig('Process_Performance_Correlation.png')
plt.savefig('Process_Performance_Correlation.pdf')

# 显示图表
plt.show()

print("相关性分析完成，并生成图表 'Process_Performance_Correlation.png' 和 'Process_Performance_Correlation.pdf'")
