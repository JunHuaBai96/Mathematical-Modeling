import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns

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


# 定义目标函数用于优化
def objective_function(params, formula, data):
    data_copy = data.copy()
    data_copy[process_params[0]] = params[0]
    data_copy[process_params[1]] = params[1]
    data_copy[process_params[2]] = params[2]
    model = ols(formula, data=data_copy).fit()
    return -model.rsquared_adj


# 定义初始猜测值和边界
initial_guess = [data[process_params[0]].mean(), data[process_params[1]].mean(), data[process_params[2]].mean()]
bounds = [(data[process_params[0]].min(), data[process_params[0]].max()),
          (data[process_params[1]].min(), data[process_params[1]].max()),
          (data[process_params[2]].min(), data[process_params[2]].max())]

# 创建一个空的DataFrame来存储最佳工艺参数组合
optimal_params_df = pd.DataFrame(columns=['性能指标', '树脂含量', '固化温度', '碱减量程度'])

# 对每个性能指标进行多元线性回归和优化
for metric in performance_metrics:
    formula = f'Q("{metric}") ~ Q("{process_params[0]}") * Q("{process_params[1]}") * Q("{process_params[2]}")'
    result = minimize(objective_function, initial_guess, args=(formula, data), bounds=bounds, method='L-BFGS-B')

    # 检查结果是否为空或全 NA
    result_df = pd.DataFrame([{
        '性能指标': metric,
        '树脂含量': result.x[0],
        '固化温度': result.x[1],
        '碱减量程度': result.x[2]
    }])
    if not result_df.isnull().all().all():
        optimal_params_df = pd.concat([optimal_params_df, result_df], ignore_index=True)

# 输出最佳工艺参数组合到excel文件
optimal_params_df.to_excel('Multiple_Linear_Regression.xlsx', index=False)

# 可视化结果
plt.figure(figsize=(14, 8))
for i, metric in enumerate(performance_metrics):
    plt.subplot(2, 4, i + 1)
    formula = f'Q("{metric}") ~ Q("{process_params[0]}") * Q("{process_params[1]}") * Q("{process_params[2]}")'
    model = ols(formula, data=data).fit()
    sns.scatterplot(x=model.fittedvalues, y=data[metric], s=100)
    plt.plot([data[metric].min(), data[metric].max()], [data[metric].min(), data[metric].max()], 'r--')
    plt.xlabel('拟合值')
    plt.ylabel('实际值')
    plt.title(metric)
plt.tight_layout()
plt.savefig('Multiple_Linear_Regression_visualization.png')
plt.savefig('Multiple_Linear_Regression_visualization.pdf')
plt.show()
