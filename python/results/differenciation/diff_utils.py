import pandas as pd

def diff_series(df, method=0):
    if method == 0:
        x_t = df["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
    elif method == 1:
        x_t = pd.Series([-1/2*df["Bitrate"][i-1] + 1/2*df["Bitrate"][i+1] for i in range(1, len(df)-1)])
    return x_t

def apply_attack(df, attackMin, method=0):
    if method == 0:
        df["Bitrate"][-attackMin*60:] = df["Bitrate"][-attackMin*60:] + (10**8)/2
    elif method == 1:
        df["Bitrate"][-attackMin*60:] = df["Bitrate"][-attackMin*60:] + [(i*10**6)/2 for i in range(attackMin*60)]
    return df