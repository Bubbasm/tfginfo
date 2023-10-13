if __name__ == "__main__":
    import pandas as pd
    from utilities import *

    # april_week2_csv  april_week4_csv   august_week2_csv  june_week1_csv  june_week3_csv   march_week4_csv  may_week1_csv
    # april_week3_csv  august_week1_csv  july_week1_csv    june_week2_csv  march_week3_csv  march_week5_csv  may_week3_csv
    # based on these files, create a list of dataframes in order of time
    # df0 = ugr_load_data("march", 3)
    # df1 = ugr_load_data("march", 4)
    # df2 = ugr_load_data("march", 5)
    # df3 = ugr_load_data("april", 2)
    # df4 = ugr_load_data("april", 3)
    # df5 = ugr_load_data("april", 4)
    # df6 = ugr_load_data("may", 1)
    df7 = ugr_load_data("may", 3)
    df8 = ugr_load_data("june", 1)
    df9 = ugr_load_data("june", 2)
    df10 = ugr_load_data("june", 3)
    # df11 = ugr_load_data("july", 1)
    # df12 = ugr_load_data("august", 1)
    # df13 = ugr_load_data("august", 2)

    df = ugr_concat_data_list([
                            #    df0, df1, df2,
                            #    df3, df4, df5,
                            #    df6, 
                               df7,
                               df8, df9, df10,
                            #    df11,
                            #    df12, df13
                               ])

    df = crop_few_minutes(df, 5, 2)


    ugr_simple_plot(df, plotColumns=["Bitrate"])