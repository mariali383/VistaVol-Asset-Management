import akshare as ak
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import helper
import pandas as pd

pdf = PdfPages('plots1.pdf')
# Example Code to access data
# run for every trade date.... first date is 20191220
option_shfe_daily_one, option_shfe_daily_two = ak.option_shfe_daily(symbol="黄金期权", trade_date="20191220")
print("=======SHFE #1=======")
print(list(option_shfe_daily_one))
print("=======SHFE #2=======")
print(list(option_shfe_daily_two))

combined_one_df = {}
combined_two_df = {}

# months = [9, 10, 11]
# days = [30, 31, 30]
months = [11]
days = [10]
for month, days in zip(months, days):
  for i in range(1, days + 1):
    month_str = f"{month:02}"
    day_str = f"{i:02}"
    trade_date = f"2024{month_str}{day_str}" 
    print(trade_date)
    try:
      one_df, two_df = ak.option_shfe_daily(symbol="黄金期权", trade_date=trade_date)
    except Exception as e:
      print(e)
      one_df, two_df = None, None
    combined_one_df[trade_date] = one_df
    combined_two_df[trade_date] = two_df

# get rid of non-trading days
combined_one_df = {k: v for k, v in combined_one_df.items() if v is not None}
combined_two_df = {k: v for k, v in combined_two_df.items() if v is not None}
print(combined_two_df)
print(combined_one_df)

# for all of these, group by contract code/contract series?
# make some plots 
# date vs Closing Price
plot1 = helper.plot_dict_by_contract(combined_one_df, '收盘价', 'date vs 收盘价', '合约代码')
# date vs settlement price
plot2 = helper.plot_dict_by_contract(combined_one_df, '结算价', 'date vs 结算价', '合约代码')
# date vs delta
plot3 = helper.plot_dict_by_contract(combined_one_df, '德尔塔', 'date vs 德尔塔', '合约代码')
# date vs exercise amount 
plot4 = helper.plot_dict_by_contract(combined_one_df, '行权量', 'date vs 行权量', '合约代码')
# date vs implied volatility
plot5 = helper.plot_dict_by_contract(combined_two_df, '隐含波动率', 'date vs 隐含波动率', '合约系列')

pdf.savefig(plot1)
pdf.savefig(plot2)
pdf.savefig(plot3)
pdf.savefig(plot4)
pdf.savefig(plot5)

# plt.plot(option_shfe_daily_one)
option_commodity_contract_sina_df = ak.option_commodity_contract_sina(symbol="黄金期权")
print("=======sina commodity contract=======")
print(option_commodity_contract_sina_df)

# group by symbol?
puts = {}
calls = {}
 
for contract in option_commodity_contract_sina_df['合约']:  
  # print(contract)
  option_commodity_contract_table_sina_df = helper.tryFunction(ak.option_commodity_contract_table_sina, symbol="黄金期权", contract=contract)
  print(f"=======sina commodity contract table for contract {contract}=======")
  # print(option_commodity_contract_table_sina_df)
  # print(f"=======看跌=======")
  for contract_code in option_commodity_contract_table_sina_df['看跌合约-看跌期权合约']:  
    option_commodity_hist_sina_df = helper.tryFunction(ak.option_commodity_hist_sina, symbol=contract_code)
    # print(f"=======sina hist commodity for contract {contract_code}=======")
    # print(option_commodity_hist_sina_df)
    if option_commodity_hist_sina_df is not None:
      puts[contract_code] = option_commodity_hist_sina_df
    break
  # print(f"=======看涨=======")
  for contract_code in option_commodity_contract_table_sina_df['看涨合约-看涨期权合约']:  
    option_commodity_hist_sina_df = helper.tryFunction(ak.option_commodity_hist_sina, symbol=contract_code)
    # print(f"=======sina hist commodity for contract {contract_code}=======")
    # print(option_commodity_hist_sina_df)
    if option_commodity_hist_sina_df is not None:
      calls[contract_code] = option_commodity_hist_sina_df
    break
  break

# date vs close
# date vs open
plot6 = helper.plot_by_contract(puts, 'date', 'close', 'Put: date vs close')
plot7 = helper.plot_by_contract(puts, 'date', 'open', 'Put: date vs open')
plot8 = helper.plot_by_contract(puts, 'date', 'close', 'Call: date vs close')
plot9 = helper.plot_by_contract(puts, 'date', 'open', 'Call: date vs open')

pdf.savefig(plot6)
pdf.savefig(plot7)
pdf.savefig(plot8)
pdf.savefig(plot9)

pdf.close()

# doesn't work
# symbols= ak.option_comm_symbol()
# print(symbols)
# option_comm_info_df = ak.option_comm_info(symbol="黄金期权")
# print(f"=======option comm info=======")
# print(option_comm_info_df)