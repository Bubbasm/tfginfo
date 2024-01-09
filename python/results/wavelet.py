if __name__ == "__main__":
    from utilities import * 
    import pywt
    import pandas as pd

    df1 = ugr_load_data("june", 2)
    # df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1])
    df = ugr_crop_few_minutes(df, 60)

    wavelet = "db1"
    level=7

    param = "Bitrate"

    coeffs = pywt.wavedec(df[param], wavelet, level=level)

    approx = coeffs[0]

    dfNew = pd.DataFrame(zip(df["Date"][::2**level], approx/(2**(level/2))), columns=["Date", param])

    dfDiff = pd.DataFrame(zip(df["Date"][::2**level], approx), columns=["Date", param])

    plt = ugr_simple_plot([df, dfNew], plotColumns=[param], smoothingWindow=60)
    plt.show()
    # hmm no veo que hacer con wavelets... (wavelets solo reducen la dimension de los datos)