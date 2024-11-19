import akshare as ak

# run for every trade date.... first date is 20191220
option_shfe_daily_one, option_shfe_daily_two = ak.option_shfe_daily(symbol="黄金期权", trade_date="20191220")
print("=======SHFE #1=======")
print(option_shfe_daily_one)
print("=======SHFE #2=======")
print(option_shfe_daily_two)

option_commodity_contract_sina_df = ak.option_commodity_contract_sina(symbol="黄金期权")
print("=======sina commodity contract=======")
print(option_commodity_contract_sina_df)

print(type(option_commodity_contract_sina_df))
for contract in option_commodity_contract_sina_df['合约']:  
  print(contract)
  option_commodity_contract_table_sina_df = ak.option_commodity_contract_table_sina(symbol="黄金期权", contract=contract)
  print(f"=======sina commodity contract table for contract {contract}=======")
  print(option_commodity_contract_table_sina_df)
  print(f"=======看跌=======")
  for contract_code in option_commodity_contract_table_sina_df['看跌合约-看跌期权合约']:  
    option_commodity_hist_sina_df = ak.option_commodity_hist_sina(symbol=contract_code)
    print(f"=======sina hist commodity for contract {contract_code}=======")
    print(option_commodity_hist_sina_df)
  
  print(f"=======看涨=======")
  for contract_code in option_commodity_contract_table_sina_df['看涨合约-看涨期权合约']:  
    option_commodity_hist_sina_df = ak.option_commodity_hist_sina(symbol=contract_code)
    print(f"=======sina hist commodity for contract {contract_code}=======")
    print(option_commodity_hist_sina_df)

# doesn't work
# symbols= ak.option_comm_symbol()
# print(symbols)
# option_comm_info_df = ak.option_comm_info(symbol="黄金期权")
# print(f"=======option comm info=======")
# print(option_comm_info_df)

