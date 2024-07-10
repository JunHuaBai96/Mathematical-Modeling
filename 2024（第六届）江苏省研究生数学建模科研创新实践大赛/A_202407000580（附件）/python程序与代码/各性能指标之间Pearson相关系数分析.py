import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 设置字体为 SimHei，用于支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载标准化后的数据
data = pd.read_excel('standardized_data-1.xlsx')

# 提取性能指标数据（第5列到第11列）
performance_data = data.iloc[:, 4:]

# 计算Pearson相关系数矩阵
correlation_matrix = performance_data.corr(method='pearson')

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)

# 设置图表标题和轴标签字体大小
plt.xlabel('性能指标', fontsize=14)
plt.ylabel('性能指标', fontsize=14)

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig('Performance_Correlation_Matrix.png')
plt.savefig('Performance_Correlation_Matrix.pdf')

# 显示图像
plt.show()
