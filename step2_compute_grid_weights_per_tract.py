import geopandas as gpd
import rasterio
import os
from tqdm import tqdm
from cdr_weather import constants, geometry
import pandas as pd

# progress bar setting
tqdm.pandas()

# Load tract boundary definitions (2010)
tract_shape_location = "/data/Heat/shape/us_tract_2010"
tract_shape_file = "US_tract_2010.shp"
print("Loading tract shape file...")
gdf = gpd.read_file(os.path.join(tract_shape_location, tract_shape_file))

# Get only the contiguous US
gdf_contiguous_us = gdf[~gdf["STATEFP10"].isin(constants.NON_CONTIGUOUS_STATES)]

# load raster file (2010) - raster definition matching across years and across temp and humidity
# already checked in step 1
raster_location = "/data/Heat/gridMet"
raster_temp = "tmmx_2010.nc"

print("Computing raster weights for each tract...")
# convert the gdf crs to the raster crs
with rasterio.open(os.path.join(raster_location, raster_temp)) as temp_data:
    crs = temp_data.crs
    gdf_contiguous_us.to_crs(crs, inplace=True)

    # compute bounding boxes for each tract
    gdf_contiguous_us["bounds"] = gdf_contiguous_us["geometry"].apply(
        lambda x: x.bounds
    )

    print("Computing bounding box raster indices for each tract...")
    # compute raster indices for each tract
    gdf_contiguous_us["raster_bbox_coords"] = gdf_contiguous_us["bounds"].apply(
        geometry.convert_bbox_coord_to_raster_index, args=(temp_data,)
    )

    # compute area for each tract
    gdf_contiguous_us["area"] = gdf_contiguous_us["geometry"].area

    print("Computing weight matrix for each tract...")
    # compute weight matrix for each tract
    gdf_contiguous_us["weight"] = gdf_contiguous_us.progress_apply(
        geometry.get_weight_matrix, axis=1, args=(temp_data,)
    )

print("Saving to file...")
# drop geometry column and save to pandas df
df_weights = pd.DataFrame(
    gdf_contiguous_us.loc[
        :, ["raster_bbox_coords", "weight", "area", "GEOID10", "bounds"]
    ]
)

# save to hdf5 file
df_weights.to_hdf(
    os.path.join(tract_shape_location, "tract_raster_weights.h5"),
    key="weights",
    mode="w",
)

print("Done!")
