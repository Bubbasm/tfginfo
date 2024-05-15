def train_test_split_2(X, Y):
    """
    Split the data into training and testing sets.
    """
    import random
    import pandas as pd
    # take 80% of continuous data for training at random and 20% for testing
    randomPercentage = random.random()*0.8
    train_X = pd.concat([X[:int(len(X)*randomPercentage)], X[int(len(X)*(randomPercentage+0.2)):]])
    train_Y = pd.concat([Y[:int(len(X)*randomPercentage)], Y[int(len(X)*(randomPercentage+0.2)):]])
    test_X = X[int(len(X)*randomPercentage)+900:-900+int(len(X)*(randomPercentage+0.2))]
    test_Y = Y[int(len(X)*randomPercentage)+900:-900+int(len(X)*(randomPercentage+0.2))]
    return train_X, test_X, train_Y, test_Y

# utilizar ventanas totalmente disjuntas o días distintos.

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

    # qt = 0.50
    # xPercentile = pd.Series([float(x_new.quantile(qt).iloc[0]) for x_new in [(dff[898*j+720:898*(j+1)])/dff[898*j:898*j+720].quantile(qt) for j in range(len(dff)//898)]])
    # qtStr = str(qt)[2:]
    # df["q0."+qtStr+"_values"] = xPercentile

    df = df.dropna()
    parameters = ["alpha_values", "beta_values", "gamma_values", "delta_values", "mean_values", "std_values"] # , "q0."+qtStr+"_values"
    # parameters = ["delta_values", "mean_values"]

    full_Y = df["attack_value"].astype(float)
    full_X = df[parameters].astype(float)
    full_X = sm.add_constant(full_X)
    att_X = full_X[full_Y == 1].reset_index(drop=True)
    att_Y = full_Y[full_Y == 1].reset_index(drop=True)
    no_att_X = full_X[full_Y == 0].reset_index(drop=True)
    no_att_Y = full_Y[full_Y == 0].reset_index(drop=True)

    # take 80% of the data for training and 20% for testing
    Xatt,tXatt,Yatt,tYatt = train_test_split_2(att_X, att_Y)
    Xnoatt,tXnoatt,Ynoatt,tYnoatt = train_test_split_2(no_att_X, no_att_Y)
    Y = pd.concat([Yatt, Ynoatt])
    X = pd.concat([Xatt, Xnoatt])
    tY = pd.concat([tYatt, tYnoatt])
    tX = pd.concat([tXatt, tXnoatt])
    model = Logit(Y,X)
    results = model.fit()
    print(results.summary())
    # calculate the accuracy of the model with test data
    predictions = results.predict(tX)
    predictions_nominal = [1 if i > 0.5 else 0 for i in predictions]
    # using sklearn ConfusionMatrixDisplay, plot the confusion matrix in shades of blue and normalized
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    import matplotlib.pyplot as plt
    disp = ConfusionMatrixDisplay.from_predictions(tY, predictions_nominal, display_labels=["No Attack", "Attack"], cmap=plt.cm.Blues, normalize="true")
    disp.ax_.set_title("Normalized Confusion Matrix, all parameters")
    plt.savefig("confusion_matrix.svg")
    # plt.show()

    # calculate the accuracy of the model
    accuracy = sum([1 if tY.iloc[i] == predictions_nominal[i] else 0 for i in range(len(tY))])/len(tY)
    print("Accuracy: ", accuracy)
    # calculate the precision of the model
    precision = sum([1 if tY.iloc[i] == 1 and predictions_nominal[i] == 1 else 0 for i in range(len(tY))])/sum(predictions_nominal)
    print("Precision: ", precision)
    # calculate the recall of the model
    recall = sum([1 if tY.iloc[i] == 1 and predictions_nominal[i] == 1 else 0 for i in range(len(tY))])/sum(tY)
    print("Recall: ", recall)
    # calculate the F1 score of the model
    f1 = 2*(precision*recall)/(precision+recall)
    print("F1 score: ", f1)
    # calculate the ROC curve
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, _ = roc_curve(tY, predictions)
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
    plt.savefig("roc_curve.svg")
    # plt.show()
