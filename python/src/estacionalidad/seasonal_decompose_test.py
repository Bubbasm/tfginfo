if __name__ == "__main__":
    from utilities import *
    df0 = ugr_load_data("june", 1)
    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    # df = ugr_concat_data_list([df0, df1, df2])
    # df = ugr_crop_few_minutes(df, 100)

    # df7 = ugr_load_data("may", 3)
    # df = ugr_crop_few_minutes(df7, 150, 10)

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
    df = ugr_crop_few_minutes(df, 10)
    # df = ugr_get_first_n_days(df, 5)
    df = ugr_get_last_n_days(df, 14)

    res1 = ugr_seasonal_decompose_2(df, paramMeasure="Bitrate")

    # with open("../csv/june_residue_mul.csv", "wb") as f:
    #     data = zip([int(d.timestamp()) for d in df["Date"]], res1.resid)
    #     for d in data:
    #         f.write("{}, {}\n".format(d[0], d[1]).encode())


    # print(len(res1.observed), len(res1.trend), len(res1.seasonal), len(res1.resid))


    ugr_seasonal_plot(df, res1, smoothingWindow=60).show()
