"""
基础策略描述：
在2022年11月1日发行产品，那么就以2022年11月1日的黄金价格为原点，
    原点~原点-50的delta是0.5（相当于亏25点，黄金价格是500的话就是亏5%），
    <原点-50的delta归成0，
    原点~原点+50的delta是1，
    >原点+50的delta是0，
按每天调一次仓，维护delta的同时对冲gamma、vega、thata。
年化收益率大于10%敲出，年化低于5%敲入，存续两年，2024年10月31日终止，观察时间间隔3个月。
交易限制：只交易主力合约的期权，所以每两个月要换一次期权。
上面的点位和delta应该是提前设置的，由产品性质决定的，比如要骗投资者“10%及时落袋为安，5%的下跌保护，跌时跌的更慢，涨时涨的更快”就可以用上面的点位和delta；
"""

"""
我们有的数据：
    已知当天的价格，不同行权价的期权在这个价格的delta
需要构建的是：
    已知当天价格，(当天价格-起始点价格)就是策略中的原点偏离多少，那么就知道了当天的目标希腊字母（范围）。
    根据知道的当天的目标希腊字母（范围），就可以求出需要哪些期权。
"""

import pandas as pd
import numpy as np
import pulp
import warnings
warnings.filterwarnings("ignore")

"""
输入格式：
1、期权dataframe数据，
    第1列：期权名称(id)，例如'au2502C500'，'au2502P510'等，str
    第2列：时间(time)，如果是日频就是精确到日期，小时频就是精确到小时，pd.Timestamp，从早到晚排序
    第3列：收盘价（期权价格, close），float
    第4列：成交量(volume)，int
    第5列：持仓量(open_interest)，int
    第6~10列：delta，gamma，theta，vega，rho
2、期货dataframe数据，
    第1列：期货名称(id)
    第2列：时间(time)，从早到晚排序
    第3列：收盘价(close)
3、参数集，就是各点位的希腊字母容忍范围，每列的名称为：[range, delta, gamma, theta, vega, rho]例如：
    range & delta & gamma & theta & vega & rho \\
    [-np.inf, -50] & [-0.1, 0.1] & [-0.1, 0.1] &  [-0.1, 0.1] &  [-0.1, 0.1] &  [-0.1, 0.1] \\
    [-50, 0] & [0.4, 0.6] & [-0.1, 0.1] &  [-0.1, 0.1] &  [-0.1, 0.1] &  [-0.1, 0.1] \\
    [0, 50] & [0.9, 1.1] & [-0.1, 0.1] &  [-0.1, 0.1] &  [-0.1, 0.1] &  [-0.1, 0.1] \\
    [50, np.inf] & [-0.1, 0.1] & [-0.1, 0.1] &  [-0.1, 0.1] &  [-0.1, 0.1] &  [-0.1, 0.1]
    就对应上面的基础策略。
    这时，只要有每天的价格，就能检索出需要的希腊字母。
对应的就是上面的基础策略。这些参数是可能可以优化的。
4、策略起始时间，pd.Timestamp

返回：
"""
def get_trading_signal(option_df: pd.DataFrame, 
                       futures_df: pd.DataFrame, 
                       paras: pd.DataFrame, 
                       start_time: pd.Timestamp):
    
    # 原点价格
    original_price = futures_df[futures_df['time'] < start_time]['close'].iloc[-1]

    target = pd.DataFrame()
    target['time'] = futures_df['time']
    target['deviation'] = futures_df['close'] - original_price # 每日价格相对于原点的偏离量

    # 定义一个函数来找到deviation对应的range
    def find_range(deviation):
        for i, (lower, upper) in enumerate(paras['range']):
            if lower <= deviation <= upper:
                return i
        return None  # 如果deviation不匹配任何range，返回None
    target['range_index'] = target['deviation'].apply(find_range)

    # 根据range_index，从paras中获取对应的参数，现在df包含time, deviation, 目标的希腊字母范围
    paras = paras.reset_index()
    paras = paras.rename(columns={'index': 'range_index'})
    target = target.merge(paras[['range_index', 'delta', 'gamma', 'theta', 'vega', 'rho']], 
                left_on='range_index', 
                right_on='range_index', 
                how='left')
    target.rename(columns={'delta': 'target_delta', 
                       'gamma': 'target_gamma', 
                       'theta': 'target_theta', 
                       'vega': 'target_vega', 
                       'rho': 'target_rho'}, inplace=True)
    target.drop(columns=['range_index'], inplace=True)
    target.reset_index(drop=True, inplace=True)

    # 有了每日的目标的希腊字母范围后，去选择期权来满足目标希腊字母范围
    position_option = pd.DataFrame()
    position_futures = pd.DataFrame()

    for traget_index, target_row in target.iterrows():

        daily_available_option = option_df[option_df['time'] == target_row['time']] # 每天可用的期权
        daily_available_futures = futures_df[futures_df['time'] == target_row['time']] # 每天可用的期权
        
        if daily_available_option.empty: continue

        # 后续每天都是一个整数规划(没有非负约束)，要最小化期权费的同时，满足希腊值的约束（nphard问题，可能会非常慢）
        prob = pulp.LpProblem("Daily_Minimize_option_price", pulp.LpMinimize)
        variables = pulp.LpVariable.dicts("Var", range(len(daily_available_option) + len(daily_available_futures)), 
                                          lowBound=-100, upBound=100, cat='Integer')
        
        # 目标函数：期权费之和
        prob += pulp.lpSum([daily_available_option['close'].iloc[i] * variables[i] for i in range(len(daily_available_option))]), "Objective"
        # 约束：希腊值
        # delta（期货的delta是1）
        prob += pulp.lpSum([daily_available_option['delta'].iloc[i] * variables[i] for i in range(len(daily_available_option))] 
                           + [variables[len(daily_available_option)+i] for i in range(len(daily_available_futures))]) >= target_row['target_delta'][0]
        prob += pulp.lpSum([daily_available_option['delta'].iloc[i] * variables[i] for i in range(len(daily_available_option))]
                           + [variables[len(daily_available_option)+i] for i in range(len(daily_available_futures))]) <= target_row['target_delta'][1]
        # gamma
        prob += pulp.lpSum([daily_available_option['gamma'].iloc[i] * variables[i] for i in range(len(daily_available_option))]) >= target_row['target_gamma'][0]
        prob += pulp.lpSum([daily_available_option['gamma'].iloc[i] * variables[i] for i in range(len(daily_available_option))]) <= target_row['target_gamma'][1]
        # theta
        prob += pulp.lpSum([daily_available_option['theta'].iloc[i] * variables[i] for i in range(len(daily_available_option))]) >= target_row['target_theta'][0]
        prob += pulp.lpSum([daily_available_option['theta'].iloc[i] * variables[i] for i in range(len(daily_available_option))]) <= target_row['target_theta'][1]
        # vega
        prob += pulp.lpSum([daily_available_option['vega'].iloc[i] * variables[i] for i in range(len(daily_available_option))]) >= target_row['target_vega'][0]
        prob += pulp.lpSum([daily_available_option['vega'].iloc[i] * variables[i] for i in range(len(daily_available_option))]) <= target_row['target_vega'][1]

        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        print(f"\nTime: {target_row['time']}")
        print("Status:", pulp.LpStatus[prob.status])

        # 如果求解成功，打印最优值和变量的值
        if prob.status == pulp.LpStatusOptimal:
            print("Optimal value is:", pulp.value(prob.objective))
            variable_values = [v.varValue for v in prob.variables()]
            print("Solution is:", variable_values)
        
        daily_position_option = daily_available_option[['id', 'time']]
        daily_position_option['position'] = variable_values[:len(daily_available_option)]
        position_option = pd.concat([position_option, daily_position_option], ignore_index=True)
        daily_position_futures = daily_available_futures[['id', 'time']]
        daily_position_futures['position'] = variable_values[-1]
        position_futures = pd.concat([position_futures, daily_position_futures], ignore_index=True)

    return position_option, position_futures
