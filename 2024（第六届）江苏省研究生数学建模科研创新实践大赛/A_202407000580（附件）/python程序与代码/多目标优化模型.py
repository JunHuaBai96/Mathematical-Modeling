import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
import random
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

# 设置权重
weights = np.array([1, 1, 1, 1, 1, 1, 1])  # 可根据需要调整权重

# 创建优化问题
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()


# 定义基因
def uniform(low, up, size=None):
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]


toolbox.register("attr_float", uniform, low=[data[col].min() for col in process_params],
                 up=[data[col].max() for col in process_params], size=len(process_params))

# 定义个体
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)

# 定义种群
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# 定义目标函数
def objective_function(individual):
    resin_content, curing_temp, alkali_reduction = individual
    data_copy = data.copy()
    data_copy[process_params[0]] = resin_content
    data_copy[process_params[1]] = curing_temp
    data_copy[process_params[2]] = alkali_reduction

    inverse_performance = []
    for metric in performance_metrics:
        model = ols(f'Q("{metric}") ~ Q("{process_params[0]}") * Q("{process_params[1]}") * Q("{process_params[2]}")',
                    data=data_copy).fit()
        predicted = model.fittedvalues.mean()  # 使用预测的均值作为指标值
        inverse_performance.append(1 / predicted)

    objective = np.dot(weights, inverse_performance)
    return objective,


toolbox.register("evaluate", objective_function)

# 定义遗传算法操作
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutPolynomialBounded, low=[data[col].min() for col in process_params],
                 up=[data[col].max() for col in process_params], eta=20.0, indpb=0.2)
toolbox.register("select", tools.selNSGA2)

# 参数设置
population_size = 100
generations = 100

# 创建初始种群
population = toolbox.population(n=population_size)

# 运行遗传算法
result_population, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=population_size,
                                                       cxpb=0.7, mutpb=0.3, ngen=generations, verbose=True)

# 获取优化结果
optimal_individuals = tools.selBest(result_population, k=1)
optimal_params = [ind[:] for ind in optimal_individuals]

# 反标准化工艺参数
optimal_params = [
    [ind[0], ind[1], ind[2]]
    for ind in optimal_params]

# 创建DataFrame存储结果
optimal_params_df = pd.DataFrame(optimal_params, columns=['树脂含量', '固化温度', '碱减量程度'])

# 输出最佳工艺参数组合到excel文件
optimal_params_df.to_excel('optimal_process_parameters_multi_objective.xlsx', index=False)