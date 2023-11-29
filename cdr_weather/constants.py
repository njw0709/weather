# user-set parameters
# set the desired parameters to download
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

DOWNLOAD_PARAMETER_LIST = [
    "bi",
    "etr",
    "erc",
    "fm100",
    "fm1000",
    "pet",
    "pr",
    "rmax",
    "rmin",
    "sph",
    "srad",
    "th",
    "tmmn",
    "tmmx",
    "vpd",
    "vs",
]


DOWNLOAD_BASE_LINK = "http://www.northwestknowledge.net/metdata/data/"

NON_CONTIGUOUS_STATES = [
    "02",  # Alaska
    "15",  # Hawaii
    "72",  # Puerto Rico
]
