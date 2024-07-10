import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns

# 设置字体为 SimHei，用于支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取标准化后的数据
data = pd.read_excel('standardized_data-1.xlsx', header=0)

# 提取工艺参数和性能指标
process_params = data.columns[1:4]  # 工艺参数列
performance_metrics = data.columns[4:]  # 性能指标列

# 创建一个空的DataFrame来存储ANOVA结果
anova_results = pd.DataFrame(columns=['Performance Metric', 'Factor', 'p-value'])

# 对每个性能指标进行双因素ANOVA
for metric in performance_metrics:
    formula = f'{metric} ~ {process_params[0]} * {process_params[1]} * {process_params[2]}'
    model = ols(formula, data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    anova_table = anova_table.reset_index().rename(columns={'index': 'Factor'})
    anova_table['Performance Metric'] = metric
    non_empty_entries = anova_table[['Performance Metric', 'Factor', 'PR(>F)']].rename(columns={'PR(>F)': 'p-value'})
    non_empty_entries = non_empty_entries.dropna(how='all')  # 移除空或全 NA 的条目
    anova_results = pd.concat([anova_results, non_empty_entries])

# 过滤显著结果（p-value < 0.05）
significant_results = anova_results[anova_results['p-value'] < 0.05]

# 可视化ANOVA结果
plt.figure(figsize=(14, 8))
sns.barplot(data=significant_results, x='Performance Metric', y='p-value', hue='Factor')
plt.axhline(y=0.05, color='r', linestyle='--')
plt.xlabel('性能指标', fontsize=14)
plt.ylabel('p-value', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='因子', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# 保存图表
plt.savefig('ANOVA_Results.png')
plt.savefig('ANOVA_Results.pdf')

plt.show()