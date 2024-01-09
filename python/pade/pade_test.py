if __name__ == '__main__':
    from utilities import *
    import numpy as np
    from scipy.interpolate import pade
    from matplotlib import pyplot as plt

    df0 = ugr_load_data("june", 1)
    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df0, df1, df2])


    df = ugr_get_last_n_days(ugr_get_first_n_days(df, 3), 1)

    df = ugr_crop_few_minutes(df, 12*60, 11*60+30)

    import matplotlib.dates as mpl_dates
    df.reset_index(inplace=True)
    df['Date']=df['Date'].apply(mpl_dates.date2num)
    df = df.astype(float)
    x = [i for i in range(-720,0)]
    y = df["Bitrate"][:len(x)]

    polynomialDegree = 71
    polyn = np.polyfit(x, y, polynomialDegree)

    print(polyn)

    padeMValue = 5
    padeNValue = 2
    p, q = pade(polyn[::-1], padeMValue, padeNValue)

    x = [i for i in range(-720,0)]
    y = df["Bitrate"][:len(x)]

    # Plot p(x)/q(x) for x in df["Date"] and the real values
    y1 = np.polyval(p, x) / np.polyval(q, x)
    y2 = np.polyval(polyn, x)

    plt.plot(x, y)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.legend(["Real values", "Pade", "Polynomial"])
    plt.show()





