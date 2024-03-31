if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    
    file1 = open("../csv/alpha_fit_normalized.csv", "r")
    # file2 = open("../csv/alpha_beta_values_no_attack.csv", "r")

    df1 = pd.read_csv(file1, sep=",")
    # df2 = pd.read_csv(file2, sep=",")
    # df = pd.concat([df1, df2], axis=0)
    df = df1


    Y = df["attack_value"].astype(float)
    color = ["red" if i == 1.0 else "blue" for i in Y]
    legend = ["Attack" if i == 1.0 else "No Attack" for i in Y]
    X = df[["alpha_values", "beta_values"]].astype(float)

    plt.figure(figsize=(10,6))
    plt.scatter(X["alpha_values"], X["beta_values"], c=color, alpha=0.05)
    plt.xlabel("Alpha Values")
    plt.ylabel("Beta Values")
    # plt.savefig("scatter_alpha_beta_diff.svg")
    plt.show()