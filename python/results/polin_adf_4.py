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


    file = open("linregr.txt", "w")

    print(len(df)/60)

    avgNoAttackMean = []
    avgNoAttackStd = []
    avgAttackMean = []
    avgAttackStd = []
    for win in range(0, len(df)//60-winlen, 1):
        dff = ugr_get_few_minutes(df, win, winlen)
        t = [i for i in range(len(dff))]
        # dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + [i*10**6/2 for i in range((predict-1)*60)]

        x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
        x_t_orig = x_t[:(winlen-predict)*60]

        a,b = x_t_orig.mean(), x_t_orig.std()

        # normalize x_t_new based on x_t_orig. If there is no attack, x_t_new should be similar to x_t_orig
        x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])
        c,d = x_t_new.mean(), x_t_new.std()
        e,f = x_t.mean(), x_t.std()
        avgNoAttackMean.append(c)
        avgNoAttackStd.append(d)

        file.write(str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " + str(e) + " " + str(f) + " 0" + "\n")

        # dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + [i*10**6/2 for i in range((predict-1)*60)]
        dff["Bitrate"][-(predict-2)*60:] = dff["Bitrate"][-(predict-2)*60:] + 1*10**8
        x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)
        x_t_new = pd.Series([(x_t[i] - a)/b for i in range((winlen-predict)*60, len(x_t))])

        c,d = x_t_new.mean(), x_t_new.std()
        e,f = x_t.mean(), x_t.std()
        avgAttackMean.append(c)
        avgAttackStd.append(d)


        file.write(str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " + str(e) + " " + str(f) + " 1" + "\n")
    print(sum(avgNoAttackMean)/len(avgNoAttackMean), sum(avgNoAttackStd)/len(avgNoAttackStd))
    print(sum(avgAttackMean)/len(avgAttackMean), sum(avgAttackStd)/len(avgAttackStd))
    exit()
    
    window = 35
    dff = ugr_get_few_minutes(df, window, winlen)
    t = [i for i in range(len(dff))]
    # dff["Bitrate"][-(predict-1)*60:] = dff["Bitrate"][-(predict-1)*60:] + [i*10**6/2 for i in range((predict-1)*60)]
    # dff["Bitrate"][-(predict-2)*60:] = dff["Bitrate"][-(predict-2)*60:] + 1*10**7

    plt.plot(t, dff["Bitrate"])
    plt.show()

    # x_t as a stencil [-1/2, 0, 1/2] 
    x_t = pd.Series([-1/2*dff["Bitrate"][i-1] + 1/2*dff["Bitrate"][i+1] for i in range(1, len(dff)-1)])

    # x_t simple differenciation
    # x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)

    x_t_orig = x_t[:(winlen-predict)*60]
    x_t_new = x_t[(winlen-predict)*60:]

    print("Epps: ",epps_singleton_2samp(x_t_orig, x_t_new).pvalue)
    print("KS:   ",ks_2samp(x_t_orig, x_t_new, alternative="two-sided").pvalue)
    print("Andr: ",anderson_ksamp([x_t_orig, x_t_new]).significance_level)

    # mean and std of x_t
    print("Train: ",(x_t_orig.mean(), x_t_orig.std()))
    print("Test:  ",(x_t_new.mean(), x_t_new.std()))
    print("Full:  ",(x_t.mean(), x_t.std()))

    # show histogram of x_t
    plt.hist(x_t_orig, bins=500, density=True, alpha=0.5)
    plt.hist(x_t_new, bins=100, color="red", density=True, alpha=0.5)
    plt.show()



    # TODO alfa estable fit de x_t y comparar sin ataque

