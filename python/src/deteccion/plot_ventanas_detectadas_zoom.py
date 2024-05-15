def elplot(df, axvspan_cols):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    import numpy as np
    from datetime import datetime
    smoothingWindow=61
    plt.rcParams['axes.grid'] = True

    fig, ax = plt.subplots(figure=(16, 9))
    ax.plot(df["Date"], smooth(df["Bitrate"], smoothingWindow), label="Bitrate", color="black")
    ax.set_ylabel("Bitrate")
    ax.set_xlabel("Time")
    ax.set_title(df["Date"][0].strftime("%Y-%m-%d"))

    myFmt = mdates.DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(myFmt)
    ax.ticklabel_format(axis='y', style='sci', scilimits=(8, 4))
    for i, col in enumerate(axvspan_cols):
        ax.axvspan(df["Date"][900*i], df["Date"][900*i]+pd.Timedelta(minutes=15), color=col, alpha=0.1)
    
    ax.legend()

    fig.autofmt_xdate()
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

    axvspan_cols_na = []
    falso_positivo = 0

    attackdf = df[df["attack_value"] == 0.0]
    attackdf = attackdf.reset_index(drop=True)
    for i in range(0, len(attackdf), 15):
        if attackdf["mean_values"][i] < 0.017:
            axvspan_cols_na.append("blue")
        else:
            axvspan_cols_na.append("red")
            falso_positivo += 1

    print("Falsos positivos: ", falso_positivo/len(axvspan_cols_na))

    axvspan_cols_a = []
    falso_negativo = 0

    attackdf = df[df["attack_value"] == 1.0]
    attackdf = attackdf.reset_index(drop=True)
    for i in range(0, len(attackdf), 15):
        if attackdf["mean_values"][i] > 0.017:
            axvspan_cols_a.append("green")
        else:
            axvspan_cols_a.append("red")
            falso_negativo += 1

    print("Falsos negativo: ", falso_negativo/len(axvspan_cols_a))

    dfref = ugr_concat_data_list([ugr_load_data("june", 2), ugr_load_data("june", 3)])
    dfref = ugr_crop_few_minutes(dfref, 10, 10)
    dfref = ugr_get_first_n_days(dfref, 1)
    axvspan_cols = axvspan_cols_na[0:96]
    plot = elplot(dfref, axvspan_cols)
    plot.savefig("catalogacion_defensa_zoom.svg")

    axvspan_cols = axvspan_cols_a[0:96]
    plot = elplot(dfref, axvspan_cols)
    plot.savefig("catalogacion_ataque_zoom.svg")
