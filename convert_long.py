import pandas as pd
import os
from tqdm import tqdm

# load the data
daily_measures_dir = "/data/weather/data/processed/daily_measures/"
all_files = [f for f in os.listdir(daily_measures_dir) if f.endswith(".csv")]
long_daily_measures_dir = "/data/weather/data/processed/daily_measures_long/"
os.makedirs(long_daily_measures_dir, exist_ok=True)

for file in tqdm(all_files):
    measure = file.split("_")[-1].split(".")[0]
    print(measure)
    print("processing {}....".format(file))
    df = pd.read_csv(os.path.join(daily_measures_dir, file), parse_dates=["Unnamed: 0"])
    df = df.rename(columns={"Unnamed: 0": "Date"})
    long_df = df.melt(id_vars=["Date"], var_name="GEOID10", value_name=measure)
    # convert K to C
    if measure == "tmmx" or measure == "tmmn":
        long_df[measure] = long_df[measure] - 273.15
    long_df.to_csv(os.path.join(long_daily_measures_dir, file), index=False)
