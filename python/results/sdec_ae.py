if __name__ == "__main__":
    from utilities import *
    from scipy.stats import epps_singleton_2samp, ks_2samp
    df0 = ugr_load_data("june", 1)
    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df0, df1, df2])

    df = ugr_crop_few_minutes(df, 10, 10)

    # Remove 1 day from the end of the data
    dff = ugr_crop_few_minutes(df, 0, 24*60)


    # Each call to ugr_seasonal_decompose() takes about 11 seconds, not that much
    baseData = ugr_seasonal_decompose(dff, paramMeasure="Bitrate")

    updatedData = ugr_seasonal_decompose(df, paramMeasure="Bitrate")

    ugr_seasonal_plot(df, updatedData)

    fifteenMinutes = updatedData.resid[len(baseData.resid):]

    fiveMinutes

    print(len(baseData.resid), len(fifteenMinutes))

    print(epps_singleton_2samp(baseData.resid, fifteenMinutes))
    print(ks_2samp(baseData.resid, fifteenMinutes, alternative="less"))
