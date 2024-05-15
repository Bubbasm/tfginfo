def elplot(df, axvspan_cols, t_ini=0, t_fin=0):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    import numpy as np
    from datetime import datetime
    smoothingWindow=61
    plt.rcParams['axes.grid'] = True
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.plot(df["Date"][t_ini*900//15:t_fin*900//15], smooth(df["Bitrate"], smoothingWindow)[t_ini*900//15:t_fin*900//15], label="Bitrate", color="black")
    ax.set_ylabel("Bitrate")
    ax.set_xlabel("Time")
    ax.set_title(df["Date"][t_ini*900//15].strftime("%Y-%m-%d %H:%M") + " to " + df["Date"][t_fin*900//15].strftime("%Y-%m-%d %H:%M"))
    myFmt = mdates.DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(myFmt)
    ax.ticklabel_format(axis='y', style='sci', scilimits=(8, 4))
    for i, col in enumerate(axvspan_cols):
        ax.axvspan(df["Date"][60*i+t_ini*900//15], df["Date"][60*i+t_ini*900//15]+pd.Timedelta(minutes=1), color=col, alpha=0.05)
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
    df = df.dropna()

    parameters = ["alpha_values", "beta_values", "gamma_values", "delta_values", "mean_values", "std_values"]

    full_Y = df["attack_value"].astype(float)
    full_X = df[parameters].astype(float)
    full_X = sm.add_constant(full_X)
    att_X = full_X[full_Y == 1].reset_index(drop=True)
    att_Y = full_Y[full_Y == 1].reset_index(drop=True)
    no_att_X = full_X[full_Y == 0].reset_index(drop=True)
    no_att_Y = full_Y[full_Y == 0].reset_index(drop=True)

    from src.deteccion.cross_validation import train_test_split_2


    dfref = ugr_concat_data_list([ugr_load_data("june", 2), ugr_load_data("june", 3)])
    dfref = ugr_crop_few_minutes(dfref, 10, 10)

# take 80% of the data for training and 20% for testing
ran = 3/14-0.044716
Xatt,tXatt,Yatt,tYatt,ran = train_test_split_2(att_X, att_Y, ran)
Xnoatt,tXnoatt,Ynoatt,tYnoatt,ran = train_test_split_2(no_att_X, no_att_Y,ran)
Y = pd.concat([Yatt, Ynoatt])
X = pd.concat([Xatt, Xnoatt])
tY = pd.concat([tYatt, tYnoatt])
tX = pd.concat([tXatt, tXnoatt])
model = Logit(Y,X)
results = model.fit()
print(results.summary())
# calculate the accuracy of the model with test data
predsAtt = results.predict(tXatt)
predsAttNominal = [1 if x > 0.5 else 0 for x in predsAtt]
predsNoAtt = results.predict(tXnoatt)
predsNoAttNominal = [1 if x > 0.5 else 0 for x in predsNoAtt]

axvspan_cols = []
falso_positivo = 0

for i in range(len(predsAttNominal)):
    if predsAttNominal[i] == tYatt.iloc[i]:
        axvspan_cols.append("green")
    else:
        axvspan_cols.append("red")
        falso_positivo += 1

print("Falsos positivo: ", falso_positivo/len(axvspan_cols))

plot = elplot(dfref, axvspan_cols, 4312, 6538)
plot.savefig("catalogacion_ataque.svg")
# plot.show()

axvspan_cols = []
falso_negativo = 0

for i in range(len(predsNoAttNominal)):
    if predsNoAttNominal[i] == tYnoatt.iloc[i]:
        axvspan_cols.append("blue")
    else:
        axvspan_cols.append("red")
        falso_negativo += 1

print("Falsos negativo: ", falso_negativo/len(axvspan_cols))

plot = elplot(dfref, axvspan_cols,4312, 6538)
plot.savefig("catalogacion_defensa.svg")
# plot.show()



