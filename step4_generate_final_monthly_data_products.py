import os
import pandas as pd
from tqdm import tqdm

daily_measure_csv_dir = "/data/Heat/data/processed/daily_measures"
save_dir = "/data/Heat/data/processed/monthly_measures"

def reformat_df(df, column_header: str):
    df.index = df.index.to_period('M')
    df = df.T
    df.index.name = "LINKCEN2010"
    # m300 -> number of precipitation days in a month
    column_names = ["{}tr{}{:02d}".format(column_header, c.year, c.month) for c in df.columns]
    df.columns = column_names
    return df

# daily min and max temperature averaged
print("Processing daily min and max temperature...")
tmmx_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("tmmx.csv")]
for i in range(len(tmmx_csvs)):
    df_tmmx = pd.read_csv(os.path.join(daily_measure_csv_dir, tmmx_csvs[i]), index_col=0, parse_dates=[0])
    df_tmmn = pd.read_csv(os.path.join(daily_measure_csv_dir, tmmx_csvs[i].replace("tmmx", "tmmn")), index_col=0, parse_dates=[0])
    year = os.path.basename(tmmx_csvs[i]).split("_")[0]

    df_monthly = df_tmmn.resample('M').mean()
    # m400 -> average daily minimum temperature
    df_monthly = reformat_df(df_monthly, "m400")

    df_monthly_max = df_tmmx.resample('M').mean()
    # m401 -> average daily maximum temperature
    df_monthly_max = reformat_df(df_monthly_max, "m401")
    df_final = pd.concat([df_monthly, df_monthly_max], axis=1)
    df_final.to_stata(os.path.join(save_dir, "tmm{}tr.dta".format(year)))

# precipitation
print("Processing precipitation...")
pr_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("pr.csv")]
for i in tqdm(range(len(pr_csvs))):
    year = os.path.basename(pr_csvs[i]).split("_")[0]
    df_pr = pd.read_csv(os.path.join(daily_measure_csv_dir, pr_csvs[i]), index_col=0, parse_dates=[0])
    df_pr_bool = df_pr>0
    df_num_pr_monthly = df_pr_bool.resample('M').sum()
    # m300 -> number of precipitation days in a month
    df_num_pr_monthly = reformat_df(df_num_pr_monthly, "m300")

    df_pct_pr_monthly = df_pr_bool.resample('M').mean()
    # m301 -> percentage of precipitation days in a month
    df_pct_pr_monthly = reformat_df(df_pct_pr_monthly, "m301")

    df_total_pr_monthly = df_pr.resample('M').sum()
    # m302 -> total precipitation in a month
    df_total_pr_monthly = reformat_df(df_total_pr_monthly, "m302")

    df_avg_pr_monthly = df_pr.resample('M').mean()
    # m303 -> average precipitation in a month 
    df_avg_pr_monthly = reformat_df(df_avg_pr_monthly, "m303")

    df_avg_pr_only_pr_days_monthly = df_pr[df_pr>0].resample('M').mean()
    df_avg_pr_only_pr_days_monthly[df_avg_pr_only_pr_days_monthly.isna()] = 0
    # m304 -> average precipitation in a month for only precipitation days
    df_avg_pr_only_pr_days_monthly = reformat_df(df_avg_pr_only_pr_days_monthly, "m304")

    # concatenate all precipitation dataframes
    df_final = pd.concat([df_num_pr_monthly, df_pct_pr_monthly, df_total_pr_monthly, df_avg_pr_monthly, df_avg_pr_only_pr_days_monthly], axis=1)
    df_final.to_stata(os.path.join(save_dir, "pr{}tr.dta".format(year)))

