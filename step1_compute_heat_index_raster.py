import os
import netCDF4 as nc
from tqdm import tqdm
from cdr_weather import heat_index as hi
from cdr_weather import rasterutils

# raster file directory
raster_location = "/data/Heat/data/raw/gridMet"


# list all tmmx.nc files
raster_temp_list = [
    os.path.join(raster_location, f)
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("tmmx")
]

# list all rmin.nc files
raster_humid_list = [
    os.path.join(raster_location, f)
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("rmin")
]
raster_temp_list.sort()
raster_humid_list.sort()

# get all available years for temperature and humidity
available_years_temp = [
    int(f.split("_")[1].split(".")[0])
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("tmmx")
]
available_years_humid = [
    int(f.split("_")[1].split(".")[0])
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("rmin")
]
available_years_temp.sort()
available_years_humid.sort()

# check if all available years match
assert available_years_temp == available_years_humid

# check if raster grid boundary definitions match
f1 = raster_temp_list[0]
for f2 in raster_temp_list[1:]:
    rasterutils.check_raster_definition_match(f1, f2)
for f2 in raster_humid_list:
    rasterutils.check_raster_definition_match(f1, f2)


# compute heat index and save to file
available_years_temp = [2022, 2023]
for year in tqdm(available_years_temp):
    # save name
    hi_file_name = os.path.join(raster_location, "hi_{}.nc".format(year))

    # load files
    air_temp_file_name = os.path.join(raster_location, "tmmx_{}.nc".format(year))
    relative_humidity_file_name = os.path.join(
        raster_location, "rmin_{}.nc".format(year)
    )
    with nc.Dataset(relative_humidity_file_name, "r") as data:
        relative_humidity = data.variables["relative_humidity"][:]

    with nc.Dataset(air_temp_file_name, "r") as data:
        air_temp = data.variables["air_temperature"][:]
        dimensions = data.variables["air_temperature"].dimensions
        file_format = data.file_format

        # convert from kelvins to fahrenheit
        air_temp_f = hi.kelvin_to_fahrenheit(air_temp)

        # compute heat index (adjusted)
        heat_index = hi.compute_heat_index_with_adjustments(
            air_temp_f, relative_humidity, masked=True
        )

        # save heat index to file
        with nc.Dataset(hi_file_name, "w", format=file_format) as dst:
            # copy attrs (dimensions, file_format, etc.)
            rasterutils.copy_attrs(data, dst, skip_var=["air_temperature"])
            # save heat index
            rasterutils.save_var(
                dst, "heat_index", heat_index, dimensions, compression="zlib"
            )
