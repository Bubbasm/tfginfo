import pandas as pd

def diff_series(df, method="conv"):
    if method == "conv":
        x_t = pd.Series([-1/2*df["Bitrate"][i-1] + 1/2*df["Bitrate"][i+1] for i in range(1, len(df)-1)])
    elif method == "diff":
        x_t = df["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
    return x_t

def apply_attack(df, attackMin, method="constant"):
    if method == "increasing":
        df["Bitrate"][-attackMin*60:] = df["Bitrate"][-attackMin*60:] + [(i*10**6)/2 for i in range(attackMin*60)]
    elif method == "constant":
        df["Bitrate"][-attackMin*60:] = df["Bitrate"][-attackMin*60:] + (10**8)/4
    return df