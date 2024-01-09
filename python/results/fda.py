if __name__ == "__main__":
    from utilities import *
    import skfda
    import matplotlib.pyplot as plt

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 60)
    dataComplete = ugr_get_first_n_days(df, 8)
    dataComplete = ugr_get_few_minutes(dataComplete, 60*7, 60*24*8)
    dataTrain = ugr_get_first_n_days(dataComplete, 7)