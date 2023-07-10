from pathlib import Path
import os
from netCDF4 import Dataset
import rioxarray
import pandas
import numpy
import matplotlib

def get_file(file_name: str) -> str:
    path = Path.cwd().parent
    list_nc_files = list()
    for child in path.iterdir():
        if file_name in str(child.absolute()):
            list_nc_files.append(str(child.absolute()))
    return [result for result in list_nc_files if file_name in result][0]


data = pandas.read_csv("new_data.csv", usecols=[2])
data = data.set_index(
    pandas.date_range('1959', '1989', freq='M')
)
print(data)