def inv_diff(data, diff, period):
    """
    Inverse the difference of a time series
    """
    import pandas as pd

    inv_data = pd.Series(data).reset_index(drop=True, inplace=False)
    inv_data[period:] = inv_data[period:] + diff
    return inv_data

if __name__ == "__main__":
    from utilities import *
    import holt_winters.holt_winters as hw
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    pd.options.mode.chained_assignment = None

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)
    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 58.85, 60)
    print(df["Date"][0])

    dataComplete = df
    dataComplete = ugr_get_few_minutes(dataComplete, 60*7+10, 60*24*8)
    trainDays = 5
    dataTrain = ugr_get_first_n_days(dataComplete, trainDays)

    lastDayOffset = 60*60*24*7

    # dataComplete["Bitrate"][lastDayOffset-100:lastDayOffset+280] = dataComplete["Bitrate"][lastDayOffset-100:lastDayOffset+280] + 2*10**8

    param="Bitrate"
    movingAvgWindow = 30

    npred = 300

    daydiff = dataTrain.diff(periods=86400)
    daydiff = daydiff.dropna().reset_index(drop=True, inplace=False)


    npDataTrain = np.array(dataTrain[param]).reshape(-1, trainDays, order='F') 
    avgday = pd.Series(np.mean(npDataTrain, axis=1))
    medianday = pd.Series(np.median(npDataTrain, axis=1))

    alpha, beta, gamma= 1.0, 0.00, 1.0
    rate = hw.triple_exponential_smoothing(daydiff[param], 86400, alpha, beta, gamma, npred)
    # Inverse daydiff to get the original data
    dataTrainAvg = pd.concat([dataTrain[param], avgday[:npred]])
    rate = inv_diff(dataTrainAvg, rate, 86400)
    fig, ax = plt.subplots(figsize=(16,9))
    plt.subplots_adjust(left=0.1, bottom=0.1)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    # plt.gcf().autofmt_xdate()

    plt.title("Triple Exponential Smoothing")
    plt.xlabel("Time")
    plt.ylabel(param)

    line1, = plt.plot(dataComplete["Date"][len(dataTrain)-2*npred:len(rate)], smooth(rate, movingAvgWindow)[len(dataTrain)-2*npred:len(rate)], color="#1368CE", label="Holt-Winters")
    line2, = plt.plot(dataComplete["Date"][len(dataTrain)-2*npred:len(rate)], smooth(dataComplete[param], movingAvgWindow)[len(dataTrain)-2*npred:len(rate)], color="#26890C", label="Real")
    line3, = plt.plot(dataComplete["Date"][len(dataTrain)-2*npred:len(rate)], np.subtract(smooth(rate, movingAvgWindow)[len(dataTrain)-2*npred:len(rate)], smooth(dataComplete[param], movingAvgWindow)[len(dataTrain)-2*npred:len(rate)]), color="#AA00AA", label="Difference")
    # vertical line at dataComplete["Date"][len(dataTrain)]
    # lineV, = plt.plot([dataComplete["Date"][len(dataTrain)], dataComplete["Date"][len(dataTrain)]], [0, 10**9], color="#FF0000", label="Prediction")
    plt.gca().legend(loc='upper left')

    realData = dataComplete[param][len(dataTrain):len(rate)]
    predData = rate[len(dataTrain):len(rate)]
    # Print the Mean Squared Error of the difference between line1 and line2 in scientific notation
    mse = np.square(np.subtract(realData, predData)).mean() 
    print("Mean Squared Error: {:.2e}".format(mse))
    # Print the maximum error of the difference between line1 and line2
    maxe = np.max(np.subtract(realData, predData))
    print("Maximum Error: {:.2e}".format(maxe))
    plt.show()

    import json
    # print errors as json object:
    d = {}
    # d["name"] = ".svg"
    d["mse"] = "{:.2e}".format(mse)
    d["maxe"] = "{:.2e}".format(maxe)
    print(json.dumps(d)+",")