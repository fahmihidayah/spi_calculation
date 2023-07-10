from osgeo import gdal
from pathlib import Path

def get_file(file_name: str) -> str:
    path = Path.cwd()
    list_nc_files = list()
    for child in path.iterdir():
        if file_name in str(child.absolute()):
            list_nc_files.append(str(child.absolute()))
    return [result for result in list_nc_files if file_name in result][0]

ds = gdal.Open(get_file('target.tif'))  # Data location
print(ds)
