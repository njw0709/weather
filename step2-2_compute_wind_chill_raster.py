import os
import netCDF4 as nc
from tqdm import tqdm
from cdr_weather import heat_index as hi
from cdr_weather import wind_chill as wc
from cdr_weather import rasterutils

# raster file directory
raster_location = "/data/Heat/data/raw/gridMet"


# list all tmmn.nc files
raster_temp_list = [
    os.path.join(raster_location, f)
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("tmmn")
]

# list all vs.nc files (wind velocity)
raster_wind_list = [
    os.path.join(raster_location, f)
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("vs")
]
raster_temp_list.sort()
raster_wind_list.sort()

# get all available years for temperature and wind velocity
available_years_temp = [
    int(f.split("_")[1].split(".")[0])
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("tmmn")
]
available_years_wind = [
    int(f.split("_")[1].split(".")[0])
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("vs")
]
available_years_temp.sort()
available_years_wind.sort()

# check if all available years match
assert available_years_temp == available_years_wind

# check if raster grid boundary definitions match
f1 = raster_temp_list[0]
for f2 in raster_temp_list[1:]:
    rasterutils.check_raster_definition_match(f1, f2)
for f2 in raster_wind_list:
    rasterutils.check_raster_definition_match(f1, f2)


# compute heat index and save to file
for year in tqdm(available_years_temp):
    # save name
    wc_file_name_c = os.path.join(raster_location, "wc_celsius_{}.nc".format(year))
    wc_file_name_f = os.path.join(raster_location, "wc_fahrenheit_{}.nc".format(year))

    # load files
    air_temp_file_name = os.path.join(raster_location, "tmmn_{}.nc".format(year))
    wind_velocity_file_name = os.path.join(
        raster_location, "vs_{}.nc".format(year)
    )
    with nc.Dataset(wind_velocity_file_name, "r") as data:
        wind_velocity = data.variables["wind_speed"][:]

    with nc.Dataset(air_temp_file_name, "r") as data:
        air_temp = data.variables["air_temperature"][:]
        dimensions = data.variables["air_temperature"].dimensions
        file_format = data.file_format

        # convert from kelvins to fahrenheit
        # air_temp_c = hi.kelvin_to_celsius(air_temp)
        air_temp_f = hi.kelvin_to_fahrenheit(air_temp)

        # compute wind chill (adjusted)
        # wind_chill_c = wc.compute_wind_chill_celsius(air_temp_c, wind_velocity)
        wind_velocity_mph = wc.meters_per_second_to_mph(wind_velocity)
        wind_chill_f = wc.compute_wind_chill_farhenheit(air_temp_f, wind_velocity_mph)
        
        # # save wind chill to file
        # with nc.Dataset(wc_file_name_c, "w", format=file_format) as dst:
        #     # copy attrs (dimensions, file_format, etc.)
        #     rasterutils.copy_attrs(data, dst, skip_var=["air_temperature"])
        #     # save heat index
        #     rasterutils.save_var(
        #         dst, "wind_chill", wind_chill_c, dimensions, compression="zlib"
        #     )
        with nc.Dataset(wc_file_name_f, "w", format=file_format) as dst:
            # copy attrs (dimensions, file_format, etc.)
            rasterutils.copy_attrs(data, dst, skip_var=["air_temperature"])
            # save heat index
            rasterutils.save_var(
                dst, "wind_chill", wind_chill_f, dimensions, compression="zlib"
            )
