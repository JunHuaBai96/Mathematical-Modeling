import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 加载实验数据文件，跳过前三行，并且不读取第一列
data_1 = pd.read_excel('附件1  断裂强力.xlsx', skiprows=2, usecols=[1], names=['value'])
data_2 = pd.read_excel('附件2  断裂伸长率.xlsx', skiprows=2, usecols=[1], names=['value'])
data_3 = pd.read_excel('附件3  撕裂强力.xlsx', skiprows=2, usecols=[1], names=['value'])
data_4 = pd.read_excel('附件4  透气率.xlsx', skiprows=2, usecols=[1], names=['value'])
data_5 = pd.read_excel('附件5  透湿率.xlsx', skiprows=2, usecols=[1], names=['value'])
data_6 = pd.read_excel('附件6  柔软度.xlsx', skiprows=2, usecols=[1], names=['value'])
data_7 = pd.read_excel('附件7  折皱回复角.xlsx', skiprows=2, usecols=[1], names=['value'])

# 将数据转换为数值类型
data_1 = data_1.apply(pd.to_numeric, errors='coerce')
data_2 = data_2.apply(pd.to_numeric, errors='coerce')
data_3 = data_3.apply(pd.to_numeric, errors='coerce')
data_4 = data_4.apply(pd.to_numeric, errors='coerce')
data_5 = data_5.apply(pd.to_numeric, errors='coerce')
data_6 = data_6.apply(pd.to_numeric, errors='coerce')
data_7 = data_7.apply(pd.to_numeric, errors='coerce')

# 计算每3行的平均值和标准差，从数据的第一个数据点开始
def calculate_mean_std(data):
    mean_values = []
    std_values = []
    for i in range(0, len(data), 3):
        subset = data.iloc[i:i+3]
        mean_values.append(subset.mean().iloc[0])
        std_values.append(subset.std().iloc[0])
    return mean_values, std_values

data_1_mean, data_1_std = calculate_mean_std(data_1)
data_2_mean, data_2_std = calculate_mean_std(data_2)
data_3_mean, data_3_std = calculate_mean_std(data_3)
data_4_mean, data_4_std = calculate_mean_std(data_4)
data_5_mean, data_5_std = calculate_mean_std(data_5)
data_6_mean, data_6_std = calculate_mean_std(data_6)
data_7_mean, data_7_std = calculate_mean_std(data_7)

# 确保所有列表长度相同
lengths = [len(data_1_mean), len(data_2_mean), len(data_3_mean), len(data_4_mean), len(data_5_mean), len(data_6_mean), len(data_7_mean)]
min_length = min(lengths)

data_1_mean = data_1_mean[:min_length]
data_1_std = data_1_std[:min_length]
data_2_mean = data_2_mean[:min_length]
data_2_std = data_2_std[:min_length]
data_3_mean = data_3_mean[:min_length]
data_3_std = data_3_std[:min_length]
data_4_mean = data_4_mean[:min_length]
data_4_std = data_4_std[:min_length]
data_5_mean = data_5_mean[:min_length]
data_5_std = data_5_std[:min_length]
data_6_mean = data_6_mean[:min_length]
data_6_std = data_6_std[:min_length]
data_7_mean = data_7_mean[:min_length]
data_7_std = data_7_std[:min_length]

# 创建一个包含所有性能指标平均值和标准差的数据框
mean_std_data = {
    '实验组': list(range(1, min_length + 1)),
    '断裂强力_mean': data_1_mean,
    '断裂强力_std': data_1_std,
    '断裂伸长率_mean': data_2_mean,
    '断裂伸长率_std': data_2_std,
    '撕裂强力_mean': data_3_mean,
    '撕裂强力_std': data_3_std,
    '透气率_mean': data_4_mean,
    '透气率_std': data_4_std,
    '透湿率_mean': data_5_mean,
    '透湿率_std': data_5_std,
    '柔软度_mean': data_6_mean,
    '柔软度_std': data_6_std,
    '折皱回复角_mean': data_7_mean,
    '折皱回复角_std': data_7_std
}

mean_std_df = pd.DataFrame(mean_std_data)

# 将数据保存到 Excel 文件
output_path = 'mean_std_data.xlsx'
mean_std_df.to_excel(output_path, index=False)

# 输出每组实验的平均值和标准差
for i in range(len(data_1_mean)):
    print(f"实验组 {i+1}：")
    print(f"断裂强力 平均值: {data_1_mean[i]}, 标准差: {data_1_std[i]}")
    print(f"断裂伸长率 平均值: {data_2_mean[i]}, 标准差: {data_2_std[i]}")
    print(f"撕裂强力 平均值: {data_3_mean[i]}, 标准差: {data_3_std[i]}")
    print(f"透气率 平均值: {data_4_mean[i]}, 标准差: {data_4_std[i]}")
    print(f"透湿率 平均值: {data_5_mean[i]}, 标准差: {data_5_std[i]}")
    print(f"柔软度 平均值: {data_6_mean[i]}, 标准差: {data_6_std[i]}")
    print(f"折皱回复角 平均值: {data_7_mean[i]}, 标准差: {data_7_std[i]}")
    print()

# 绘制带误差棒的直方图
font = FontProperties(fname='C:/Windows/Fonts/simsun.ttc', size=12)
fig, axs = plt.subplots(4, 2, figsize=(20, 20))
fig.delaxes(axs[3][1])  # 删除多余的子图

colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink']

performance_metrics = {
    '断裂强力': ('断裂强力_mean', '断裂强力_std'),
    '断裂伸长率': ('断裂伸长率_mean', '断裂伸长率_std'),
    '撕裂强力': ('撕裂强力_mean', '撕裂强力_std'),
    '透气率': ('透气率_mean', '透气率_std'),
    '透湿率': ('透湿率_mean', '透湿率_std'),
    '柔软度': ('柔软度_mean', '柔软度_std'),
    '折皱回复角': ('折皱回复角_mean', '折皱回复角_std')
}

for ax, (metric, (mean_col, std_col)), color in zip(axs.flatten(), performance_metrics.items(), colors):
    ax.bar(mean_std_df['实验组'], mean_std_df[mean_col], yerr=mean_std_df[std_col], capsize=4, color=color)
    ax.set_xticks(mean_std_df['实验组'])
    ax.set_xticklabels(mean_std_df['实验组'], fontproperties=font, size=14)
    ax.set_xlabel('实验组', fontproperties=font, size=14)
    ax.set_ylabel(metric, fontproperties=font, size=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)

plt.tight_layout()
plt.savefig('Performance_Indicators_Bar_Chart.pdf')
plt.savefig('Performance_Indicators_Bar_Chart.png')
plt.show()
