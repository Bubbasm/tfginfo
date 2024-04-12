if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    
    file = open("../csv/linregr2.txt", "r")
    columns=["a", "b", "c", "d", "e", "f", "attack"]

    df = pd.read_csv(file, sep=" ", names=columns)

    # I want to perform linear regression with variables a, b, c, d, e, f with OLS
    Y = df["attack"].astype(float)
    color = ["red" if i == 1.0 else "blue" for i in Y]
    legend = ["Attack" if i == 1.0 else "No Attack" for i in Y]
    X = df[["c", "d"]].astype(float)

    # plot dots of (c,d) as a scatter plot with two colors: red for attack and blue for no attack
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X["c"], X["d"], Y, c=color, alpha=0.05)
    plt.xlabel("Mean")
    plt.ylabel("Std")
    plt.show()
    # plt.savefig("scatter.svg")