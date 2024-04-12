if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import statsmodels.api as sm
    import matplotlib.pyplot as plt

    file1 = open("../csv/diff_attack.csv", "r")
    file2 = open("../csv/diff_no_attack.csv", "r")
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)

    file1 = open("../csv/alpha_fit_normalized.csv", "r")
    df = pd.read_csv(file1, sep=",")

    x1 = pd.Series([(float(x_new.mean().iloc[0]), float(x_new.std().iloc[0])) for x_new in [(df1[898*j+720:898*(j+1)] - df1[898*j:898*j+720].mean())/df1[898*j:898*j+720].std() for j in range(len(df1)//898)]])
    x2 = pd.Series([(float(x_new.mean().iloc[0]), float(x_new.std().iloc[0])) for x_new in [(df2[898*j+720:898*(j+1)] - df2[898*j:898*j+720].mean())/df2[898*j:898*j+720].std() for j in range(len(df2)//898)]])
    # alternating x1 and x2
    xMeanStd = pd.concat([x1, x2], axis=0)

    # Add x1 and x2 to df
    df["mean_values"], df["std_values"] = zip(*xMeanStd)

    color = ["red" if i == 1.0 else "blue" for i in df["attack_value"]]

    parameters = ["alpha", "beta", "gamma", "delta", "mean", "std"]

    # plot only delta histogram
    fig, axs = plt.subplots(1, 1, figsize=(10, 10), constrained_layout=True)
    i = 3
    j = 3
    axs.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    axs.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    bins=100000
    axs.hist(df[df["attack_value"] == 1.][parameters[i]+"_values"], bins=bins, color="red", alpha=0.5, density=True)
    axs.hist(df[df["attack_value"] == 0.][parameters[i]+"_values"], bins=bins, color="blue", alpha=0.5, density=True)
    print(parameters[i])
    print("Attack: Mean", df[df["attack_value"] == 1.][parameters[i]+"_values"].mean(), "Std", df[df["attack_value"] == 1.][parameters[i]+"_values"].std())
    print("No Attack: Mean", df[df["attack_value"] == 0.][parameters[i]+"_values"].mean(), "Std", df[df["attack_value"] == 0.][parameters[i]+"_values"].std())
    print(len(df[df["attack_value"] == 1.][parameters[i]+"_values"]), len(df[df["attack_value"] == 0.][parameters[i]+"_values"]))
    # axs.set_xlim(df[parameters[i]+"_values"].quantile(0.001), df[parameters[i]+"_values"].quantile(0.999))
    axs.set_title(parameters[i])
    axs.set_xlabel(parameters[i])
    axs.set_ylabel("Frequency")
    # plt.savefig("scatter_params_compare.png")
    plt.show()
