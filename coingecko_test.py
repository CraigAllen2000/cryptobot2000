import requests
import datetime
import numpy as np
import time
import pytz
from stock_tools import *
global z
url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1657670093&to=1657756493'
x = requests.get(url)
X = np.array(convert_time([row[0] for row in x.json()["prices"]]))
Y = [row[1] for row in x.json()["prices"]]

z = []
print(len(z))
z.append(X[-1])
z.append(X[-2])
print(z)