if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import statsmodels.api as sm
    
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

    parameters = ["alpha_values", "beta_values", "gamma_values", "delta_values", "mean_values", "std_values"]

    Y = df["attack_value"].astype(float)
    X = df[parameters].astype(float)
    X = sm.add_constant(X)
    model = sm.GLS(Y,X)
    results = model.fit()
    print(results.summary())
    