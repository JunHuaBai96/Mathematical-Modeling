import pandas as pd
from sklearn.preprocessing import StandardScaler

# 加载处理后的数据
data = pd.read_excel('data-1.xlsx', header=0)

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
standardized_df.to_excel('standardized_data-1.xlsx', index=False)

print("数据标准化处理完成，并保存为 'standardized_data-1.xlsx'")
