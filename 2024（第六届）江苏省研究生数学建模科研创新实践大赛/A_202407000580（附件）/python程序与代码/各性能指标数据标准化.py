import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 设置字体为 SimHei，用于支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载处理后的数据
data = pd.read_excel('data.xlsx', header=0)

# 提取实验组数据（不包括第一行和最后一行）并转换为数值类型
experimental_data = data.iloc[1:-1, 1:].apply(pd.to_numeric, errors='coerce')

# 初始化StandardScaler
scaler = StandardScaler()

# 对数据进行标准化处理
standardized_data = scaler.fit_transform(experimental_data)

# 将标准化后的数据转换为DataFrame，并添加列名
standardized_df = pd.DataFrame(standardized_data, columns=experimental_data.columns)

# 添加实验组编号列
standardized_df.insert(0, '实验组编号', data.iloc[1:-1, 0].values)

# 保存标准化后的数据到新的Excel文件
standardized_df.to_excel('standardized_data.xlsx', index=False)

print("数据标准化处理完成，并保存为 'standardized_data.xlsx'")

# 可视化标准化后的数据
plt.figure(figsize=(14, 8))
for column in standardized_df.columns[1:]:
    plt.plot(standardized_df['实验组编号'], standardized_df[column], marker='o', label=column)

plt.xlabel('实验组编号')
plt.ylabel('标准化值')
plt.legend()
plt.grid(True)
plt.xticks(range(1, len(standardized_df) + 1))  # 设置横坐标的分度值为1
plt.tight_layout()
plt.savefig('Standardized_Performance_Comparison.png')
plt.savefig('Standardized_Performance_Comparison.pdf')
plt.show()
