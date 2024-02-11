if __name__ == "__main__":
    from utilities import *
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.stattools import adfuller, kpss
    import warnings
    from statsmodels.tools.sm_exceptions import InterpolationWarning
    warnings.simplefilter('ignore', InterpolationWarning)
    import matplotlib.pyplot as plt
    from scipy.stats import epps_singleton_2samp, ks_2samp, anderson_ksamp
    import scipy.stats as stats

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])

    df = ugr_crop_few_minutes(df, 10, 10)

    predict = 3 # minutes
    winlen = 15 # minutes

    window = 10 # 158 # ejemplo de falso positivo
    dff = ugr_get_few_minutes(df, window, winlen)
    t = [i for i in range(len(dff))]
    # dff["Bitrate"][-(predict)*60:] = dff["Bitrate"][-(predict)*60:] + [(i*10**6)/2 for i in range((predict)*60)]
    dff["Bitrate"][-(predict-2)*60:] = dff["Bitrate"][-(predict-2)*60:] + 1*10**8/2

    plt.plot(dff["Date"], dff["Bitrate"])
    plt.show()

    # x_t as a stencil [-1/2, 0, 1/2] 
    # x_t = pd.Series([-1/2*dff["Bitrate"][i-1] + 1/2*dff["Bitrate"][i+1] for i in range(1, len(dff)-1)])

    # x_t simple differenciation
    x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)

    x_t_orig = x_t[:(winlen-predict)*60]
    a,b = x_t_orig.mean(), x_t_orig.std()

    x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])
    x_t_orig = pd.Series([(x_t_orig[i] - a)/b for i in range(len(x_t_orig))])

    # pasan siempre los tests. Inutil
    # print("Epps: ",epps_singleton_2samp(x_t_orig, x_t_new).pvalue)
    # print("KS:   ",ks_2samp(x_t_orig, x_t_new, alternative="two-sided").pvalue)
    # print("Andr: ",anderson_ksamp([x_t_orig, x_t_new]).significance_level)

    # # mean and std of x_t
    # print("Train:  ",(x_t_orig.mean(), x_t_orig.std()))
    # print("Test:  ",(x_t_new.mean(), x_t_new.std()))

    # # show histogram of x_t
    # plt.hist(x_t_orig, bins=100, density=True, alpha=0.5)
    # plt.hist(x_t_new, bins=100, color="red", density=True, alpha=0.5)
    # plt.show()
