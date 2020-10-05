# importing libraries

from pandas_datareader import data as web, wb, quandl as quandl
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
from matplotlib import pyplot as plt
sns.set_style('whitegrid')


# setting start and end dates for the analysis
start = datetime.date(year=2006, month=1,day=1)
end = datetime.date(year=2016, month=1,day=1)

# importing stocks data and preparing data

BAC = web.DataReader('BAC.US', 'quandl', start='2006-01-01', end='2016-01-01', api_key='ufEPgWRnkEaUnp652z2y')
C = web.DataReader('C.US', 'quandl', start='2006-01-01', end='2016-01-01', api_key='ufEPgWRnkEaUnp652z2y')
GS = web.DataReader('GS.US', 'quandl', start='2006-01-01', end='2016-01-01', api_key='ufEPgWRnkEaUnp652z2y')
JPM = web.DataReader('JPM.US', 'quandl', start='2006-01-01', end='2016-01-01', api_key='ufEPgWRnkEaUnp652z2y')
MS = web.DataReader('MS.US', 'quandl', start='2006-01-01', end='2016-01-01', api_key='ufEPgWRnkEaUnp652z2y')
WFC = web.DataReader('WFC.US', 'quandl', start='2006-01-01', end='2016-01-01', api_key='ufEPgWRnkEaUnp652z2y')

tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

# consolidating data to a single dataframe

bank_stock = pd.concat(keys=tickers, objs=[BAC, C, GS, JPM, MS, WFC], axis=1)
bank_stock.columns.names = ['Bank Ticker','Stock Info']
bank_stock = bank_stock.reindex(index=bank_stock.index[::-1])

# Exploration data analysis
# max close price for each bank
bank_stock.xs(key='Close',axis=1,level='Stock Info').max()

# empty dataframe returns
returns = pd.DataFrame()

# close returns
a = bank_stock.pct_change()
for stock in tickers:
    returns[str(stock) + ' return'] = a[stock, 'Close']

# pairplot
sns.pairplot(returns)
plt.tight_layout()

# najgorsze i najlepsze obserwacje
returns.min()
returns.max()

returns.idxmin() # biggest crysis in the market
returns.idxmax()

# standard deviation - risk analysis
returns.std() # during whole period, GS was the least risky investment
returns[returns.index.year == 2015].std() # in 2015 WFC was the least risky investment with standard deviation 0,013

sns.distplot(a=returns['MS return'][returns.index.year == 2015], bins=50, color='red')
sns.distplot(a=returns['C return'][returns.index.year == 2008], bins=50, color='purple')

# MORE VISUALIZATIONSSSS

for tick in tickers:
    bank_stock[tick]['Close'].plot(figsize=(12,4),label=tick)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

bank_stock.xs(key='Close',axis=1,level='Stock Info').plot()

BAC = BAC.reindex(index=BAC.index[::-1])
BAC.reset_index(inplace=True)


plt.figure(figsize=(12,6))
BAC['Close'].ix[502:755].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].ix[502:755].plot(label='BAC CLOSE')
plt.legend()


plt.figure(figsize=(12,6))
sns.heatmap(data=bank_stock.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True)
plt.show()

plt.figure(figsize=(12,6))
sns.clustermap(data=bank_stock.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True)
plt.show()


# import plotly
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
print(__version__) # requires version >= 1.9.0
plotly.io.renderers.default = 'browser'
# import cufflinks
import cufflinks as cf
# For offline use
cf.go_offline()

BAC[['Open', 'High', 'Low', 'Close']].loc['2015-01-01':'2016-01-01'].iplot(kind='candle') # needs to be this order of cols
BAC['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='sma', periods=[15,21,30])
BAC['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='boll')

MS.reindex(index=MS.index[::-1])
MS['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='sma')