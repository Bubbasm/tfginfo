if __name__ == "__main__":
    from utilities import *
    from diff_utils import *
    import pandas as pd
    from scipy.stats import levy_stable

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10, 10)

    

    predict = 3 # minutes
    winlen = 15 # minutes

    for win in range(0, len(df)//60-winlen, 1):
        dff = ugr_get_few_minutes(df, win, winlen)
        t = [i for i in range(len(dff))]
        # dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + [i*10**6/2 for i in range((predict-1)*60)]
        dff = apply_attack(dff, predict-1, method="increasing")

        x_t = diff_series(dff, method="conv")
        x_t_orig = x_t[:(winlen-predict)*60]
        x_t_new = x_t[(winlen-predict)*60:]

        # levy-stable fit
        print(len(x_t_new))
        print(levy_stable.fit(x_t_new))
        print(len(x_t_orig))
        print(levy_stable.fit(x_t_orig))
