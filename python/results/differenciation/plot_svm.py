if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    
    file1 = open("diff_attack.csv", "r")
    file2 = open("diff_no_attack.csv", "r")
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)

    file1 = open("alpha_fit_normalized.csv", "r")
    df = pd.read_csv(file1, sep=",")

    x1 = pd.Series([(float(x_new.mean().iloc[0]), float(x_new.std().iloc[0])) for x_new in [(df1[898*j+720:898*(j+1)] - df1[898*j:898*j+720].mean())/df1[898*j:898*j+720].std() for j in range(len(df1)//898)]])
    x2 = pd.Series([(float(x_new.mean().iloc[0]), float(x_new.std().iloc[0])) for x_new in [(df2[898*j+720:898*(j+1)] - df2[898*j:898*j+720].mean())/df2[898*j:898*j+720].std() for j in range(len(df2)//898)]])
    # alternating x1 and x2
    xMeanStd = pd.concat([x1, x2], axis=0)

    # Add x1 and x2 to df
    df["mean_values"], df["std_values"] = zip(*xMeanStd)

    parameters = ["delta_values", "mean_values"]

    Y = df["attack_value"].astype(float)
    color = ["red" if i == 1.0 else "blue" for i in Y]
    legend = ["Attack" if i == 1.0 else "No Attack" for i in Y]
    X = df[parameters].astype(float)

    # calculate svm with X and Y
    from sklearn import svm
    clf = svm.SVC()
    clf.fit(X, Y)

    # print(clf.coef_)
    # print(clf.intercept_)

    x_min, x_max = X.min() - 1, X.max() + 1
    

    h = .02  # step size in the mesh
    xx, yy = np.meshgrid(np.arange(x_min[parameters[0]], x_max[parameters[0]], h), np.arange(x_min[parameters[1]], x_max[parameters[1]], h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
    scatter = plt.scatter(X[parameters[0]], X[parameters[1]], c=Y, cmap=plt.cm.coolwarm)

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    plt.legend(handles=scatter.legend_elements()[0], labels=["No Attack", "Attack"])

    plt.xlabel(parameters[0])
    plt.ylabel(parameters[1])

    plt.show()