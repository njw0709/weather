def reformat_df(df, column_header: str):
    df.index = df.index.to_period("M")
    df = df.T
    df.index.name = "LINKCEN2010"
    # m300 -> number of precipitation days in a month
    column_names = [
        "{}tr{}{:02d}".format(column_header, c.year, c.month) for c in df.columns
    ]
    df.columns = column_names
    return df
