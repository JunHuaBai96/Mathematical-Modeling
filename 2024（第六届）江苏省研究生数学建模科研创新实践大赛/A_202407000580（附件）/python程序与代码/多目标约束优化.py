import pandas as pd
import numpy as np
from scipy.optimize import minimize
from statsmodels.formula.api import ols

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
def objective_function(params, data):
    data_copy = data.copy()
    data_copy[process_params[0]] = params[0]
    data_copy[process_params[1]] = params[1]
    data_copy[process_params[2]] = params[2]

    # 使用线性回归模型预测力学性能和柔软性能
    mechanical_model = ols(
        f'Q("{performance_metrics[0]}") ~ Q("{process_params[0]}") * Q("{process_params[1]}") * Q("{process_params[2]}")',
        data=data_copy).fit()
    softness_model = ols(
        f'Q("{performance_metrics[-1]}") ~ Q("{process_params[0]}") * Q("{process_params[1]}") * Q("{process_params[2]}")',
        data=data_copy).fit()

    mechanical_pred = mechanical_model.fittedvalues.mean()
    softness_pred = softness_model.fittedvalues.mean()

    # 组合多个目标，将其合并为一个标量值
    weights = [0.5, 0.5]  # 可以根据需要调整权重
    objective_value = weights[0] * -mechanical_pred + weights[1] * -softness_pred

    return objective_value


# 初始工艺参数
initial_guess = [23, 116, 16]

# 定义边界
bounds = [(data[process_params[0]].min(), data[process_params[0]].max()),
          (data[process_params[1]].min(), data[process_params[1]].max()),
          (data[process_params[2]].min(), data[process_params[2]].max())]


# 定义约束条件
def constraint(params):
    resin_content, curing_temp, alkali_reduction = params
    return [resin_content - 23, curing_temp - 116, alkali_reduction - 16]


constraints = [{'type': 'eq', 'fun': lambda x: constraint(x)[0]},
               {'type': 'eq', 'fun': lambda x: constraint(x)[1]},
               {'type': 'eq', 'fun': lambda x: constraint(x)[2]}]

# 运行优化
result = minimize(objective_function, initial_guess, args=(data,), bounds=bounds, constraints=constraints,
                  method='SLSQP')

# 获取最优参数
optimal_params = result.x

# 输出结果
optimal_params_df = pd.DataFrame([optimal_params], columns=['树脂含量', '固化温度', '碱减量程度'])
optimal_params_df.to_excel('optimal_process_parameters_constrained.xlsx', index=False)

print("最优工艺参数组合:", optimal_params)
