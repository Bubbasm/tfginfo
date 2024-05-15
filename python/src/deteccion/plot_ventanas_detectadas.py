def elplot(df, axvspan_cols):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    import numpy as np
    from datetime import datetime
    smoothingWindow=60*15+1
    plt.rcParams['axes.grid'] = True
    weeksArr = [[g for n, g in df.groupby(
        pd.Grouper(key='Date', freq='W')) if len(g) > 0]]
    [week.reset_index(drop=True, inplace=True) for weeks in weeksArr for week in weeks ]
    axCount = len(weeksArr[0])
    fig, axs = plt.subplots(axCount, 1, figsize=(16, 9))
    if axCount == 1:
        axs = [axs]
    plt.subplots_adjust(left=0.1, bottom=0.25)
    for weekIdx in range(len(weeksArr[0])):
        weekArr = [w[weekIdx] for w in weeksArr]
        plotCol = "Bitrate"
        for ax in axs[weekIdx::axCount]:
            week = weekArr[0]
            print(week)
            ax.plot(week["Date"], smooth(week[plotCol],
                    smoothingWindow), label=plotCol, color="black")
            ax.set_ylabel(plotCol)
            ax.set_xlabel("Date" + " (week "+str(week["Date"][0].week)+")")
            ax.xaxis.set_major_formatter(
                mdates.DateFormatter('%Y/%m/%d %A'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            startWeek = datetime.strptime(
                str(week["Date"][0].year) + " " + str(week["Date"][0].week-1) + ' 0', "%Y %W %w")
            endWeek = datetime.strptime(
                str(week["Date"][0].year) + " " + str(week["Date"][0].week) + ' 0', "%Y %W %w")
            ax.set_xbound(pd.to_datetime(startWeek)+pd.Timedelta(days=1),
                            pd.to_datetime(endWeek)+pd.Timedelta(days=1))
            ax.legend()
            ax.ticklabel_format(axis='y', style='sci', scilimits=(8, 4))
        for i, col in enumerate(axvspan_cols):
            # print(week["Date"][(900*i)%len])
            if week is weeksArr[0][0] and i<671:
                ax.axvspan(week["Date"][(900*i)], week["Date"][(900*i)]+pd.Timedelta(minutes=15),
                            color=col, alpha=0.1)
            if week is weeksArr[0][1] and i>671:
                j = i-671
                ax.axvspan(week["Date"][(900*(j))], week["Date"][(900*j)]+pd.Timedelta(minutes=15),
                            color=col, alpha=0.1)
            pass
        print("Barra")
    fig.tight_layout()
    return plt

if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    from statsmodels.discrete.discrete_model import Logit
    from sklearn.model_selection import train_test_split

    file1 = open("../csv/diff_attack.csv", "r")
    file2 = open("../csv/diff_no_attack.csv", "r")
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)
    dff = pd.concat([df1, df2], axis=0)

    file1 = open("../csv/alpha_fit_normalized.csv", "r")
    df = pd.read_csv(file1, sep=",")

    xMeanStd = pd.Series([(float(x_new.mean().iloc[0]), float(x_new.std().iloc[0])) for x_new in [(dff[898*j+720:898*(j+1)] - dff[898*j:898*j+720].mean())/dff[898*j:898*j+720].std() for j in range(len(dff)//898)]])
    df["mean_values"], df["std_values"] = zip(*xMeanStd)

    axvspan_cols = []
    falso_positivo = 0

    attackdf = df[df["attack_value"] == 0.0]
    attackdf = attackdf.reset_index(drop=True)
    for i in range(0, len(attackdf), 15):
        if attackdf["mean_values"][i] < 0.017:
            axvspan_cols.append("blue")
        else:
            axvspan_cols.append("red")
            falso_positivo += 1

    print("Falsos positivos: ", falso_positivo/len(axvspan_cols))

    axvspan_cols = []
    falso_negativo = 0

    attackdf = df[df["attack_value"] == 1.0]
    attackdf = attackdf.reset_index(drop=True)
    for i in range(0, len(attackdf), 15):
        if attackdf["mean_values"][i] > 0.017:
            axvspan_cols.append("blue")
        else:
            axvspan_cols.append("red")
            falso_negativo += 1

    print("Falsos negativo: ", falso_negativo/len(axvspan_cols))

    # dfref = ugr_concat_data_list([ugr_load_data("june", 2), ugr_load_data("june", 3)])
    # dfref = ugr_crop_few_minutes(dfref, 10, 10)
    # plot = elplot(dfref, axvspan_cols=axvspan_cols)
    # plot.show()


