if __name__ == "__main__":
    from utilities import *
    df0 = ugr_load_data("june", 1)
    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([
                           df0, df1, df2,
                        #    df3, df4, df5,
                            # df6, 
                            # df7,
                            # df8, df9, df10,
                        #    df11,
                        #    df12, df13
                            ])

    # Crop 3 days starting from the second day
    df = ugr_get_first_n_days(df, 10)
    df = ugr_get_last_n_days(df, 7)
    print(len(df))

    # El algoritmo no va...
    period = ugr_detect_periodicity_sf(df, 86400, 60)

    print(period)