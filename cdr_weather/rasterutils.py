import rasterio
import netCDF4 as nc
import numpy as np
from typing import Tuple


def check_raster_definition_match(file1: str, file2: str):
    # check if raster definitions match
    with rasterio.open(file1) as temp_src:
        with rasterio.open(file2) as humid_src:
            assert temp_src.crs == humid_src.crs
            assert temp_src.width == humid_src.width
            assert temp_src.height == humid_src.height
            assert temp_src.transform == humid_src.transform
            assert temp_src.bounds == humid_src.bounds


def copy_attrs(src: nc.Dataset, dst: nc.Dataset, skip_var: list = []) -> nc.Dataset:
    # Copy global attributes
    for name in src.ncattrs():
        dst.setncattr(name, src.getncattr(name))

    # Create dimensions
    for name, dimension in src.dimensions.items():
        dst.createDimension(
            name, (len(dimension) if not dimension.isunlimited() else None)
        )

    # Create variables and copy their attributes, but skip "air_temperature"
    for name, variable in src.variables.items():
        if name not in skip_var:
            dst_var = dst.createVariable(name, variable.datatype, variable.dimensions)
            dst[name].setncatts(src[name].__dict__)

    return dst


def save_var(
    dst: nc.Dataset, key: str, data: np.ndarray, dimensions: Tuple, compression="zlib"
) -> nc.Dataset:
    dst.createVariable(key, data.dtype, dimensions, compression=compression)
    dst.variables[key][:] = data
