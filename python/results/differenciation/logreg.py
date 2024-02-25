if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import statsmodels.api as sm

    from statsmodels.discrete.discrete_model import Logit
    
    file = open("linregr2.txt", "r")
    columns=["a", "b", "c", "d", "e", "f", "attack"]

    df = pd.read_csv(file, sep=" ", names=columns)

    # I want to perform linear regression with variables a, b, c, d, e, f with OLS

    Y = df["attack"].astype(float)
    X = df[["c", "d"]].astype(float)
    X = sm.add_constant(X)
    model = Logit(Y,X)
    results = model.fit()
    print(results.summary())
    