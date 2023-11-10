def residue_load_data(basename: str):
    import pandas as pd
    columns = ["Date", "Residue"]
    try:
        df = pd.read_csv(basename+".csv", sep=',', names=columns)
    except FileNotFoundError:
        print("File not found")
        return
    df["Date"] = pd.to_datetime(df["Date"], unit='s')

    return df

def residue_get_first_n_days(df, n):
    from utilities import ugr_get_first_n_days
    return ugr_get_first_n_days(df, n)


def residue_get_last_n_days(df, n):
    from utilities import ugr_get_last_n_days
    return ugr_get_last_n_days(df, n)


def residue_crop_few_minutes(df, minutesLeft, minutesRight=None):
    from utilities import ugr_crop_few_minutes
    return ugr_crop_few_minutes(df, minutesLeft, minutesRight)

def residue_levy_fit(df):
    import numpy as np
    from scipy.stats import levy_stable
    return levy_stable.fit(df["Residue"])
