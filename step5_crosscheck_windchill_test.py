import os
import pandas as pd
from tqdm import tqdm
from cdr_weather.heat_index import kelvin_to_fahrenheit
from cdr_weather.reformat import reformat_df

daily_measure_csv_dir = "/data/weather/data/processed/daily_measures"
save_dir = "/data/weather/data/processed/monthly_measures"

# wind chill
print("Processing wind chill, celsius / fahrenheit...")
wc_c_csvs = [
    os.path.join(daily_measure_csv_dir, f)
    for f in os.listdir(daily_measure_csv_dir)
    if f.endswith("wc_celsius.csv")
]
wc_c_csvs.sort()
for i in tqdm(range(len(wc_c_csvs))):
    year = os.path.basename(wc_c_csvs[i]).split("_")[0]
    df_wc_c = pd.read_csv(
        os.path.join(daily_measure_csv_dir, wc_c_csvs[i]), index_col=0, parse_dates=[0]
    )
    df_wc_f = pd.read_csv(
        os.path.join(
            daily_measure_csv_dir, wc_c_csvs[i].replace("celsius", "fahrenheit")
        ),
        index_col=0,
        parse_dates=[0],
    )

    df_wc_c_level0 = df_wc_c > 0
    df_wc_c_level0_num_monthly = df_wc_c_level0.resample("M").sum()
    df_wc_c_level0_pct_monthly = df_wc_c_level0.resample("M").mean()
    # m200 -> number of level 0 wind chill days in month
    df_wc_c_level0_num_monthly = reformat_df(df_wc_c_level0_num_monthly, "m200")
    # m210 -> percentage of level 0 wind chill days in month
    df_wc_c_level0_pct_monthly = reformat_df(df_wc_c_level0_pct_monthly, "m210")

    df_wc_c_level1 = (df_wc_c > -10) & (df_wc_c <= 0)
    df_wc_c_level1_num_monthly = df_wc_c_level1.resample("M").sum()
    df_wc_c_level1_pct_monthly = df_wc_c_level1.resample("M").mean()
    # m201 -> number of level 1 wind chill days in month
    df_wc_c_level1_num_monthly = reformat_df(df_wc_c_level1_num_monthly, "m201")
    # m211 -> percentage of level 1 wind chill days in month
    df_wc_c_level1_pct_monthly = reformat_df(df_wc_c_level1_pct_monthly, "m211")

    df_wc_c_level2 = (df_wc_c > -28) & (df_wc_c <= -10)
    df_wc_c_level2_num_monthly = df_wc_c_level2.resample("M").sum()
    df_wc_c_level2_pct_monthly = df_wc_c_level2.resample("M").mean()
    # m202 -> number of level 2 wind chill days in month
    df_wc_c_level2_num_monthly = reformat_df(df_wc_c_level2_num_monthly, "m202")
    # m212 -> percentage of level 2 wind chill days in month
    df_wc_c_level2_pct_monthly = reformat_df(df_wc_c_level2_pct_monthly, "m212")

    df_wc_c_level3 = (df_wc_c > -40) & (df_wc_c <= -28)
    df_wc_c_level3_num_monthly = df_wc_c_level3.resample("M").sum()
    df_wc_c_level3_pct_monthly = df_wc_c_level3.resample("M").mean()
    # m203 -> number of level 3 wind chill days in month
    df_wc_c_level3_num_monthly = reformat_df(df_wc_c_level3_num_monthly, "m203")
    # m213 -> percentage of level 3 wind chill days in month
    df_wc_c_level3_pct_monthly = reformat_df(df_wc_c_level3_pct_monthly, "m213")

    df_wc_c_level4 = (df_wc_c > -48) & (df_wc_c <= -40)
    df_wc_c_level4_num_monthly = df_wc_c_level4.resample("M").sum()
    df_wc_c_level4_pct_monthly = df_wc_c_level4.resample("M").mean()
    # m204 -> number of level 4 wind chill days in month
    df_wc_c_level4_num_monthly = reformat_df(df_wc_c_level4_num_monthly, "m204")
    # m214 -> percentage of level 4 wind chill days in month
    df_wc_c_level4_pct_monthly = reformat_df(df_wc_c_level4_pct_monthly, "m214")

    df_wc_c_level5 = (df_wc_c > -55) & (df_wc_c <= -48)
    df_wc_c_level5_num_monthly = df_wc_c_level5.resample("M").sum()
    df_wc_c_level5_pct_monthly = df_wc_c_level5.resample("M").mean()
    # m205 -> number of level 5 wind chill days in month
    df_wc_c_level5_num_monthly = reformat_df(df_wc_c_level5_num_monthly, "m205")
    # m215 -> percentage of level 5 wind chill days in month
    df_wc_c_level5_pct_monthly = reformat_df(df_wc_c_level5_pct_monthly, "m215")

    df_wc_c_level6 = df_wc_c <= -55
    df_wc_c_level6_num_monthly = df_wc_c_level6.resample("M").sum()
    df_wc_c_level6_pct_monthly = df_wc_c_level6.resample("M").mean()
    # m206 -> number of level 6 wind chill days in month
    df_wc_c_level6_num_monthly = reformat_df(df_wc_c_level6_num_monthly, "m206")
    # m216 -> percentage of level 6 wind chill days in month
    df_wc_c_level6_pct_monthly = reformat_df(df_wc_c_level6_pct_monthly, "m216")

    df_final_c = pd.concat(
        [
            df_wc_c_level0_num_monthly,
            df_wc_c_level0_pct_monthly,
            df_wc_c_level1_num_monthly,
            df_wc_c_level1_pct_monthly,
            df_wc_c_level2_num_monthly,
            df_wc_c_level2_pct_monthly,
            df_wc_c_level3_num_monthly,
            df_wc_c_level3_pct_monthly,
            df_wc_c_level4_num_monthly,
            df_wc_c_level4_pct_monthly,
            df_wc_c_level5_num_monthly,
            df_wc_c_level5_pct_monthly,
            df_wc_c_level6_num_monthly,
            df_wc_c_level6_pct_monthly,
        ],
        axis=1,
    )

    # wind chill, fahrenheit
    # level 0: above 0F
    df_wc_f_level0 = df_wc_f > 0
    df_wc_f_level0_num_monthly = df_wc_f_level0.resample("M").sum()
    df_wc_f_level0_pct_monthly = df_wc_f_level0.resample("M").mean()
    # m220 -> number of level 0 wind chill days in month
    df_wc_f_level0_num_monthly = reformat_df(df_wc_f_level0_num_monthly, "m220")
    # m230 -> percentage of level 0 wind chill days in month
    df_wc_f_level0_pct_monthly = reformat_df(df_wc_f_level0_pct_monthly, "m230")

    df_wc_f_level1 = (df_wc_f <= 0) & (df_wc_f > -10)
    df_wc_f_level1_num_monthly = df_wc_f_level1.resample("M").sum()
    df_wc_f_level1_pct_monthly = df_wc_f_level1.resample("M").mean()
    # m221 -> number of level 1 wind chill days in month
    df_wc_f_level1_num_monthly = reformat_df(df_wc_f_level1_num_monthly, "m221")
    # m231 -> percentage of level 1 wind chill days in month
    df_wc_f_level1_pct_monthly = reformat_df(df_wc_f_level1_pct_monthly, "m231")

    df_wc_f_level2 = (df_wc_f <= -10) & (df_wc_f > -15)
    df_wc_f_level2_num_monthly = df_wc_f_level2.resample("M").sum()
    df_wc_f_level2_pct_monthly = df_wc_f_level2.resample("M").mean()
    # m222 -> number of level 2 wind chill days in month
    df_wc_f_level2_num_monthly = reformat_df(df_wc_f_level2_num_monthly, "m222")
    # m232 -> percentage of level 2 wind chill days in month
    df_wc_f_level2_pct_monthly = reformat_df(df_wc_f_level2_pct_monthly, "m232")

    df_wc_f_level3 = (df_wc_f <= -15) & (df_wc_f > -25)
    df_wc_f_level3_num_monthly = df_wc_f_level3.resample("M").sum()
    df_wc_f_level3_pct_monthly = df_wc_f_level3.resample("M").mean()
    # m223 -> number of level 3 wind chill days in month
    df_wc_f_level3_num_monthly = reformat_df(df_wc_f_level3_num_monthly, "m223")
    # m233 -> percentage of level 3 wind chill days in month
    df_wc_f_level3_pct_monthly = reformat_df(df_wc_f_level3_pct_monthly, "m233")

    df_wc_f_level4 = (df_wc_f <= -25) & (df_wc_f > -45)
    df_wc_f_level4_num_monthly = df_wc_f_level4.resample("M").sum()
    df_wc_f_level4_pct_monthly = df_wc_f_level4.resample("M").mean()
    # m224 -> number of level 4 wind chill days in month
    df_wc_f_level4_num_monthly = reformat_df(df_wc_f_level4_num_monthly, "m224")
    # m234 -> percentage of level 4 wind chill days in month
    df_wc_f_level4_pct_monthly = reformat_df(df_wc_f_level4_pct_monthly, "m234")

    df_wc_f_level5 = (df_wc_f <= -45) & (df_wc_f > -60)
    df_wc_f_level5_num_monthly = df_wc_f_level5.resample("M").sum()
    df_wc_f_level5_pct_monthly = df_wc_f_level5.resample("M").mean()
    # m225 -> number of level 5 wind chill days in month
    df_wc_f_level5_num_monthly = reformat_df(df_wc_f_level5_num_monthly, "m225")
    # m235 -> percentage of level 5 wind chill days in month
    df_wc_f_level5_pct_monthly = reformat_df(df_wc_f_level5_pct_monthly, "m235")

    df_wc_f_level6 = df_wc_f <= -60
    df_wc_f_level6_num_monthly = df_wc_f_level6.resample("M").sum()
    df_wc_f_level6_pct_monthly = df_wc_f_level6.resample("M").mean()
    # m226 -> number of level 6 wind chill days in month
    df_wc_f_level6_num_monthly = reformat_df(df_wc_f_level6_num_monthly, "m226")
    # m236 -> percentage of level 6 wind chill days in month
    df_wc_f_level6_pct_monthly = reformat_df(df_wc_f_level6_pct_monthly, "m236")

    df_final_f = pd.concat(
        [
            df_wc_f_level0_num_monthly,
            df_wc_f_level0_pct_monthly,
            df_wc_f_level1_num_monthly,
            df_wc_f_level1_pct_monthly,
            df_wc_f_level2_num_monthly,
            df_wc_f_level2_pct_monthly,
            df_wc_f_level3_num_monthly,
            df_wc_f_level3_pct_monthly,
            df_wc_f_level4_num_monthly,
            df_wc_f_level4_pct_monthly,
            df_wc_f_level5_num_monthly,
            df_wc_f_level5_pct_monthly,
            df_wc_f_level6_num_monthly,
            df_wc_f_level6_pct_monthly,
        ],
        axis=1,
    )
    df_final = pd.concat([df_final_c, df_final_f], axis=1)
    df_final.to_stata(os.path.join(save_dir, "wc{}tr.dta".format(year)))
