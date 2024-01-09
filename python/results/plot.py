if __name__ == "__main__":
    from utilities import *

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10, 10)
    

    ugr_simple_plot(df, plotColumns=["Bitrate"], smoothingWindow=60).show()
