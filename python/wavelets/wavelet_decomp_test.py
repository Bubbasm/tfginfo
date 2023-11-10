if __name__ == "__main__":
    import pywt
    import pandas as pd
    from utilities import *


    df = ugr_load_data("may", 3)
    df = ugr_crop_few_minutes(df, 150, 2)
    param = "Bitrate"

    (A1, D1) = pywt.dwt(df[param], "db1")
    (A2, D2) = pywt.dwt(A1, "db1")
    
    dfNew1 = pd.DataFrame(zip(df["Date"][::2], [a/1.5 for a in A1]), columns=["Date", param])
    dfNew2 = pd.DataFrame(zip(df["Date"][::4], [a/2 for a in A2]), columns=["Date", param])

    dfDiff = pd.DataFrame(zip(df["Date"][::4], [a/2 for a in D2]), columns=["Date", param])

    print(len(df), len(dfNew1), len(dfNew2))

    plt = ugr_simple_plot([df, dfNew1], plotColumns=[param], smoothingWindow=1)
    plt.show()
