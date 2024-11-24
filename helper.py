import matplotlib.pyplot as plt

def plotGraph(x, y, x_name, y_name):
  fig = plt.figure()
  plt.plot(y, y)
  plt.title(f'{x_name} vs {y_name}')
  plt.xlabel(x_name)
  plt.xticks(rotation=45)
  plt.ylabel(y_name)
  return fig

def tryFunction(function, **kwargs):
  try:
    return function(**kwargs)
  except Exception as e:
    print(e)
    return []
  
def plot_by_contract(data, x, y, title):
  fig = plt.figure()

  for contract, df in data.items():
    plt.plot(df[x], df[y], label=contract)

  # Customize the plot
  plt.title(title)
  plt.xlabel(x)
  plt.xticks(rotation=45)
  plt.ylabel(y)
  plt.legend(title='Contract', loc='best')

  return fig

def plot_dict_by_contract(date_dict, y, title, contract):
  fig = plt.figure()

  for date, df in date_dict.items():
    for _, row in df.iterrows():
        plt.plot(date, row[y], label=row[contract])

  plt.title(title)
  plt.xlabel('Date')
  plt.xticks(rotation=45)
  plt.ylabel(y)
  plt.legend(title='Contract', loc='best')

  return fig
