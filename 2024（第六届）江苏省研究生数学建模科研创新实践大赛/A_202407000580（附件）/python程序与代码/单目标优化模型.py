import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols  # 确保导入ols

# 设置字体为 SimHei，用于支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
data = pd.read_excel('data-1.xlsx', header=0)

# 去掉前两行非数据行
data = data.drop([0, 1]).reset_index(drop=True)

# 将工艺参数和性能指标转换为数值类型
data = data.apply(pd.to_numeric, errors='coerce')

# 提取工艺参数和性能指标
process_params = data.columns[1:4]  # 工艺参数列
performance_metrics = data.columns[4:]  # 性能指标列

# 定义目标函数
def objective_function(params, metric, data):
    data_copy = data.copy()
    data_copy[process_params[0]] = params[0]
    data_copy[process_params[1]] = params[1]
    data_copy[process_params[2]] = params[2]
    model = ols(f'Q("{metric}") ~ Q("{process_params[0]}") * Q("{process_params[1]}") * Q("{process_params[2]}")', data=data_copy).fit()
    return -model.rsquared_adj

# 定义工艺参数的边界
bounds = [(data[process_params[0]].min(), data[process_params[0]].max()),
          (data[process_params[1]].min(), data[process_params[1]].max()),
          (data[process_params[2]].min(), data[process_params[2]].max())]

# 定义初始猜测值
initial_guess = [data[process_params[0]].mean(), data[process_params[1]].mean(), data[process_params[2]].mean()]

# 最优力学性能
result_mechanical = minimize(objective_function, initial_guess, args=('断裂强力', data), bounds=bounds, method='L-BFGS-B')
optimal_mechanical = result_mechanical.x

# 最优热湿舒适性
result_thermal = minimize(objective_function, initial_guess, args=('透湿率', data), bounds=bounds, method='L-BFGS-B')
optimal_thermal = result_thermal.x

# 最优柔软性能
result_softness = minimize(objective_function, initial_guess, args=('柔软度', data), bounds=bounds, method='L-BFGS-B')
optimal_softness = result_softness.x

# 输出结果
optimal_params_df = pd.DataFrame({
    '性能类型': ['力学性能', '热湿舒适性', '柔软性能'],
    '树脂含量': [optimal_mechanical[0], optimal_thermal[0], optimal_softness[0]],
    '固化温度': [optimal_mechanical[1], optimal_thermal[1], optimal_softness[1]],
    '碱减量程度': [optimal_mechanical[2], optimal_thermal[2], optimal_softness[2]]
})

optimal_params_df.to_excel('optimal_process_parameters_single_objective.xlsx', index=False)

# 可视化结果
plt.figure(figsize=(14, 8))
metrics = ['断裂强力', '透湿率', '柔软度']
optimal_values = [optimal_mechanical, optimal_thermal, optimal_softness]

for i, metric in enumerate(metrics):
    plt.subplot(1, 3, i + 1)
    formula = f'Q("{metric}") ~ Q("{process_params[0]}") * Q("{process_params[1]}") * Q("{process_params[2]}")'
    model = ols(formula, data=data).fit()
    sns.scatterplot(x=model.fittedvalues, y=data[metric], s=100)
    plt.plot([data[metric].min(), data[metric].max()], [data[metric].min(), data[metric].max()], 'r--')
    plt.xlabel('拟合值')
    plt.ylabel('实际值')
    plt.title(metric)

plt.tight_layout()
plt.savefig('optimal_process_parameters_single_objective_visualization.png')
plt.savefig('optimal_process_parameters_single_objective_visualization.pdf')
plt.show()
