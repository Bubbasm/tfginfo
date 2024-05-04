if __name__ == "__main__":
    from datetime import datetime
    from matplotlib.widgets import Slider
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    import numpy as np
    import time
    from utilities import *
    from holt_winters import *
    import numpy as np


    segsInDay = 86400
    movingAvgWindow = 60*10

    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df1, df2])
    df = ugr_crop_few_minutes(df, 10)

    train = ugr_get_first_n_days(df, 9)
    test = ugr_get_first_n_days(df, 10)

    param="Bitrate"
    lastTwoHours = train[param]

    alpha, beta, gamma= 0.5408062471295899, 0.0, 0.1750058448315196
    rate = triple_exponential_smoothing(lastTwoHours, segsInDay, alpha, beta, gamma, segsInDay)

    fig, axs = plt.subplots(2, 1, figsize=(16,8))
    plt.subplots_adjust(left=0.1, bottom=0.1)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()

    fig.suptitle(f"Holt-Winters, alpha={alpha}, beta={beta}, gamma={gamma}")
    fig.supxlabel("Time")
    fig.supylabel("Value")

    line1, = axs[0].plot(test["Date"][-segsInDay:], smooth(rate, movingAvgWindow)[-segsInDay:], color="#1368CE", label="Prediction Holt-Winters")
    line2, = axs[0].plot(test["Date"][-segsInDay:], smooth(test[param], movingAvgWindow)[-segsInDay:], color="#26890C", label="Real")
    line3, = axs[1].plot(test["Date"][-segsInDay:], smooth(rate-test[param], movingAvgWindow)[-segsInDay:], color="#E21B3C", label="Error")

    print("MSE: ", "{:.2E}".format(np.mean(((rate-test[param])[-segsInDay:])**2)))

    axs[0].legend()
    axs[1].legend()
    plt.savefig("holt_winters_prediccion_three.svg")
    # plt.show()
