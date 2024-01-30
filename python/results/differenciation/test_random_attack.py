if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import random

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])

    df = ugr_crop_few_minutes(df, 10, 10)

    predict = 3 # minutes
    winlen = 15 # minutes
    win = random.randint(0, len(df)//60-winlen)

    dff = ugr_get_few_minutes(df, win, winlen)
    t = [i for i in range(len(dff))]

    x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
    x_t_orig = x_t[:(winlen-predict)*60]

    a,b = x_t_orig.mean(), x_t_orig.std()

    x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])
    m = x_t_new.mean()
    print("NA ", m, m<0.016556434219985622)

    dff["Bitrate"][-(predict-2)*60:] = dff["Bitrate"][-(predict-2)*60:] + 1*10**8
    x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)

    x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])
    m = x_t_new.mean()
    print("A ",m, m>=0.016556434219985622)

    print()