# heat index
print("Processing heat index...")
hi_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("heat_index.csv")]
for i in tqdm(range(len(hi_csvs))):
    year = os.path.basename(hi_csvs[i]).split("_")[0]
    df_hi = pd.read_csv(os.path.join(daily_measure_csv_dir, hi_csvs[0]), index_col=0, parse_dates=[0])

    # level 0: below 80F
    df_hi_level0 = df_hi<80
    df_hi_level0_num_monthly = df_hi_level0.resample('M').sum()
    df_hi_level0_pct_monthly = df_hi_level0.resample('M').mean()
    # m100 -> number of level 0 heat days in month
    df_hi_level0_num_monthly = reformat_df(df_hi_level0_num_monthly, "m100")
    # m110 -> percentage of level 0 heat days in month
    df_hi_level0_pct_monthly = reformat_df(df_hi_level0_pct_monthly, "m110")

    # level 1: 80-90F
    df_hi_level1 = (df_hi>=80) & (df_hi<90)
    df_hi_level1_num_monthly = df_hi_level1.resample('M').sum()
    df_hi_level1_pct_monthly = df_hi_level1.resample('M').mean()
    # m101 -> number of level 1 heat days in month
    df_hi_level1_num_monthly = reformat_df(df_hi_level1_num_monthly, "m101")
    # m111 -> percentage of level 1 heat days in month
    df_hi_level1_pct_monthly = reformat_df(df_hi_level1_pct_monthly, "m111")

    # level 2: 90-103F
    df_hi_level2 = (df_hi>=90) & (df_hi<103)
    df_hi_level2_num_monthly = df_hi_level2.resample('M').sum()
    df_hi_level2_pct_monthly = df_hi_level2.resample('M').mean()
    # m102 -> number of level 2 heat days in month
    df_hi_level2_num_monthly = reformat_df(df_hi_level2_num_monthly, "m102")
    # m112 -> percentage of level 2 heat days in month
    df_hi_level2_pct_monthly = reformat_df(df_hi_level2_pct_monthly, "m112")

    # level 3: 103-125F
    df_hi_level3 = (df_hi>=103) & (df_hi<125)
    df_hi_level3_num_monthly = df_hi_level3.resample('M').sum()
    df_hi_level3_pct_monthly = df_hi_level3.resample('M').mean()
    # m103 -> number of level 3 heat days in month
    df_hi_level3_num_monthly = reformat_df(df_hi_level3_num_monthly, "m103")
    # m113 -> percentage of level 3 heat days in month
    df_hi_level3_pct_monthly = reformat_df(df_hi_level3_pct_monthly, "m113")

    # level 4: above 125F
    df_hi_level4 = df_hi>=125
    df_hi_level4_num_monthly = df_hi_level4.resample('M').sum()
    df_hi_level4_pct_monthly = df_hi_level4.resample('M').mean()
    # m104 -> number of level 4 heat days in month
    df_hi_level4_num_monthly = reformat_df(df_hi_level4_num_monthly, "m104")
    # m114 -> percentage of level 4 heat days in month
    df_hi_level4_pct_monthly = reformat_df(df_hi_level4_pct_monthly, "m114")

    df_final = pd.concat([
        df_hi_level0_num_monthly, df_hi_level0_pct_monthly,
        df_hi_level1_num_monthly, df_hi_level1_pct_monthly,
        df_hi_level2_num_monthly, df_hi_level2_pct_monthly,
        df_hi_level3_num_monthly, df_hi_level3_pct_monthly,
        df_hi_level4_num_monthly, df_hi_level4_pct_monthly
    ], axis=1)
    df_final.to_stata(os.path.join(save_dir, "hi{}tr.dta".format(year)))

