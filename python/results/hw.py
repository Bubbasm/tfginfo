if __name__ == "__main__":
    from utilities import *
    import holt_winters.holt_winters as hw
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd


    df0 = ugr_load_data("june", 1)
    df1 = ugr_load_data("june", 2)
    df2 = ugr_load_data("june", 3)

    df = ugr_concat_data_list([df0, df1, df2])

    df = ugr_get_last_n_days(ugr_get_first_n_days(df, 17), 17)

    df = ugr_crop_few_minutes(df, 30, 0)

    twodays = ugr_get_first_n_days(df, 7)
    threedays = ugr_get_first_n_days(df, 8)

    param="Bitrate"
    movingAvgWindow = 60+1

    npred = 300

    alpha, beta, gamma= 0.55, 0.0, 1
    rate = hw.triple_exponential_smoothing(twodays[param], 86400, alpha, beta, gamma, npred)
    fig, ax = plt.subplots(figsize=(16,9))
    plt.subplots_adjust(left=0.1, bottom=0.1)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    # plt.gcf().autofmt_xdate()

    plt.title("Triple Exponential Smoothing")
    plt.xlabel("Time")
    plt.ylabel(param)

    line1, = plt.plot(threedays["Date"][len(twodays)-2*npred:len(rate)], smooth(rate, movingAvgWindow)[len(twodays)-2*npred:len(rate)], color="#1368CE", label="Holt-Winters")
    line2, = plt.plot(threedays["Date"][len(twodays)-2*npred:len(rate)], smooth(threedays[param], movingAvgWindow)[len(twodays)-2*npred:len(rate)], color="#26890C", label="Real")
    # difference between line1 and line2
    line3, = plt.plot(threedays["Date"][len(twodays)-2*npred:len(rate)], np.subtract(smooth(rate, movingAvgWindow)[len(twodays)-2*npred:len(rate)], smooth(threedays[param], movingAvgWindow)[len(twodays)-2*npred:len(rate)]), color="#AA00AA", label="Difference")
    # vertical line at threedays["Date"][len(twodays)]
    # lineV, = plt.plot([threedays["Date"][len(twodays)], threedays["Date"][len(twodays)]], [0, 10**9], color="#FF0000", label="Prediction")
    plt.gca().legend(loc='upper left')

    # Print the Mean Squared Error of the difference between line1 and line2 in scientific notation
    mse = np.square(np.subtract(threedays[param][len(twodays):len(rate)], rate[len(twodays):len(rate)])).mean() 
    print("Mean Squared Error: {:.2e}".format(mse))
    # Print the maximum error of the difference between line1 and line2
    maxe = np.max(np.subtract(threedays[param][len(twodays):len(rate)], rate[len(twodays):len(rate)]))
    print("Maximum Error: {:.2e}".format(maxe))

    # from matplotlib.widgets import Slider
    # plt.subplots_adjust(left=0.1, bottom=0.25)
    # axcolor = 'lightgoldenrodyellow'
    # axalpha = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
    # axbeta = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)
    # axgamma = plt.axes([0.1, 0.00, 0.65, 0.03], facecolor=axcolor)
    # s_alpha = Slider(axalpha, 'Alpha', 0.0, 1.0, valinit=alpha)
    # s_beta = Slider(axbeta, 'Beta', 0.0, 1.0, valinit=beta)
    # s_gamma = Slider(axgamma, 'Gamma', 0.0, 1.0, valinit=gamma)
    # def update(val):
    #     alpha = s_alpha.val
    #     beta = s_beta.val
    #     gamma = s_gamma.val

    #     # Recalculate rate with updated alpha, beta, and gamma
    #     rate = hw.triple_exponential_smoothing(twodays[param], 86400, alpha, beta, gamma, npred)

    #     # Update plot data
    #     line1.set_ydata(smooth(rate, movingAvgWindow)[len(twodays)-2*npred:len(rate)])
    #     line3.set_ydata(np.subtract(smooth(rate, movingAvgWindow)[len(twodays)-2*npred:len(rate)], smooth(threedays[param], movingAvgWindow)[len(twodays)-2*npred:len(rate)]))

    #     print("alpha, beta, gamma = {:.2f}, {:.2f}, {:.2f}".format(alpha, beta, gamma))
    #     # Print the error
    #     esm = np.mean(np.subtract(rate[len(twodays)-2*npred:len(rate)], threedays[param][len(twodays)-2*npred:len(rate)]))**2
    #     print("Mean Squared Error: {:.2e}".format(mse))
    #     maxe = np.max(np.subtract(rate[len(twodays)-2*npred:len(rate)], threedays[param][len(twodays)-2*npred:len(rate)]))
    #     print("Maximum Error: {:.2e}".format(maxe))

    #     # Redraw the plot
    #     fig.canvas.draw_idle()
    #     # plt.savefig("holt_winters"+str(int(time.time()))+".png")
    # # Attach the update function to the sliders
    # s_alpha.on_changed(update)
    # s_beta.on_changed(update)
    # s_gamma.on_changed(update)

    # save as svg
    # plt.savefig("../../images/holt_winters.svg")
    plt.show()

    import json
    # print errors as json object:
    d = {}
    d["name"] = ".svg"
    d["mse"] = "{:.2e}".format(mse)
    d["maxe"] = "{:.2e}".format(maxe)
    print(json.dumps(d)+",")
