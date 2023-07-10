import xarray
import numpy as np
import pandas as pd

ds = xarray.Dataset(
    {"foo": (("x", "y"), np.random.rand(4, 5))},
    coords={
        "x": [10, 20, 30, 40],
        "y": pd.date_range("2000-01-01", periods=5),
        "z": ("x", list("abcd")),
    },
)

ds.to_netcdf("new_file.nc")

data_array = xarray.open_dataset("new_file.nc")