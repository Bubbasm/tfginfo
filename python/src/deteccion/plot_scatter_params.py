if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    
    file1 = open("../csv/diff_attack.csv", "r")
    file2 = open("../csv/diff_no_attack.csv", "r")
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)
    dff = pd.concat([df1, df2], axis=0)

    file1 = open("../csv/alpha_fit_normalized.csv", "r")
    df = pd.read_csv(file1, sep=",")

    xMeanStd = pd.Series([(float(x_new.mean().iloc[0]), float(x_new.std().iloc[0])) for x_new in [(dff[898*j+720:898*(j+1)] - dff[898*j:898*j+720].mean())/dff[898*j:898*j+720].std() for j in range(len(dff)//898)]])
    df["mean_values"], df["std_values"] = zip(*xMeanStd)

    # qt = 0.50
    # qtStr = str(qt)[2:]
    # xPercentile = pd.Series([float(x_new.quantile(qt).iloc[0]) for x_new in [(dff[898*j+720:898*(j+1)])/dff[898*j:898*j+720].quantile(qt) for j in range(len(dff)//898)]])
    # df["q"+qtStr+"_values"] = xPercentile

    color = ["red" if i == 1.0 else "blue" for i in df["attack_value"]]

    parameters = ["alpha", "beta", "gamma", "delta"] # , "mean", "std", "q"+qtStr]
    parameters += ["mean", "std"]

    # 6x6 plot comparing all parameters
    fig, axs = plt.subplots(len(parameters), len(parameters), figsize=(16, 16), constrained_layout=True)
    
    for i in range(len(parameters)):
        for j in range(len(parameters)):
            axs[i, j].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            axs[i, j].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            if i == j:
                bins=500
                if parameters[i] == "delta":
                    # remove outliers percentile 1% and 99%
                    delta1 = df[df["attack_value"] == 1.][parameters[i]+"_values"].clip(lower=df[parameters[i]+"_values"].quantile(0.01), upper=df[parameters[i]+"_values"].quantile(0.99))
                    delta2 = df[df["attack_value"] == 0.][parameters[i]+"_values"].clip(lower=df[parameters[i]+"_values"].quantile(0.01), upper=df[parameters[i]+"_values"].quantile(0.99))
                    axs[i, j].hist(delta1, bins=bins, color="red", alpha=0.5, density=True, rasterized=True)
                    axs[i, j].hist(delta2, bins=bins, color="blue", alpha=0.5, density=True, rasterized=True)
                else:
                    axs[i, j].hist(df[df["attack_value"] == 1.][parameters[i]+"_values"], bins=bins, color="red", alpha=0.5, density=True, rasterized=True)
                    axs[i, j].hist(df[df["attack_value"] == 0.][parameters[i]+"_values"], bins=bins, color="blue", alpha=0.5, density=True, rasterized=True)
                print("Attack: Mean", df[df["attack_value"] == 1.][parameters[i]+"_values"].mean(), "Std", df[df["attack_value"] == 1.][parameters[i]+"_values"].std())
                print("No Attack: Mean", df[df["attack_value"] == 0.][parameters[i]+"_values"].mean(), "Std", df[df["attack_value"] == 0.][parameters[i]+"_values"].std())
                print(len(df[df["attack_value"] == 1.][parameters[i]+"_values"]), len(df[df["attack_value"] == 0.][parameters[i]+"_values"]))
                axs[i, j].set_xlim(df[parameters[i]+"_values"].quantile(0.01), df[parameters[i]+"_values"].quantile(0.99))
                axs[i, j].set_title(parameters[i])
                labels = ["Attack", "No Attack"]
                axs[i, j].legend(labels, fontsize=8)
            elif i>j:
                axs[i, j].axis('off')
            else:
                axs[i, j].scatter(df[parameters[j]+"_values"], df[parameters[i]+"_values"], c=color, alpha=0.05, s=3, rasterized=True)
                # legend
                labels = ["Attack", "No Attack"]
                handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="red", markersize=5),
                           plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="blue", markersize=5)]
                axs[i, j].legend(handles, labels, fontsize=8)
                axs[i, j].set_xlabel(parameters[j])
                axs[i, j].set_ylabel(parameters[i])
                axs[i, j].set_xlim(df[parameters[j]+"_values"].quantile(0.01), df[parameters[j]+"_values"].quantile(0.99))
                axs[i, j].set_ylim(df[parameters[i]+"_values"].quantile(0.01), df[parameters[i]+"_values"].quantile(0.99))
    # x labels and y labels for all plots
    # for i in range(len(parameters)):
    #     axs[len(parameters)-1, i].set_xlabel(parameters[i])
    #     axs[i, 0].set_ylabel(parameters[i])
    plt.tight_layout()
    plt.savefig("scatter_plot.svg", dpi=300)
    # plt.show()
