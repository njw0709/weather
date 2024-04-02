import time
import os
import urllib.request
import concurrent.futures
from tqdm import tqdm
from cdr_weather import constants, utils

# set the desired parameters to download - remove if not needed from the list
# please use the following codes to indicate desired parameters
# bi      model-G
# etr     reference alfalfa evapotranspiration
# erc     model-G
# fm100   100-hour dead fuel moisture
# fm1000  1000-hour dead fuel moisture
# pdsi    Palmer drought severity index
# pet     reference grass evapotranspiration
# pr      precipitation
# rmax    maximum near-surface relative humidity
# rmin    minimum near-surface relative humidity
# sph     near-surface specific humidity
# srad    surface downwelling solar radiation
# th      wind direction at 10m
# tmmn    minimum near-surface air temperature
# tmmx    maximum near-surface air temperature
# vpd     mean vapor pressure deficit
# vs      wind speed at 10m
download_parameters = constants.DOWNLOAD_PARAMETER_LIST

# indicate the desired year(s) or range of years to download
years = list(range(1979, 2024))
# years = list(range(2022, 2024))

# save directory
save_dir = "/data/Heat/data/raw/gridMet"

start = time.process_time()
# use concurrent.futures to parallelize the file downloads
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for p in download_parameters:
        for y in years:
            extension = p + "_" + str(y) + ".nc"
            url = constants.DOWNLOAD_BASE_LINK + extension
            destfile = os.path.join(save_dir, extension)
            if os.path.exists(destfile):
                print(f"File already exists: {destfile}")
            else:
                futures.append(executor.submit(utils.download_file, url, destfile))

    # use tqdm to display a progress bar
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
        # check for exceptions in the futures
        if future.exception() is not None:
            print(f"Exception occurred: {future.exception()}")

# prints a message to indicate the end of the script and provide total elapsed time
print("total time elapsed:", round((time.process_time() - start) / 60, 1), "minutes")
print("DOWNLOAD COMPLETE")
