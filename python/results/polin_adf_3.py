if __name__ == "__main__":
    from utilities import *
    import numpy as np
    from statsmodels.tsa.stattools import adfuller, kpss
    import warnings
    from statsmodels.tools.sm_exceptions import InterpolationWarning
    warnings.simplefilter('ignore', InterpolationWarning)
    import matplotlib.pyplot as plt


    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])

    df = ugr_crop_few_minutes(df, 10, 10)

    winlen = 15 # minutes

    # print(len(df)//60)
    # for window in range(0, len(df)//60, winlen):
        # print(window)
    window = 10
    dff = ugr_get_few_minutes(df, window, winlen)

    t = [i for i in range(len(dff))]
    # y_t = dff["Bitrate"][:len(t)]
    # y_adf = adfuller(y_t, regression="c")
    # print(y_adf)
    # y_kpss = kpss(y_t)
    # print(y_kpss)
    # if y_adf[1] < 0.05 and y_kpss[1] > 0.05:
    #     # print("Stationary")
    #     exit

    print(dff)

    # modify 180 points of dff["Bitrate"], adding them a value of ~50000
    dff["Bitrate"][100:280] = dff["Bitrate"][100:280] + [i*500000 for i in range(180)]
    
    # plot dff["Bitrate"]
    plt.plot(t, dff["Bitrate"])
    plt.show()


    x_t = dff["Bitrate"].diff().dropna().reset_index(drop=True, inplace=False)

    # mean and std of x_t
    print(x_t.mean())
    print(x_t.std())
    # show histogram of x_t
    plt.hist(x_t, bins=500)
    plt.show()

