from pathlib import Path
import os
from netCDF4 import Dataset
import rioxarray
import pandas as pd
import numpy as np
import matplotlib
import xarray as xr
from scipy import stats as st

np.seterr(divide='ignore')


def gama_cdf(data, a, scale):
    return st.gamma.cdf(data, a=a, scale=scale)


def calculate_spi(ds, thresh, dimension):
    ds_ma = ds.rolling(day=thresh, center=False).mean(dimension)
    ds_ln = np.log(ds_ma)
    ds_ln = ds_ln.where(np.isinf(ds_ln) == False)  # = np.nan  #Change infinity to NaN

    # Overall Mean of Moving Averages
    ds_mu = ds_ma.mean(dimension)

    # Summation of Natural log of moving averages
    ds_sum = ds_ln.sum(dimension)

    # Computing essentials for gamma distribution

    n = ds_ln[thresh - 1:, :, :].count(dimension)  # size of data
    A = np.log(ds_mu) - (ds_sum / n)  # Computing A
    alpha = (1 / (4 * A)) * (1 + (1 + ((4 * A) / 3)) ** 0.5)  # Computing alpha  (a)
    beta = ds_mu / alpha  # Computing beta (scale)

    # Gamma Distribution (CDF)
    gamma_func = lambda data, a, scale: st.gamma.cdf(data, a=a, scale=scale)
    gamma = xr.apply_ufunc(gamma_func, ds_ma, alpha, beta)

    # Standardized Precipitation Index   (Inverse of CDF)
    norminv = lambda data: st.norm.ppf(data, loc=0, scale=1)
    norm_spi = xr.apply_ufunc(norminv, gamma)  # loc is mean and scale is standard dev.

    return ds_ma, ds_ln, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi


da_data = xr.open_dataset('pr_2021.nc')
# print(da_data['precipitation_amount'])
rr = da_data['precipitation_amount']
print(rr)
rr = rr.sel(lon=slice(-124.7, -124.6),lat=slice(48.19, 48.15))
result = calculate_spi(rr, 30, 'day')[9]
da_data['spi'] = result
da_data.to_netcdf("spi_result_new.nc")
