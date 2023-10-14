if __name__ == "__main__":
    from utilities import *
    # df0 = ugr_load_data("june", 1)
    # df1 = ugr_load_data("june", 2)
    # df2 = ugr_load_data("june", 3)

    # df = ugr_concat_data_list([df0, df1, df2])
    # df = ugr_crop_few_minutes(df, 100)

    df7 = ugr_load_data("may", 3)
    df = ugr_crop_few_minutes(df7, 150, 10)


    # Crop 3 days starting from the second day
    # df = ugr_get_first_n_days(df, 5)
    # df = ugr_get_last_n_days(df, 2)

    # ugr_seasonal_decompose_2 takes too long (never ended)
    res1 = ugr_seasonal_decompose_1(df, paramMeasure="Bitrate")

    ugr_seasonal_plot(df, res1)    