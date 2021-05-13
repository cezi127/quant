from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import math

np.seterr(all='ignore')
rcParams['figure.figsize'] = (14, 6)

from funcat import *

from funcat.data.tushare_backend import TushareDataBackend


set_data_backend(TushareDataBackend())

a = TushareDataBackend()

set_start_date("2020-01-01")
S("300350.SZ")  # 设置当前关注股票
T("2021-05-01")   # 设置当前观察日期


print(O, H, L, C, V)
