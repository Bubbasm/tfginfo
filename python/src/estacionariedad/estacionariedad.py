if __name__ == "__main__":
    from statsmodels.tsa.stattools import adfuller, kpss
    from utilities import *
    import warnings
    from statistics import mean
    from statsmodels.tools.sm_exceptions import InterpolationWarning
    warnings.simplefilter('ignore', InterpolationWarning)

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 60)

    pvaluesadf = []
    pvalueskpss = []
    for i in range(0, 60, 15):
        dff = ugr_get_few_minutes(df, i, 15)
        pvaluesadf.append(adfuller(dff["Bitrate"])[1])
        pvalueskpss.append(kpss(dff["Bitrate"])[1])
    meanadf = mean(pvaluesadf)
    meankpss = mean(pvalueskpss)
    print("ADF:")
    print(meanadf)
    print(len([1 for i in pvaluesadf if i>0.05])/len(pvaluesadf))
    print("KPSS:")
    print(meankpss)
    print(len([1 for i in pvalueskpss if i<0.05])/len(pvalueskpss))
    print("Combined:")
    print(len([1 for i in range(len(pvalueskpss)) if pvalueskpss[i]<0.05 or pvaluesadf[i]>0.05])/len(pvalueskpss))