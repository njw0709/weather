import os
import pandas as pd
from tqdm import tqdm

daily_measure_csv_dir = "/data/Heat/data/processed/daily_measures"
save_dir = "/data/Heat/data/processed/monthly_measures"

tmmx_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("tmmx.csv")]
tmmn_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("tmmn.csv")]
rmax_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("rmax.csv")]
rmin_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("rmin.csv")]
hi_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("heat_index.csv")]
wc_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("wc.csv")]
pr_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("pr.csv")]
all_csvs = tmmx_csvs + tmmn_csvs + rmax_csvs + rmin_csvs + hi_csvs + wc_csvs + pr_csvs

for csvfile in tqdm(all_csvs):
    df = pd.read_csv(csvfile, index_col=0)
    # convert index to datetime
    df.index = pd.to_datetime(df.index)
    # resample to monthly
    monthly_df = df.resample("M").mean()
    # if temperature, convert to Fahrenheit
    if "tmmx" in csvfile or "tmmn" in csvfile:
        monthly_df = (monthly_df - 273.15) * 9/5 + 32
    # change index to month
    monthly_df.index = monthly_df.index.to_period('M')
    
    # save to csv
    csvfile_name = os.path.basename(csvfile)
    new_csv_name = csvfile_name.replace("daily", "monthly")
    # dta_file_name = new_csv_name.replace(".csv", ".dta")
    monthly_df.to_csv(os.path.join(save_dir, new_csv_name))