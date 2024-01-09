if __name__ == "__main__":
    from utilities import *
    import matplotlib.pyplot as plt
    import numpy as np 

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 60)
    dataComplete = ugr_get_first_n_days(df, 8)
    dataComplete = ugr_get_few_minutes(dataComplete, 60*7, 60*24*8)
    dataTrain = ugr_get_first_n_days(dataComplete, 7)

    daydiff = df.diff(periods=86400)
    daydiff = daydiff.dropna()

    param = "Bitrate"

    avgday = sum([np.array(dataTrain[param][i:i+86400]) for i in range(0, len(dataTrain), 86400)])
    avgday = np.divide(avgday, len(dataTrain)/86400)

    print(len(avgday),avgday)

    plt.plot(smooth(avgday, 60))
    plt.show()