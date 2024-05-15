if __name__ == "__main__":
    from utilities import *
    import pandas as pd
    import numpy as np
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

    x_min, x_max = X.quantile(0.01)-1, X.quantile(0.99)+1

    h = .02  # step size in the mesh
    xx, yy = np.meshgrid(np.arange(x_min[parameters[0]], x_max[parameters[0]], h), np.arange(x_min[parameters[1]], x_max[parameters[1]], h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(7, 7))
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8, rasterized=True)
    scatter = plt.scatter(X[parameters[0]], X[parameters[1]], c=Y, cmap=plt.cm.coolwarm, s=20, alpha=0.1, rasterized=True)

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    plt.legend(handles=scatter.legend_elements()[0], labels=["No Attack", "Attack"])

    plt.xlabel(parameters[0].split("_")[0])
    plt.ylabel(parameters[1].split("_")[0])

    # plt.savefig("svm_delta_mean.svg", dpi=300)
    plt.show()

    # using sklearn ConfusionMatrixDisplay, plot the confusion matrix in shades of blue and normalized
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    predictions = clf.predict(X)
    disp = ConfusionMatrixDisplay.from_predictions(Y, predictions, display_labels=["No Attack", "Attack"], cmap=plt.cm.Blues, normalize="true")
    disp.ax_.set_title("Normalized Confusion Matrix, all parameters")
    plt.savefig("confusion_matrix_svm_delta_mean.pdf")
    plt.show()

    # calculate the accuracy, precision, recall, and F1 score
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = accuracy_score(Y, predictions)
    precision = precision_score(Y, predictions)
    recall = recall_score(Y, predictions)
    f1 = f1_score(Y, predictions)
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 score: ", f1)
    # calculate the ROC curve
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, _ = roc_curve(Y, predictions)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic, all parameters')
    plt.legend(loc="lower right")
    # plt.savefig("roc_curve_svm_delta_mean.pdf")
    plt.show()

