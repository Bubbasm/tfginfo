if __name__ == "__main__":
    from utilities import *
    from alfa_estable import *

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])
    dff = ugr_get_few_minutes(df, 0, 15)

    from results.differenciation.diff_utils import diff_series

    x_t = diff_series(dff, 1)

    print(len(x_t))

    from scipy.stats import levy_stable

    print(levy_stable.fit(x_t[:10]))
    