# wind chill
print("Processing wind chill, celsius / fahrenheit...")
wc_c_csvs = [os.path.join(daily_measure_csv_dir, f) for f in os.listdir(daily_measure_csv_dir) if f.endswith("wc_celsius.csv")]
for i in tqdm(range(len(wc_c_csvs))):
    
    df_wc_c = pd.read_csv(os.path.join(daily_measure_csv_dir, wc_c_csvs[i]), index_col=0, parse_dates=[0])
    df_wc_f = pd.read_csv(os.path.join(daily_measure_csv_dir, wc_c_csvs[i].replace("celsius", "fahrenheit")), index_col=0, parse_dates=[0])

    df_wc_c_level0 = df_wc_c>0
    df_wc_c_level0_num_monthly = df_wc_c_level0.resample('M').sum()
    df_wc_c_level0_pct_monthly = df_wc_c_level0.resample('M').mean()
    # m200 -> number of level 0 wind chill days in month
    df_wc_c_level0_num_monthly = reformat_df(df_wc_c_level0_num_monthly, "m200")
    # m210 -> percentage of level 0 wind chill days in month
    df_wc_c_level0_pct_monthly = reformat_df(df_wc_c_level0_pct_monthly, "m210")

    df_wc_c_level1 = (df_wc_c>-10) & (df_wc_c<=0)
    df_wc_c_level1_num_monthly = df_wc_c_level1.resample('M').sum()
    df_wc_c_level1_pct_monthly = df_wc_c_level1.resample('M').mean()
    # m201 -> number of level 1 wind chill days in month
    df_wc_c_level1_num_monthly = reformat_df(df_wc_c_level1_num_monthly, "m201")
    # m211 -> percentage of level 1 wind chill days in month
    df_wc_c_level1_pct_monthly = reformat_df(df_wc_c_level1_pct_monthly, "m211")

    df_wc_c_level2 = (df_wc_c>-28) & (df_wc_c<=-10)
    df_wc_c_level2_num_monthly = df_wc_c_level2.resample('M').sum()
    df_wc_c_level2_pct_monthly = df_wc_c_level2.resample('M').mean()
    # m202 -> number of level 2 wind chill days in month
    df_wc_c_level2_num_monthly = reformat_df(df_wc_c_level2_num_monthly, "m202")
    # m212 -> percentage of level 2 wind chill days in month
    df_wc_c_level2_pct_monthly = reformat_df(df_wc_c_level2_pct_monthly, "m212")

    df_wc_c_level3 = (df_wc_c>-40) & (df_wc_c<=-28)
    df_wc_c_level3_num_monthly = df_wc_c_level3.resample('M').sum()
    df_wc_c_level3_pct_monthly = df_wc_c_level3.resample('M').mean()
    # m203 -> number of level 3 wind chill days in month
    df_wc_c_level3_num_monthly = reformat_df(df_wc_c_level3_num_monthly, "m203")
    # m213 -> percentage of level 3 wind chill days in month
    df_wc_c_level3_pct_monthly = reformat_df(df_wc_c_level3_pct_monthly, "m213")

    df_wc_c_level4 = (df_wc_c>-48) & (df_wc_c<=-40)
    df_wc_c_level4_num_monthly = df_wc_c_level4.resample('M').sum()
    df_wc_c_level4_pct_monthly = df_wc_c_level4.resample('M').mean()
    # m204 -> number of level 4 wind chill days in month
    df_wc_c_level4_num_monthly = reformat_df(df_wc_c_level4_num_monthly, "m204")
    # m214 -> percentage of level 4 wind chill days in month
    df_wc_c_level4_pct_monthly = reformat_df(df_wc_c_level4_pct_monthly, "m214")

    df_wc_c_level5 = (df_wc_c>-55) & (df_wc_c<=-48)
    df_wc_c_level5_num_monthly = df_wc_c_level5.resample('M').sum()
    df_wc_c_level5_pct_monthly = df_wc_c_level5.resample('M').mean()
    # m205 -> number of level 5 wind chill days in month
    df_wc_c_level5_num_monthly = reformat_df(df_wc_c_level5_num_monthly, "m205")
    # m215 -> percentage of level 5 wind chill days in month
    df_wc_c_level5_pct_monthly = reformat_df(df_wc_c_level5_pct_monthly, "m215")

    df_wc_c_level6 = (df_wc_c<=-55)
    df_wc_c_level6_num_monthly = df_wc_c_level6.resample('M').sum()
    df_wc_c_level6_pct_monthly = df_wc_c_level6.resample('M').mean()
    # m206 -> number of level 6 wind chill days in month
    df_wc_c_level6_num_monthly = reformat_df(df_wc_c_level6_num_monthly, "m206")
    # m216 -> percentage of level 6 wind chill days in month
    df_wc_c_level6_pct_monthly = reformat_df(df_wc_c_level6_pct_monthly, "m216")

    df_final_c = pd.concat([
        df_wc_c_level0_num_monthly, df_wc_c_level0_pct_monthly,
        df_wc_c_level1_num_monthly, df_wc_c_level1_pct_monthly,
        df_wc_c_level2_num_monthly, df_wc_c_level2_pct_monthly,
        df_wc_c_level3_num_monthly, df_wc_c_level3_pct_monthly,
        df_wc_c_level4_num_monthly, df_wc_c_level4_pct_monthly,
        df_wc_c_level5_num_monthly, df_wc_c_level5_pct_monthly,
        df_wc_c_level6_num_monthly, df_wc_c_level6_pct_monthly
    ], axis=1)

    # wind chill, fahrenheit
    # level 0: above 0F
    df_wc_f_level0 = df_wc_f>0
    df_wc_f_level0_num_monthly = df_wc_f_level0.resample('M').sum()
    df_wc_f_level0_pct_monthly = df_wc_f_level0.resample('M').mean()
    # m220 -> number of level 0 wind chill days in month
    df_wc_f_level0_num_monthly = reformat_df(df_wc_f_level0_num_monthly, "m220")
    # m230 -> percentage of level 0 wind chill days in month
    df_wc_f_level0_pct_monthly = reformat_df(df_wc_f_level0_pct_monthly, "m230")

    df_wc_f_level1 = (df_wc_f<=0) & (df_wc_f> -10)
    df_wc_f_level1_num_monthly = df_wc_f_level1.resample('M').sum()
    df_wc_f_level1_pct_monthly = df_wc_f_level1.resample('M').mean()
    # m221 -> number of level 1 wind chill days in month
    df_wc_f_level1_num_monthly = reformat_df(df_wc_f_level1_num_monthly, "m221")
    # m231 -> percentage of level 1 wind chill days in month
    df_wc_f_level1_pct_monthly = reformat_df(df_wc_f_level1_pct_monthly, "m231")

    df_wc_f_level2 = (df_wc_f<=-10) & (df_wc_f> -15)
    df_wc_f_level2_num_monthly = df_wc_f_level2.resample('M').sum()
    df_wc_f_level2_pct_monthly = df_wc_f_level2.resample('M').mean()
    # m222 -> number of level 2 wind chill days in month
    df_wc_f_level2_num_monthly = reformat_df(df_wc_f_level2_num_monthly, "m222")
    # m232 -> percentage of level 2 wind chill days in month
    df_wc_f_level2_pct_monthly = reformat_df(df_wc_f_level2_pct_monthly, "m232")

    df_wc_f_level3 = (df_wc_f<=-15) & (df_wc_f> -25)
    df_wc_f_level3_num_monthly = df_wc_f_level3.resample('M').sum()
    df_wc_f_level3_pct_monthly = df_wc_f_level3.resample('M').mean()
    # m223 -> number of level 3 wind chill days in month
    df_wc_f_level3_num_monthly = reformat_df(df_wc_f_level3_num_monthly, "m223")
    # m233 -> percentage of level 3 wind chill days in month
    df_wc_f_level3_pct_monthly = reformat_df(df_wc_f_level3_pct_monthly, "m233")

    df_wc_f_level4 = (df_wc_f<=-25) & (df_wc_f> -45)
    df_wc_f_level4_num_monthly = df_wc_f_level4.resample('M').sum()
    df_wc_f_level4_pct_monthly = df_wc_f_level4.resample('M').mean()
    # m224 -> number of level 4 wind chill days in month
    df_wc_f_level4_num_monthly = reformat_df(df_wc_f_level4_num_monthly, "m224")
    # m234 -> percentage of level 4 wind chill days in month
    df_wc_f_level4_pct_monthly = reformat_df(df_wc_f_level4_pct_monthly, "m234")

    df_wc_f_level5 = (df_wc_f<=-45) & (df_wc_f> -60)
    df_wc_f_level5_num_monthly = df_wc_f_level5.resample('M').sum()
    df_wc_f_level5_pct_monthly = df_wc_f_level5.resample('M').mean()
    # m225 -> number of level 5 wind chill days in month
    df_wc_f_level5_num_monthly = reformat_df(df_wc_f_level5_num_monthly, "m225")
    # m235 -> percentage of level 5 wind chill days in month
    df_wc_f_level5_pct_monthly = reformat_df(df_wc_f_level5_pct_monthly, "m235")

    df_wc_f_level6 = (df_wc_f<=-60)
    df_wc_f_level6_num_monthly = df_wc_f_level6.resample('M').sum()
    df_wc_f_level6_pct_monthly = df_wc_f_level6.resample('M').mean()
    # m226 -> number of level 6 wind chill days in month
    df_wc_f_level6_num_monthly = reformat_df(df_wc_f_level6_num_monthly, "m226")
    # m236 -> percentage of level 6 wind chill days in month
    df_wc_f_level6_pct_monthly = reformat_df(df_wc_f_level6_pct_monthly, "m236")

    df_final_f = pd.concat([
        df_wc_f_level0_num_monthly, df_wc_f_level0_pct_monthly,
        df_wc_f_level1_num_monthly, df_wc_f_level1_pct_monthly,
        df_wc_f_level2_num_monthly, df_wc_f_level2_pct_monthly,
        df_wc_f_level3_num_monthly, df_wc_f_level3_pct_monthly,
        df_wc_f_level4_num_monthly, df_wc_f_level4_pct_monthly,
        df_wc_f_level5_num_monthly, df_wc_f_level5_pct_monthly,
        df_wc_f_level6_num_monthly, df_wc_f_level6_pct_monthly
    ], axis=1)
    df_final = pd.concat([df_final_c, df_final_f], axis=1)
    df_final.to_stata(os.path.join(save_dir, "wc{}tr.dta".format(year)))

