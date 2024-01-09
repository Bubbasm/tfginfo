if __name__ == "__main__":
    from statsmodels.tsa.stattools import adfuller
    from utilities import *

    df0 = ugr_load_data("june", 1)
    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df0, df1, df2])

    # Keep 1 day only
    df = ugr_get_last_n_days(ugr_get_first_n_days(df, 3), 1)

    # Keep 15 minutes only
    dff = ugr_crop_few_minutes(df, 12*60+15, 11*60+30)

    # Output meaning
    # (adf, pvalue, usedlag, nobs, critical values, icbest)
    pvalues = []
    for i in range(0, 24*60, 15):
        dff = ugr_crop_few_minutes(df, i, 24*60-15-i)
        pvalues.append((adfuller(dff["Bitrate"])[1], i))
    pvalues.sort(reverse=True)
    print(pvalues)
    print(len([1 for i in pvalues if i[0]>0.05]), len([1 for i in pvalues if i[0]<0.05]), len(pvalues))
    # 11.46% de los casos no podemos afirmar que los datos sean estacionarios, con alpha=0.05

    # Para 1 dia:
    # (-9.388440876963791, 6.660831103960549e-16, 64, 86335, {'1%': -3.4304257455775677, '5%': -2.86157347830019, '10%': -2.566787819337882}, 3145900.334027101)
    # p-valor muy pequeño => rechazamos la hipótesis nula => la serie es estacionaria

    # Para 3 dias:
    # (-13.257627042838898, 8.52433606550738e-25, 77, 259122, {'1%': -3.430375236625147, '5%': -2.8615511542684158, '10%': -2.566775937013609}, 9381727.712127574)
    # p-valor muy pequeño => rechazamos la hipótesis nula => la serie es estacionaria