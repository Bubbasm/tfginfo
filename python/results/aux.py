if __name__ == "__main__":
    from utilities import *
    from differenciation.diff_utils import *
    import pandas as pd
    from scipy.stats import levy_stable

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10, 10)

    x = pd.Series()

    win = 12

    dff = ugr_get_few_minutes(df, win, 15)
    # dff = apply_attack(dff, 2, method="increasing")

    x_t = diff_series(dff, method=1)
    print(x_t.mean(), x_t.std())
    # plot series
    from matplotlib import pyplot as plt
    plt.plot(dff["Date"][:898], x_t)
    plt.show()

    