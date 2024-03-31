if __name__ == "__main__":
    from utilities import *
    from differenciation.diff_utils import *
    import pandas as pd

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10, 10)

    predict = 3 # minutes
    winlen = 15 # minutes

    file = open("diff_attack.csv", "w")

    for win in range(0, len(df)//60-winlen, 1):
        dff = ugr_get_few_minutes(df, win, winlen)
        t = [i for i in range(len(dff))]
        
        dff = apply_attack(dff, 2, 1)
        x_t = diff_series(dff, 1)
        file.write(x_t.to_csv(header=False, index=False))