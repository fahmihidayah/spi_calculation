import pandas as pd
import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdatas

np.seterr(divide='ignore')

def spi(ds: pd.DataFrame, thresh):
    # ds - data; thresh - time interval / scale
    # Rolling Mean / Moving Averages
    ds_ma = ds.rolling(thresh, center=False).mean()

    print(ds_ma)
    # Natural Log of moving averages
    ds_ln = np.log(ds_ma)
    ds_ln[np.isinf(ds_ln)] = np.nan

    ds_mu = np.nanmean(ds_ma)
    ds_sum = np.nansum(ds_ln)

    # computing essential for gama distribution
    n = len(ds_ln[thresh-1:])
    A = np.log(ds_mu,) - (ds_sum/n)
    alpha = ((1/4*A) * (1+(1+((4*A)/3))**0.5))
    beta = ds_mu / alpha

    # Gama distribution (CDF)
    gama = st.gamma.cdf(ds_ma, a=alpha, scale=beta)

    norm_spi = st.norm.ppf(gama, loc=0, scale=1)

    return ds_ma, ds_ln, ds_mu, ds_sum, n, A, alpha, beta, gama, norm_spi

# def clean_spi_result(data):
#     return list(map(lambda i: 0 if str(i) == '-inf' or str(i) == 'nan' else i, data))


data = pd.read_csv("new_data.csv", usecols=[2])
data = data.set_index(pd.date_range('1959', '1989', freq='M'))
data.head(5)

times = [3, 6, 9, 12, 24]
result_spi = spi(data['precipitation'], 6)[9]
# print(clean_spi_result(result_spi))
# for time in times:
#     # x = clean_spi_result(spi(data['precipitation'], time)[9])
#     x = spi(data['precipitation'], time)[9]
#     data[f'spi_{str(time)}'] = x

# print(data)
