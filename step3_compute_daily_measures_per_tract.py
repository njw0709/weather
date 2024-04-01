import numpy as np
import geopandas as gpd
import time
import os
from tqdm import tqdm
import pandas as pd
from tqdm import tqdm
import netCDF4 as nc
from cdr_weather import constants

print("Loading tract shape file...")
# load shape file and raster weights
tract_shape_location = "/data/Heat/data/raw/shape/us_tract_2010"
tract_shape_file = "US_tract_2010.shp"
gdf = gpd.read_file(os.path.join(tract_shape_location, tract_shape_file))

# subset only contiguous US
gdf = gdf[~gdf["STATEFP10"].isin(constants.NON_CONTIGUOUS_STATES)]

print("Loading raster weights...")
df_weights = pd.read_hdf(
    os.path.join(tract_shape_location, "tract_raster_weights.h5"), key="weights"
)
# merge weights with tract geometry on GEOID10
gdf = gdf.merge(df_weights, on="GEOID10")


# compute heat index for each tract
raster_location = "/data/Heat/data/raw/gridMet"
available_years = [
    int(f.split("_")[1].split(".")[0])
    for f in os.listdir(raster_location)
    if f.endswith("nc") and f.startswith("hi")
]
available_years.sort()

# create numpy array of size (num_years, num_tracts, num_days)
# this will be used to store the daily heat index for each tract
num_years = len(available_years)
num_tracts = gdf.shape[0]
save_dir = "/data/Heat/data/processed/daily_measures"


geoid_list = gdf["GEOID10"].tolist()

data_types = {
    # "tmmx": "air_temperature",
    # "tmmn": "air_temperature",
    # "rmax": "relative_humidity",
    # "rmin": "relative_humidity",
    # "hi": "heat_index"
    "wc": "wind_chill",
    "pr": "precipitation_amount",
    }

# loop through each year
for year in available_years:
    # TODO: load in other measures such as tmmx, tmmn, rmax, rmin, and compute per-tract measures.
    
    for dtype, key in data_types.items():
        # load raster
        raster_file = os.path.join(raster_location, "{}_{}.nc".format(dtype, year))

        # Read the entire raster data
        print("Reading {} for year {}...".format(dtype, year))
        t = time.time()
        with nc.Dataset(raster_file, "r") as data:
            # shape = (num_days, num_rows, num_cols)
            raster_data = data.variables[key][:]
        print("Reading took {} seconds".format(time.time() - t))

        # create placeholder numpy array
        daily_heat_idx_np = np.zeros((num_tracts, raster_data.shape[0]))

        # loop through each tract
        for idx, row in tqdm(gdf.iterrows(), total=gdf.shape[0]):
            # get raster coords
            raster_bbox_coords = row["raster_bbox_coords"]
            # get weight matrix
            weight = row["weight"]
            if weight is None:
                daily_heat_idx_np[idx, :] = np.nan
                continue
            # get subset
            (row_start, row_stop), (col_start, col_stop) = raster_bbox_coords
            hi_data_subset = raster_data[:, row_start:row_stop, col_start:col_stop]
            # compute heat index
            daily_heat_tract = np.sum(hi_data_subset * weight, axis=(1, 2))
            daily_heat_idx_np[idx, :] = daily_heat_tract

        # save to file
        print("Saving {} for year {}...".format(dtype, year))
        t = time.time()

        # format using day index
        daily_index = pd.date_range(
            start="{}-01-01".format(year), end="{}-12-31".format(year)
        )

        # create df with columns = geoid and row_index = day index
        df = pd.DataFrame(daily_heat_idx_np.T, columns=geoid_list, index=daily_index)
        df.to_csv(os.path.join(save_dir, "{}_daily_{}.csv".format(year, dtype)))
        print("Saving took {} seconds".format(time.time() - t))