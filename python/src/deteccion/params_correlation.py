if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import statsmodels.api as sm
    
    file1 = open("../csv/diff_attack.csv", "r")
    file2 = open("../csv/diff_no_attack.csv", "r")
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)
    dff = pd.concat([df1, df2], axis=0)

    file1 = open("../csv/alpha_fit_normalized.csv", "r")
    df = pd.read_csv(file1, sep=",")

    xMeanStd = pd.Series([(float(x_new.mean().iloc[0]), float(x_new.std().iloc[0])) for x_new in [(dff[898*j+720:898*(j+1)] - dff[898*j:898*j+720].mean())/dff[898*j:898*j+720].std() for j in range(len(dff)//898)]])

    df["mean_values"], df["std_values"] = zip(*xMeanStd)
    
    parameters = ["delta_values", "mean_values"]

    # Calculate the correlation matrix
    corr = df[parameters].corr()
    print(corr)